# matrix_data_manager.py
import json

class MatrixDataManager:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
            return data.get('unknowns'), data.get('matrix_a'), data.get('matrix_b')
        except:
            return 3, [['' for _ in range(3)] for _ in range(3)], [['' for _ in range(1)] for _ in range(3)]  

    def save_data(self, unknowns, matrix_a, matrix_b):
        data = {
            'unknowns': unknowns,
            'matrix_a': matrix_a,
            'matrix_b': matrix_b
        }
        with open(self.filepath, 'w') as file:
            file.write('{\n')
            file.write('    "unknowns": ' + str(unknowns) + ',\n')
            file.write('    "matrix_a": [\n')
            for row in matrix_a[:-1]:
                file.write('        ' + json.dumps(row) + ',\n')
            file.write('        ' + json.dumps(matrix_a[-1]) + '\n')
            file.write('    ],\n')
            file.write('    "matrix_b": [\n')
            for row in matrix_b[:-1]:
                file.write('        ' + json.dumps(row) + ',\n')
            file.write('        ' + json.dumps(matrix_b[-1]) + '\n')
            file.write('    ]\n')
            file.write('}\n')
