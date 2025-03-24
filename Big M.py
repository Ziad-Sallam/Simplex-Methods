import numpy as np
from simplex import Simplex
from tabulate import tabulate

class BigMMethod(Simplex):
    def __init__(self, A, b, Z, urv, signs, objective):
        super().__init__(A, b, Z, urv, objective)
        self.signs = signs
        self.M = 1e6

    def addingArtificialVars(self):
        artificial = []
        artificial_indices = []
        for i, sign in enumerate(self.signs):
            if sign in ['=', '>=']:
                col = np.zeros(self.m)
                col[i] = 1
                artificial.append(col)
                artificial_indices.append(self.n + len(artificial) - 1)
                self.varNames.append(f"A{i + 1}'")
        if artificial:
            artificial = np.array(artificial).T
            self.A = np.hstack((self.A, artificial))
            self.Z = np.append(self.Z, np.ones(len(artificial_indices)) * self.M)
            self.artificial_vars = artificial_indices
            self.BV.extend(artificial_indices)

    def method(self):
        for i in range(len(self.artificial_vars)):
            if self.b[i] < 0:
                self.A[i] *= -1
                self.b[i] *= -1

        for i, var in enumerate(self.artificial_vars):
            self.Z -= self.M * self.A[i]
            self.Z_final -= self.M * self.b[i]

        maxValues, Z_final, status = super().method()

        for var in self.artificial_vars:
            if var in self.BV:
                return None, None, "Infeasible solution"

        self.Z = self.Z[:self.n]
        self.A = self.A[:, :self.n]
        self.varNames = self.varNames[:self.n]

        maxValues, Z_final, status = super().method()

        return maxValues, Z_final, status
    
    def ansSetup(self):
        self.varNames = [f'x{i}' for i in range(self.n)]
        self.varNames.insert(0, '')
        for i in range(self.m):
            if self.signs[i] == '<=':
                self.varNames.append(f'S{i}')
            elif self.signs[i] == '>=':
                self.varNames.append(f'R{i}')
        if hasattr(self, 'artificial_vars'):
            for i, var in enumerate(self.artificial_vars):
                self.varNames.append(f"A{i + 1}'")
        self.varNames.append('RHS')

    def addToSteps(self):
        self.stp = []
        self.stp.append(self.varNames)
        z = ['Z']
        for i in range(len(self.A[0])):
            z.append(self.Z[i])
        z.append(self.Z_final)
        self.stp.append(z)
        for i in range(len(self.A)):
            x = self.A[i].tolist()
            x.insert(0, self.varNames[self.BV[i] + 1])
            x.append(self.b[i])
            self.stp.append(x)
        self.steps += tabulate(self.stp, tablefmt='grid') + '\n\n'

    def addURV(self):
        if hasattr(self, 'urv') and any(self.urv):
            for i in range(len(self.urv)):
                if self.urv[i] == 1:
                    coeff = np.array(self.A[:, i]) * -1
                    self.A = np.hstack((self.A, coeff.reshape(-1, 1)))
                    self.Z = np.append(self.Z, self.Z[i] * -1)
                    self.BV.append(self.n + self.m + i)
            self.urvCols = []
            for j in range(len(self.urv)):
                if self.urv[j] == 1:
                    self.urvCols.append(j)

def main():
    A = [[1, 1], [2, -1]]
    b = [4, -5]
    Z = [2, 3]
    objective = 1  # 1 for maximization, -1 for minimization
    urv = [0, 1]
    signs = ['<=', '<=']
    big_m = BigMMethod(A, b, Z, urv, signs, objective)
    big_m.addingSlackVars()
    big_m.addURV()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    
if __name__ == "__main__":
    main()