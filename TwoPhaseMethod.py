import numpy as np

from simplex import Simplex


class TwoPhaseMethod(object):
    def __init__(self,A,b,Z,signs,objective):
        """
        :param A: coefficient of constraints
        :param b: right hand side of constraints
        :param Z: coefficient of objective function
        :param signs: '>=', '<=', or '==',
        :param objective: 1 to maximization ,-1 for minimization
        """
        self.artificialVars = 0
        self.A = A
        self.b = b
        self.Z = Z
        self.signs = signs
        self.objective = objective
        self.m = len(A)
        self.n = len(A[0])
        self.tableau = A


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
        z = [0]*(self.n + self.m)
        for i in range(self.artificialVars):
            z.append(1)

        smplx = Simplex(self.tableau,b,Z,-1)
        BV= []
        for x in range(self.m):
            for y in range(self.n, len(self.tableau[0])):
                if self.tableau[x][y] == 1:
                    BV.append(y)
        smplx.BV = BV
        maxValues, Z_final, state = smplx.method()
        print(Z_final)
        print(state)
        print(maxValues)
        for x in self.tableau:
            print(x)




A = [[-1,3],
     [1,-3] ,
     [1,1]]

b = [6,6,1]
Z = [0,0,0,0,0,1,1]
signs = ['<=', '=', '>=']

p = TwoPhaseMethod(A,b,Z,signs,None)
p.initialTableau()
p.phaseOne()

# x = Simplex(p.tableau,b,Z,-1)
# x.BV = [2,5,6]
# for i in p.tableau:
#     print(i)
# a, b, c = x.method()
# print(a)
# print(b)
# print(c)










