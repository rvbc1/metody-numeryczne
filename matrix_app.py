# matrix_app.py
import tkinter as tk
from matrix_data_manager import MatrixDataManager
from matrix_calculations import Matrix, MatrixCalculations


entry_bg = 'white' 
button_bg = 'grey'  
text_color = 'black'  


class GuiMatrix():
    def __init__(self, frame, rows, columns):
        super().__init__()
        self.frame = frame
        self.entries = []
        self._matrix = Matrix()

    def getRows(self):
        return self._matrix.getRows()
    
    def getColumns(self):
        return self._matrix.getColumns()

    def setMatrixData(self, matrix):
        self._matrix.setData(matrix)
        self._updateSize()
        self._updateEntries()

    def getMatrix(self):
        return self._matrix
    
    def _updateSize(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        entries = []
        for i in range(self._matrix.getRows()):
            row = []
            for j in range(self._matrix.getColumns()):
                entry = tk.Entry(self.frame, width=5, bg=entry_bg, fg=text_color, borderwidth=2)
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            entries.append(row)
        self.entries = entries

    def updateData(self):  
        print(":)")
        rows = len(self.entries)
        columns = len(self.entries[0]) if self.entries else 0


        matrix = []

        for i in range(rows):
            matrix_row = []
            for j in range(columns):
                cell_value = self.entries[i][j].get()
                try:
                    cell_value = float(cell_value)
                except ValueError:
                    cell_value = 0.0  
                matrix_row.append(cell_value)
            matrix.append(matrix_row)

        self.matrix = matrix

    def _updateEntries(self):
        for i, row in enumerate(self._matrix.getData()):
            for j, value in enumerate(row):
                if i < len(self.entries) and j < len(self.entries[i]):
                    self.entries[i][j].insert(0, value)

class MatrixApp(tk.Tk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.title("Matrix Modifier")
        self.geometry("640x480")

        self.center_window( self.winfo_screenwidth() / 4,  self.winfo_screenheight() / 4) 


        self._initWindowElements()

        self.m1 = GuiMatrix(self.matrix_a_frame, 3, 3)
        self.m2 = GuiMatrix(self.matrix_b_frame, 3, 1)

        self.unknowns, matrix_a_data, matrix_b_data = self.data_manager.load_data()
        
        self.m1.setMatrixData(matrix_a_data)
        self.m2.setMatrixData(matrix_b_data)
        self.row_entry.insert(0, str(self.unknowns))
       

    def _initWindowElements(self):
        self.row_label = tk.Label(self, text="Niewiadome:")
        self.row_label.grid(row=0, column=0)
        self.row_entry = tk.Entry(self, width=5, bg=entry_bg, fg=text_color)
        self.row_entry.grid(row=0, column=1)

        self.set_size_btn = tk.Button(self, text="Set Matrix Size", command=self.set_matrix_size, bg=button_bg, fg=text_color)
        self.set_size_btn.grid(row=0, column=2, columnspan=1)

        self.matrix_a_frame = tk.Frame(self) 
        self.matrix_a_frame.grid(row=3, column=0, columnspan=3)

        self.matrix_b_frame = tk.Frame(self) 
        self.matrix_b_frame.grid(row=3, column=4, columnspan=3)

        self.columnconfigure(3, minsize=30)

        self.update_btn = tk.Button(self, text="Update Matrix", command=self.update_matrix, bg=button_bg, fg=text_color)
        self.update_btn.grid(row=4, column=0, columnspan=2)

        self.matrix_label = tk.Label(self, text="Matrix Values: ", fg='grey')
        self.matrix_label.grid(row=5, column=0, columnspan=2)

   



    def center_window(self, width=300, height=200):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def set_matrix_size(self):
        self.unknowns = int(self.row_entry.get())
        self.m1.setMatrixData(self.m1.getMatrix().changeShape(self.unknowns, self.unknowns))
        self.m2.setMatrixData(self.m2.getMatrix().changeShape(self.unknowns, 1))

                    
    def update_matrix(self):
        self.m1.updateData()
        self.m2.updateData()

        self.data_manager.save_data(self.unknowns, self.m1.getMatrix(), self.m2.getMatrix())

        
        values = "\n".join([" ".join(map(lambda x: f"{x:.2f}", row)) for row in self.m1.getMatrix().getData()])
        self.matrix_label.config(text="Matrix Values:\n" + values)

        x = MatrixCalculations.met_gaussa(self.m1.getMatrix(), self.m2.getMatrix())
        print(x)

  

if __name__ == "__main__":
    data_manager = MatrixDataManager('matrix_data.json')
    app = MatrixApp(data_manager)
    app.mainloop()
