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

    def met_gaussa(matrixA, matrixB):
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

        return X
