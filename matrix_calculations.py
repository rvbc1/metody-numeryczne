import json
import numpy as np

class MatrixCalculations:
    def __init__(self):
        pass

    def getMaxValue(self, matrix):
        return max([max(row) for row in matrix])

    def normalize(self, matrix):
        div_value = self.getMaxValue(matrix)
        if div_value == 0:
            div_value = 1
        return [[cell / div_value for cell in row] for row in matrix]

def met_gaussa(A, B):
    n = A.shape[0]
    C = np.zeros((n, n + 1))
    X = np.zeros(n)

    for i in range(n):
        for j in range(n):
            C[i, j] = A[i, j]
        C[i, n] = B[i]

    for p in range(n - 1):
        for i in range(p + 1, n):
            for j in range(p + 1, n + 1):
                C[i, j] = C[i, j] - C[i, p] * C[p, j] / C[p, p]

    X[n - 1] = C[n - 1, n] / C[n - 1, n - 1]

    for i in range(n - 2, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += C[i, j] * X[j]
        X[i] = (C[i, n] - suma) / C[i, i]

    return X