import json

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
