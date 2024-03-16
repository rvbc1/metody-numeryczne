# matrix_app.py
import tkinter as tk
from matrix_data_manager import MatrixDataManager
from matrix_calculations import MatrixCalculations

class MatrixApp(tk.Tk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.title("Matrix Modifier")
        self.geometry("640x480")

        self.center_window( self.winfo_screenwidth() / 4,  self.winfo_screenheight() / 4) 

        self.entry_bg = 'white'  # białe tło dla widoczności
        self.button_bg = 'grey'  # szare tło dla przycisku
        self.text_color = 'black'  # czarny tekst dla widoczności

        # Pola do wprowadzania rozmiaru macierzy
        self.row_label = tk.Label(self, text="Niewiadome:")
        self.row_label.grid(row=0, column=0)
        self.row_entry = tk.Entry(self, width=5, bg=self.entry_bg, fg=self.text_color)
        self.row_entry.grid(row=0, column=1)


        # Przycisk do ustawiania rozmiaru macierzy
        self.set_size_btn = tk.Button(self, text="Set Matrix Size", command=self.set_matrix_size, bg=self.button_bg, fg=self.text_color)
        self.set_size_btn.grid(row=0, column=2, columnspan=1)

        self.matrix_a_frame = tk.Frame(self)  # Ramka na macierz a
        self.matrix_a_frame.grid(row=3, column=0, columnspan=3)

        self.matrix_b_frame = tk.Frame(self)  # Ramka na macierz b
        self.matrix_b_frame.grid(row=3, column=4, columnspan=3)

        self.columnconfigure(3, minsize=30)

        # Przycisk do aktualizacji macierzy
        self.update_btn = tk.Button(self, text="Update Matrix", command=self.update_matrix, bg=self.button_bg, fg=self.text_color)
        self.update_btn.grid(row=4, column=0, columnspan=2)

        self.matrix_label = tk.Label(self, text="Matrix Values: ", fg='grey')
        self.matrix_label.grid(row=5, column=0, columnspan=2)

        self.entries = []
        self.entries2 = []

        # Ładowanie danych z pliku przy starcie
        rows, columns, matrix_a_data, matrix_b_data = self.data_manager.load_data()
        self.row_entry.insert(0, str(rows))
        # self.column_entry.insert(0, str(columns))
        self.set_matrix_size()  # Ustaw rozmiar macierzy
        self.fill_matrix(matrix_a_data, self.entries)  # Wypełnij macierz danymi
        self.fill_matrix(matrix_b_data, self.entries2)  # Wypełnij macierz danymi

    def center_window(self, width=300, height=200):
        # Obliczenie współrzędnych środka ekranu
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Obliczenie położenia okna, aby znalazło się na środku ekranu
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def set_matrix_size(self):
        rows = int(self.row_entry.get())
        columns = int(self.row_entry.get())
        self.update_array(rows, columns, self.matrix_a_frame, self.entries)
        self.update_array(1, 1, self.matrix_b_frame, self.entries2)

    def update_array(self, rows, columns, frame, entries2):
        # Usuwamy wszystkie poprzednie Entry z ramki
        for widget in frame.winfo_children():
            widget.destroy()

        entries2 = []
        for i in range(rows):
            row = []
            for j in range(columns):
                entry = tk.Entry(self.matrix_a_frame, width=5, bg=self.entry_bg, fg=self.text_color, borderwidth=2)
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            entries2.append(row)


    def fill_matrix(self, matrix_data, entries2):
        for i, row in enumerate(matrix_data):
            for j, value in enumerate(row):
                if i < len(entries2) and j < len(entries2[i]):
                    entries2[i][j].insert(0, value)


    # def update_matrix(self):
    #     rows = len(self.entries)
    #     columns = len(self.entries[0]) if self.entries else 0
    #     # Zamiana pustych pól na zera
    #     matrix = [[self.entries[i][j].get() if self.entries[i][j].get() != '' else '0' for j in range(columns)] for i in range(rows)] if self.entries else []
    #     self.data_manager.save_data(rows, columns, matrix)
    #     values = "\n".join([" ".join(str(cell) if cell != '' else '0' for cell in row) for row in matrix])
    #     self.matrix_label.config(text="Matrix Values:\n" + values)
                    
    def update_matrix(self):
        rows = len(self.entries)
        columns = len(self.entries[0]) if self.entries else 0
        matrix = []

        matrix2 = []

        for i in range(rows):
            matrix_row = []
            for j in range(columns):
                cell_value = self.entries[i][j].get()
                # Próba konwersji wartości komórki na liczbę zmiennoprzecinkową
                try:
                    cell_value = float(cell_value)
                except ValueError:
                    cell_value = 0.0  # Ustawiamy 0.0 jeśli konwersja nie powiedzie się
                matrix_row.append(cell_value)
            matrix.append(matrix_row)

        for i in range(rows):
            matrix_row = []
            cell_value = self.entries2[0][0].get()
            # Próba konwersji wartości komórki na liczbę zmiennoprzecinkową
            try:
                cell_value = float(cell_value)
            except ValueError:
                cell_value = 0.0  # Ustawiamy 0.0 jeśli konwersja nie powiedzie się
            matrix_row.append(cell_value)
        matrix2.append(matrix_row)


        # Zapisywanie do pliku JSON (nadpisujemy funkcję save_data, aby obsługiwała liczby całkowite)
        self.data_manager.save_data(rows, columns, matrix, matrix2)

        # Aktualizowanie etykiety z wartościami macierzy
        norm = MatrixCalculations().normalize(matrix)
        values = "\n".join([" ".join(map(lambda x: f"{x:.2f}", row)) for row in norm])
        self.matrix_label.config(text="Matrix Values:\n" + values)

  

if __name__ == "__main__":
    data_manager = MatrixDataManager('matrix_data.json')
    app = MatrixApp(data_manager)
    app.mainloop()
