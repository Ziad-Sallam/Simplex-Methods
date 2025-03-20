import numpy as np

class Simplex():
    def __init__(self, A, b, Z , objective):
        """
        :param A: Coefficient of constraints
        :param b: Right hand side
        :param Z: Coefficient of the objective function
        :param objective: 1 to maximization ,-1 for minimization
        """
        self.objective = objective # 1 for maximization, -1 for minimization
        self.m = len(A) # number of slack variables
        self.n = len(A[0]) # number of variables
        self.A = np.array(A, dtype=float)  # coefficient matrix
        self.b = np.array(b, dtype=float)  # RHS
        self.Z = np.array(Z, dtype=float) * -1 # objective vector
        self.Z_final = 0
        self.BV = [i + self.n for i in range(self.m)]  # Basic variables

    def addingSlackVars(self):
        identity = np.eye(self.m)
        self.A = np.hstack((self.A, identity))
        self.Z = np.append(self.Z, np.zeros(self.m))
    
    def method(self):
        optimal = False
        while not optimal:
            if self.objective == 1:
                pivotCol = np.argmin(self.Z)
            else:
                pivotCol = np.argmax(self.Z)

            if np.all(self.A[:, pivotCol] <= 0):
                return None, None, "Unbounded solution"

            ratios = np.zeros(self.m)
            for i in range(self.m):
                if self.A[i, pivotCol] > 0:
                    ratios[i] = self.b[i] / self.A[i, pivotCol]
                else:
                    ratios[i] = np.inf

            pivotRow = np.argmin(ratios)

            factor = self.A[pivotRow, pivotCol]
            self.A[pivotRow] /= factor
            self.b[pivotRow] /= factor

            for i in range(self.m):
                if i != pivotRow:
                    factor = self.A[i, pivotCol]
                    self.A[i] -= factor * self.A[pivotRow]
                    self.b[i] -= factor * self.b[pivotRow]
        
            factor = self.Z[pivotCol]
            self.Z -= factor * self.A[pivotRow]
            self.Z_final -= factor * self.b[pivotRow]

            self.BV[pivotRow] = pivotCol
            if self.objective == 1:
                optimal = np.all(self.Z >= 0)
            else:
                optimal = np.all(self.Z <= 0)

        maxValues = np.zeros(self.n)
        for i in range(self.m):
            if self.BV[i] < self.n:
                maxValues[self.BV[i]] = self.b[i]

        return maxValues, self.Z_final, "optimum solution"

def main():
    A = [[1, 4], [1, 2]]
    b = [8, 4]
    Z = [3, 9]
    objective = 1 #min
    simplex = Simplex(A, b, Z, objective)
    simplex.addingSlackVars()
    maxValues, Z_final, status = simplex.method()

    print("Max values of variables:", maxValues)
    print("Final value of Z:", Z_final)
    print("Status:", status)

#main()