import numpy as np
from tabulate import tabulate

from simplex import Simplex

M = 1000000
class BigM2:
    def __init__(self, A, b, Z, urv, signs, objective):
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
        self.artificialVarCol =[]


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
        c = 0
        for x in range(self.m):
            z = False
            for y in range(self.artificialVars):
                if c == y and (self.signs[x] == '>=' or self.signs[x] == '='):
                    self.tableau[x].append(1)
                    z = True
                else:
                    self.tableau[x].append(0)
            if z:
                c += 1

        self.Z += [0]*self.m
        self.Z += [M*-1] *self.artificialVars
        for x in range(self.m+ self.n,len(self.Z)):
            self.artificialVarCol.append(x)
        #print(self.artificialVarCol)

        self.BV = []
        for x in range(self.m):
            for y in range(self.n, len(self.tableau[0])):
                if self.tableau[x][y] == 1:
                    self.BV.append(y)

    def removeVar(self,ind):
        self.Z.pop(ind)
        for i in range(len(self.A)):
            self.tableau[i].pop(ind)

    def solve(self):
        for i,s in enumerate(self.signs):
            if s == '>=' or s == '=':
                self.Z_final += self.b[i]*M
                for x in range(len(self.Z)):
                    self.Z[x] += self.tableau[i][x]*M


        simplex = Simplex(self.tableau, self.b, self.Z, self.urv, self.objective)
        simplex.Z_final = self.Z_final*-1
        simplex.BV = self.BV
        simplex.artificialCount = self.artificialVars
        simplex.numberOfVars = self.n
        simplex.addURV()
        simplex.ansSetup()
        #print(simplex.varNames)
        try:
            x,y,z = simplex.method()
        except ValueError as e:
            self.steps += simplex.steps
            self.steps += f'{e}\n'
            return False    
        self.steps += simplex.steps
        for i in simplex.BV:
            for j in self.artificialVarCol:
                if i == j:
                    self.steps += 'No solution\n'
                    return False

        self.steps += f"Max values of variables: {x}\n"
        self.steps += f"Final value of Z: {y}\n"
        self.steps += f"Status: {z}\n"

        return True


A = [
    [1,-1]
    
]
b = [2]
Z = [2,1]
urv =[0,1]
signs = ['<=']
x = BigM2(A, b, Z, urv, signs, 1)
x.initialTableau()
x.solve()
print(x.steps)


