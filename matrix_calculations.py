import json

class Matrix:
    def __init__(self):
        self._data = []
        pass

    def setData(self, data):
        self._data = data

    def getData(self):  
        return self._data
    
    def getRows(self):
        return len(self._data)
    
    def getColumns(self):
        return len(self._data[0])
    
    def changeShape(self, new_rows, new_columns):
        if not self._data:
            self._data = [[0 for _ in range(new_columns)] for _ in range(new_rows)]
            return
        
        current_rows = self.getRows()
        if new_rows > current_rows:
            for _ in range(new_rows - current_rows):
                self._data.append([0] * new_columns)
        elif new_rows < current_rows:
            self._data = self._data[:new_rows]
        
        current_columns = self.getColumns()
        for row in self._data:
            if new_columns > current_columns:
                row.extend([0] * (new_columns - current_columns))
            elif new_columns < current_columns:
                del row[new_columns:]

        return self._data

    def getShape(self):
        return (self.getRows(), self.getColumns())
    
    # def setShape(self, size):
    #     return self.setShape(size, size)
    
    


  
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

    def met_gaussa_transponowana(matrixA, matrixB):
        A = matrixA.getData()
        B = matrixB.getData()
        n = len(A)
        C = [[0 for _ in range(n + 1)] for _ in range(n)]
        X = [0 for _ in range(n)]

        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j]
            C[i][n] = B[i][0]  # Assuming B is a matrix of shape (n, 1)

        # Creating upper triangular matrix
        for p in range(n - 1):
            for i in range(p + 1, n):
                if C[p][p] == 0:
                    continue  # Avoid division by zero
                multiplier = C[i][p] / C[p][p]
                for j in range(p + 1, n + 1):
                    C[i][j] -= C[p][j] * multiplier

        # Solving the system of equations with upper triangular matrix
        if C[n - 1][n - 1] == 0:
            return None  # No solution if diagonal element is 0
        X[n - 1] = C[n - 1][n] / C[n - 1][n - 1]

        for i in range(n - 2, -1, -1):
            suma = 0
            for j in range(i + 1, n):
                suma += C[i][j] * X[j]
            if C[i][i] == 0:
                return None  # No solution if diagonal element is 0
            X[i] = (C[i][n] - suma) / C[i][i]

        # Zmiana formatu wyjściowego na macierz kolumnową (transponowaną)
        X_transponowana = [[x] for x in X]
        return X_transponowana

    def simple_iteration_method(matrixA, matrixB, tolerance=1e-10, max_iterations=1000):
        A = matrixA.getData()
        B = matrixB.getData()
        n = len(A)
        X = [0 for _ in range(n)]
        X_new = X.copy()

        for _ in range(max_iterations):
            for i in range(n):
                sum_ = B[i][0]
                for j in range(n):
                    if i != j:
                        sum_ -= A[i][j] * X[j]
                X_new[i] = sum_ / A[i][i]

            if all(abs(X_new[i] - X[i]) < tolerance for i in range(n)):
                return X_new
            X = X_new.copy()

        return X # No solution found within max_iterations
    
    def lu_decomposition_doolittle(matrixA):
        A = matrixA.getData()
        n = len(A)
        L = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        U = [[0 for _ in range(n)] for _ in range(n)]

        for j in range(n):
            for i in range(j+1):
                sum_ = sum(L[i][k] * U[k][j] for k in range(i))
                U[i][j] = A[i][j] - sum_

            for i in range(j, n):
                sum_ = sum(L[i][k] * U[k][j] for k in range(j))
                L[i][j] = (A[i][j] - sum_) / U[j][j]

        return L, U
    #4
    def gauss_seidel_method(matrixA, matrixB, tolerance=1e-10, max_iterations=1000):
        A = matrixA.getData()
        B = matrixB.getData()
        n = len(A)
        X = [0 for _ in range(n)]

        for _ in range(max_iterations):
            X_new = X.copy()
            for i in range(n):
                sum_ = B[i][0]
                for j in range(n):
                    if i != j:
                        sum_ -= A[i][j] * X_new[j]
                X_new[i] = sum_ / A[i][i]

            if all(abs(X_new[i] - X[i]) < tolerance for i in range(n)):
                return X_new
            X = X_new.copy()

        return None 
    
    def thomas_algorithm(matrixA, matrixB):
        A = matrixA.getData()
        B = matrixB.getData()
        n = len(A)
        c_ = [0] * n
        d_ = [0] * n
        X = [0] * n

        c_[0] = A[0][1] / A[0][0]
        d_[0] = B[0] / A[0][0]

        for i in range(1, n):
            a = A[i][i-1]
            b = A[i][i]
            c = 0 if i == n-1 else A[i][i+1]
            d = B[i]

            denom = b - a * c_[i-1]
            c_[i] = c / denom if i < n-1 else 0
            d_[i] = (d - a * d_[i-1]) / denom

        X[n-1] = d_[n-1]
        for i in range(n-2, -1, -1):
            X[i] = d_[i] - c_[i] * X[i+1]

        return X
    #5
    def SOR_method(matrixA, matrixB, omega, tol=1e-10, max_iterations=10000):
        A = matrixA.getData()
        B = matrixB.getData()
        n = len(A)
        X = [0 for _ in range(n)]
        X_new = X.copy()

        for iteration in range(max_iterations):
            for i in range(n):
                sum1 = sum(A[i][j] * X_new[j] for j in range(i))
                sum2 = sum(A[i][j] * X[j] for j in range(i + 1, n))
                X_new[i] = (1 - omega) * X[i] + (omega / A[i][i]) * (B[i] - sum1 - sum2)
            
            if all(abs(X_new[i] - X[i]) < tol for i in range(n)):
                return X_new, iteration + 1  # Return solution and iterations
            
            X = X_new.copy()

        return X, max_iterations 