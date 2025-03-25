import numpy as np
from tabulate import tabulate

from simplex import Simplex


class TwoPhaseMethod(object):
    def __init__(self,A,b,Z,urv,signs,objective):
        """
        :param A: coefficient of constraints
        :param b: right hand side of constraints
        :param Z: coefficient of objective function
        :param signs: '>=', '<=', or '==',
        :param objective: 1 to maximization ,-1 for minimization
        """
        self.BV = None
        self.artificialVars = 0
        self.A = A
        self.b = b
        self.Z = Z
        self.signs = signs
        self.objective = objective
        self.m = len(A)
        self.n = len(A[0])
        self.tableau = A
        self.urv = urv
        self.steps = ''
        self.Z_final = 0


    def initialTableau(self):
        i = np.eye(self.m)
        self.artificialVars = 0
        for x in range(self.m):
            for y in range(self.m):
                if i[x][y] != 0:
                    if i[x][y] != 0:
                        if self.signs[x] == '>=':
                            i[x][y] = -1
                            self.artificialVars += 1
                        elif self.signs[x] == '=':
                            i[x][y] = 0
                            self.artificialVars += 1
                self.tableau[x].append(i[x][y])
        c=0
        for x in range(self.m):
            z = False
            for y in range(self.artificialVars):

                if c==y and (self.signs[x] == '>=' or self.signs[x] == '='):
                    self.tableau[x].append(1)
                    z = True
                else:
                    self.tableau[x].append(0)
            if z:
                c+=1


    def phaseOne(self):
        
        z_p1 = [0]*(self.n + self.m)
        for i in range(self.artificialVars):
            z_p1.append(1)
            
        for ind,s in enumerate(self.signs):
            if s=='>=' or s=='=':
                for i in range(len(z_p1)):
                    z_p1[i] -= self.tableau[ind][i]
        for i in b:
            self.Z_final +=i

        BV= []
        for x in range(self.m):
            for y in range(self.n, len(self.tableau[0])):
                if self.tableau[x][y] == 1:
                    BV.append(y)
        
        smplx = Simplex(self.tableau, b, z_p1, self.urv, -1)
        smplx.Z_final = self.Z_final
        smplx.artificialCount = self.artificialVars
        smplx.numberOfVars = self.n
        smplx.addURV()
        smplx.ansSetup()
        self.varNames = smplx.varNames
        smplx.BV = BV
        
        try:
            maxValues, Z_final, state = smplx.method()
        except ValueError as e:
            self.steps += str(e)
            return False        
        self.steps += smplx.steps

        self.tableau = smplx.A
        self.BV = smplx.BV

        self.b = smplx.b
        if smplx.Z_final != 0:
            return False
        else:
            return True


    def phaseTwo(self):
        self.steps += 'phase 2:\n'
        z_p2 = self.Z
        for y in range(self.artificialVars):
            self.tableau = self.tableau[:, :-1]
        for i in range(self.m):
            z_p2.append(0)
        for i in range(len(self.urv)):
            if self.urv[i] == 1:
                z_p2.append(z_p2[i]*-1)


        # print(self.tableau)
        remove = []
        for i  in self.varNames:
            if len(i) > 0:
                if i[0] == 'a':
                    remove.append(i)

        for i in remove:
            self.varNames.remove(i)
        smplx = Simplex(self.tableau,self.b,z_p2,[0]*self.n,self.objective)
        smplx.BV = self.BV
        smplx.varNames = self.varNames

        try:
            maxValues, Z_final, state = smplx.method()
        except ValueError as e:
            self.steps += str(e)
            return False

        self.steps += smplx.steps

        state = "Max" if self.objective == 1 else "Min"
        self.steps += f"\n{state} values of variables: {maxValues}\n"
        for i in range(len(maxValues)):
            if maxValues[i] !=0:
                self.steps += f"{self.varNames[i+1]}: {maxValues[i]}\n"


        self.steps += f"Z final: {Z_final}\n"
        self.steps += f"status: optimum solution\n"
        # print(self.tableau)
        # print(smplx.b)
        # print(Z_final)
        # print(state)
        # print(maxValues)
        # print(smplx.Z)
    def method(self):
        self.initialTableau()
        print("heeeeee")
        self.phaseOne()
        print("heeeeee")
        self.phaseTwo()
        print("heeeeee")



A = [
    [1,-1]
    
]
b = [2]
Z = [2,1]
urv =[0,1]
signs = ['<=']

p = TwoPhaseMethod(A,b,Z,urv,signs,1)
p.initialTableau()
if p.phaseOne():
    p.phaseTwo()
    print(p.steps)
else:
    print(p.steps)
    















