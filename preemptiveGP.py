import numpy as np
from simplex import Simplex

class PreemptiveGP():
    def __init__(self,G, Gb, A, b, signs):
        self.G = np.array(G, dtype=float)
        self.Gb = np.array(Gb, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.signs = np.array(signs, dtype=str)
        self.k = len(G)
        self.m = len(A)
        self.n = len(A[0])
        self.BV =  [i + self.n+self.k for i in range(self.m+self.k)] 

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
        self.G = np.zeros((self.k, self.n+2*self.k+self.m))
        self.Gb = np.zeros(self.k)
        for i in range(self.k):
            if self.signs[i] == '>=':
                self.G[i][i+self.n+self.k] = -1
            elif self.signs[i] == '<=':
                self.G[i][i+self.n] = -1
            else:
                self.G[i][i+self.n] = -1
                self.G[i][i+self.n+self.k] = -1
                        
    def method(self):
        tol = 1e-9
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

        maxValues = np.zeros(self.n)
        for i in range(self.m+self.k):
            if self.BV[i] < self.n:
                maxValues[self.BV[i]] = self.tableauRHS[i]

        return maxValues  
                    




def main():
    Gh = np.array([[200, 0], [100, 400], [0, 250 ]])
    Gb = [1000, 1200, 800]
    Ah = [[1500, 3000]]
    b = [15000]
    signs = ['>=', '>=', '>=']
    preemptive = PreemptiveGP(Gh, Gb, Ah, b, signs)
    preemptive.initialTableau()
    preemptive.setGoals()
    maxvalues = preemptive.method()
    np.set_printoptions(precision=6, suppress=True)
    print(preemptive.G)
    print(preemptive.Gb)
    print(preemptive.tableau)
    print(preemptive.tableauRHS)
    print(maxvalues)
main()    
       
