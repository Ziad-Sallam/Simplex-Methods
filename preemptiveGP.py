import numpy as np
from simplex import Simplex
from tabulate import tabulate


class PreemptiveGP():
    def __init__(self,G, Gb, A, b, urv, signs):
        self.G = np.array(G, dtype=float)
        self.Gb = np.array(Gb, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.urv = np.array(urv, dtype=float)
        self.signs = np.array(signs, dtype=str)
        self.k = len(G)
        self.m = len(A)
        self.n = len(A[0]) if len(A) > 0 else len(G[0])
        self.BV =  [i + self.n+self.k for i in range(self.m+self.k)]
        self.counturv = (self.urv == 1).sum() 
        self.steps = ''

    def initialTableau(self):
        self.tableau = np.zeros((self.m+self.k, self.n + 2*self.k+self.m), dtype=float)
        self.tableauRHS = np.zeros(self.m+self.k, dtype=float)
        for i in range(self.k):
            self.tableau[i, :self.n] = self.G[i]
            self.tableau[i, i+self.n] = -1
            self.tableau[i, i+self.n+self.k] = 1
            self.tableauRHS[i] = self.Gb[i]
        for i in range(self.m):
            self.tableau[i+self.k, :self.n] = self.A[i]
            self.tableau[i+self.k ,i+self.n+2*self.k] = 1
            self.tableauRHS[i+self.k] = self.b[i]

    def setGoals (self):
        self.G = np.zeros((self.k, self.n+2*self.k+self.m+self.counturv))
        self.Gb = np.zeros(self.k)
        for i in range(self.k):
            if self.signs[i] == '>=':
                self.G[i][i+self.n+self.k] = -1
            elif self.signs[i] == '<=':
                self.G[i][i+self.n] = -1
            else:
                self.G[i][i+self.n] = -1
                self.G[i][i+self.n+self.k] = -1

    def addURV(self):
        if self.counturv > 0:
            for i in range(len(self.urv)):
                if self.urv[i] == 1:
                    coeff = np.array(self.tableau[:,i]) * -1
                    self.tableau = np.hstack((self.tableau, coeff.reshape(-1,1)))
                    self.BV.append(self.n + self.m + 2*self.k+ i)

        self.urvCols =[]
        for j in range(len(self.urv)):
            if self.urv[j] == 1:
                self.urvCols.append(j) 

    def ansSetup(self):
        self.varNames = [f'x{i}' for i in range(0, self.n)]
        self.varNames.insert(0, '')
        for i in range(self.k):
            self.varNames.append(f'S{i}+')
        for i in range(self.k):
            self.varNames.append(f'S{i}-')
        for i in range(self.m):
            self.varNames.append(f'S{i+self.k}')    
        for i in range(self.counturv):
            self.varNames.append(f'X{self.urvCols[i]}\'')    
        self.varNames.append('RHS')


    def addToSteps(self):
        self.stp = []
        self.stp.append(self.varNames)
        
        for j in range(self.k):
            z = [f"Z{j}"]
            for i in range(len(self.G[0])):
                z.append(self.G[j,i])
            z.append(self.Gb[j])
            self.stp.append(z)

        for i in range(len(self.tableau)):
            x = self.tableau[i]
            x = x.tolist()
            x.insert(0,self.varNames[self.BV[i]+1])
            x.append(self.tableauRHS[i])
            self.stp.append(x)
        self.steps += tabulate(self.stp, tablefmt='grid') +'\n\n'                       
                        
    def method(self):
        tol = 1e-9
        self.addToSteps()
        for i in range(self.k):
            self.G[i] += self.tableau[i]
            self.Gb[i] += self.tableauRHS[i]
        cols = []
        
        for i in range(self.k):
            cols =[]
            for j in range(len(self.G[i])):

                if self.G[i,j] > tol:
                    cols.append(j)
                else :
                    cols.append(-1)    
            sortedcols = sorted(cols , key = lambda x: self.G[i,x], reverse=True)
            sortedcols = [x for x in sortedcols if x != -1] 
            while len(sortedcols) > 0 :
                pivotCol = sortedcols[0]
                valid_pivot = True


                for j in range(i):
                     if self.G[j, pivotCol] < 0:   
                        valid_pivot = False
                        break
                if not valid_pivot:
                    sortedcols.pop(0)
                    continue  


                ratios = np.zeros(self.m + self.k)
                for j in range(self.m + self.k):
                    if self.tableau[j, pivotCol] > 0:
                        ratios[j] = self.tableauRHS[j] / self.tableau[j, pivotCol]
                    else:
                        ratios[j] = np.inf
                if np.all(ratios == np.inf):
                    return None, "unbounded solution"        

                pivotRow = np.argmin(ratios)
                factor = self.tableau[pivotRow, pivotCol]
                self.tableau[pivotRow] /= factor
                self.tableauRHS[pivotRow] /= factor
                
                
                for j in range(self.k):
                    factor = self.G[j, pivotCol] 
                    self.G[j] -= factor * self.tableau[pivotRow]
                    self.Gb[j] -= factor * self.tableauRHS[pivotRow]
                    for k in range(len(self.G[i])):
                        if abs(self.G[j, k]) < tol:
                            self.G[j, k] = 0
                

                for j in range(self.m + self.k):
                    if j != pivotRow:
                        factor = self.tableau[j, pivotCol]
                        self.tableau[j] -= factor * self.tableau[pivotRow]
                        self.tableauRHS[j] -= factor * self.tableauRHS[pivotRow]
                        for k in range(len(self.tableau[i])):
                            if abs(self.tableau[j, k]) < tol:
                                self.tableau[j, k] = 0.0

                self.BV[pivotRow] = pivotCol
                if np.all(self.G[i] <= tol):
                    break      
                else:
                    cols = []
                    for j in range(len(self.G[i])):   
                        if self.G[i,j] > tol:
                            cols.append(j)
                        else :
                            cols.append(-1)    
                    sortedcols = sorted(cols , key = lambda x: self.G[i,x], reverse=True)
                    sortedcols = [x for x in sortedcols if x != -1]
            self.addToSteps()
        maxValues = np.zeros(self.n)
        for i in range(self.m+self.k):
            if self.BV[i] < self.n:
                maxValues[self.BV[i]] = self.tableauRHS[i]
            elif self.BV[i] >= self.n + self.m + 2*self.k:
                maxValues[self.BV[i] - self.m - 2*self.k] = self.b[i]
        status = ""
        for i in range(self.k):
            if self.Gb[i] > tol:
                status += f"Goal {i+1} not achieved\n"
            else:
                status += f"Goal {i+1} achieved\n"   
        return maxValues, status 
                    




def main():
    G = np.array([[1, 1], [1, 1]]) 
    Gb = [10,5]
    A = []
    b = []
    signs = ['>=', '<=']
    urv = [0,0]
    preemptive = PreemptiveGP(G, Gb, A, b,urv, signs)
    
    preemptive.initialTableau()
    preemptive.addURV()
    preemptive.setGoals()
    
    preemptive.ansSetup()
    print(preemptive.G[0])
    print(preemptive.tableau[0])
    maxvalues,status = preemptive.method()
   # np.set_printoptions(precision=6, suppress=True)
    # print(preemptive.G)
    # print(preemptive.Gb)
    # print(preemptive.tableau)
    # print(preemptive.tableauRHS)
    print(status)
    print(maxvalues)
    print(preemptive.steps)
main()    
       
