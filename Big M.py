import numpy as np
from simplex import Simplex

class BigMMethod(Simplex):
    def __init__(self, A, b, Z, objective):
        super().__init__(A, b, Z, objective)
        self.M = 1e6

    def addingArtificialVars(self):
        artificial = np.eye(self.m)
        self.A = np.hstack((self.A, artificial))
        self.Z = np.append(self.Z, np.ones(self.m) * self.M)
        self.artificial_vars = [self.n + self.m + i for i in range(self.m)]
        self.BV = self.artificial_vars.copy()

    def method(self):
        for i in range(len(self.artificial_vars)):
            if self.b[i] < 0:
                self.A[i] *= -1
                self.b[i] *= -1

        for i, var in enumerate(self.artificial_vars):
            self.Z -= self.M * self.A[i]
            self.Z_final += self.M * self.b[i]

        maxValues, Z_final, status = super().method()

        for var in self.artificial_vars:
            if var in self.BV:
                return None, None, "Infeasible solution"

        self.Z = self.Z[:self.n]
        self.A = self.A[:, :self.n]

        maxValues, Z_final, status = super().method()

        return maxValues, Z_final, status

def main():
    # test 1
    A = [[-1, 1], [1, -2], [-1, -1]]
    b = [-1, -2, -3]
    Z = [2, 1]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    print("\n")

    # test 2
    A = [[1, 1], [-1, -1]]
    b = [1, -3]
    Z = [2, 1]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    print("\n")

    # test 3
    A = [[1, -1]]
    b = [2]
    Z = [1, 1]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    print("\n")

    # test 4
    A = [[2, 1], [4, 2]]
    b = [4, 8]
    Z = [3, 2]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    print("\n")

    # test 5
    A = [[1, 1], [2, 2]]
    b = [5, 10]
    Z = [1, 1]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    print("\n")

    # test 6
    A = [[1, 1], [2, -1]]
    b = [4, -5]
    Z = [2, 3]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)
    print("\n")

    # test 7
    A = [[1, 1], [2, 2]]
    b = [4, 8]
    Z = [3, 2]
    objective = 1  # 1 for maximization, -1 for minimization
    big_m = BigMMethod(A, b, Z, objective)
    big_m.addingSlackVars()
    big_m.addingArtificialVars()
    maxValues, Z_final, status = big_m.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)

if __name__ == "__main__":
    main()