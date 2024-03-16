import tkinter as tk

class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Matrix Modifier")
        self.geometry("300x200")
        
        self.entry_bg = 'white'  # białe tło dla widoczności
        self.button_bg = 'grey'  # szare tło dla przycisku
        self.text_color = 'black'  # czarny tekst dla widoczności

        # Pola do wprowadzania rozmiaru macierzy
        self.row_label = tk.Label(self, text="Rows:")
        self.row_label.grid(row=0, column=0)
        self.row_entry = tk.Entry(self, width=5, bg=self.entry_bg, fg=self.text_color)
        self.row_entry.grid(row=0, column=1)

        self.column_label = tk.Label(self, text="Columns:")
        self.column_label.grid(row=1, column=0)
        self.column_entry = tk.Entry(self, width=5, bg=self.entry_bg, fg=self.text_color)
        self.column_entry.grid(row=1, column=1)

        # Przycisk do ustawiania rozmiaru macierzy
        self.set_size_btn = tk.Button(self, text="Set Matrix Size", command=self.set_matrix_size, bg=self.button_bg, fg=self.text_color)
        self.set_size_btn.grid(row=2, column=0, columnspan=2)

        self.matrix_frame = tk.Frame(self)  # Ramka na macierz
        self.matrix_frame.grid(row=3, column=0, columnspan=2)

        # Przycisk do aktualizacji macierzy
        self.update_btn = tk.Button(self, text="Update Matrix", command=self.update_matrix, bg=self.button_bg, fg=self.text_color)
        self.update_btn.grid(row=4, column=0, columnspan=2)

        self.matrix_label = tk.Label(self, text="Matrix Values: ", fg='grey')
        self.matrix_label.grid(row=5, column=0, columnspan=2)

        self.entries = []

    def set_matrix_size(self):
        rows = int(self.row_entry.get())
        columns = int(self.column_entry.get())
        self.update_array(rows, columns)

    def update_array(self, rows, columns):
        # Usuwamy wszystkie poprzednie Entry z ramki
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        self.entries = []
        for i in range(rows):
            row = []
            for j in range(columns):
                entry = tk.Entry(self.matrix_frame, width=5, bg=self.entry_bg, fg=self.text_color, borderwidth=2)
                entry.grid(row=i, column=j, padx=1, pady=1)  # Dodajemy pady i padx dla odpowiedniej odległości między komórkami
                row.append(entry)
            self.entries.append(row)

    def update_matrix(self):
        values = ""
        for row in self.entries:
            for entry in row:
                values += entry.get() + " "
            values += "\n"
        self.matrix_label.config(text="Matrix Values:\n" + values)

if __name__ == "__main__":
    app = MatrixApp()
    app.mainloop()
