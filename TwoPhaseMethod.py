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


        BV= []
        for x in range(self.m):
            for y in range(self.n, len(self.tableau[0])):
                if self.tableau[x][y] == 1:
                    BV.append(y)

        print("before phase one: ")

        for x in self.tableau:
            print(x)
        print(z_p1)
        print(b)
        print(BV)
        smplx = Simplex(self.tableau, b, z_p1, -1)
        smplx.BV = BV
        maxValues, Z_final, state = smplx.method()

        self.tableau = smplx.A
        self.BV = smplx.BV
        print("after phase one: ")
        self.b = smplx.b

        print(maxValues)
        print(smplx.Z)
        for x in self.tableau:
            print(x)

    def phaseTwo(self):
        print("---------------------------------------------------------")
        z_p2 = self.Z
        for y in range(self.artificialVars):
            self.tableau = self.tableau[:, :-1]
        for i in range(self.m):
            z_p2.append(0)

        # print(z_p2)
        # print(self.tableau)
        smplx = Simplex(self.tableau,self.b,z_p2,self.objective)
        smplx.BV = self.BV
        maxValues, Z_final, state = smplx.method()

        print(self.tableau)
        print(smplx.b)
        print(Z_final)
        print(state)
        print(maxValues)
        print(smplx.Z)

A = [
    [1,1,1],
    [2,-5,1]
]
b = [7, 10]
Z = [1, 2, 1]
signs = ['=', '>=']

p = TwoPhaseMethod(A,b,Z,signs,1)
p.initialTableau()
p.phaseOne()
p.tableau = np.array([
    [0,1,1/7,0,1/7,2/7,-1/7],
    [1,0,6/7,0,-1/7,5/7,1/7]
])
p.b = [4/7,45/7]
p.BV = [1,0]
print()
p.phaseTwo()













