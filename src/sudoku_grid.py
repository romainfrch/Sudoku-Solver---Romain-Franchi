class SudokuGrid:
    _instance = None

    def get_all_empty_cells(self):
        empty_cells = [i for i, value in enumerate(self.grid) if value == 0]
        return empty_cells
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SudokuGrid, cls).__new__(cls)
            cls._instance.grid = [0] * 81
        return cls._instance

    def load_grid(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read().strip().replace(',', ' ').split()
                self.grid = [int(x) for x in content]
                self.grid = [value if value != -1 else 0 for value in self.grid]
        except FileNotFoundError:
            print("Le fichier n'a pas été trouvé.")

    def set_value(self, index, value):
        if self.is_valid_move(index, value):
            self.grid[index] = value
            return True
        else:
            return False

    def is_valid_move(self, index, value):
        row, col = index // 9, index % 9
        for i in range(9):
            if self.grid[row * 9 + i] == value or self.grid[i * 9 + col] == value:
                return False
        box_start = (row // 3) * 27 + (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[box_start + i * 9 + j] == value:
                    return False
        return True

    def is_grid_full(self):
        return 0 not in self.grid

    def display_grid(self):
        for i in range(9):
            row_display = []
            for value in self.grid[i * 9:(i + 1) * 9]:
                row_display.append(str(value) if value != 0 else "0")
            print(" ".join(row_display))

    def display_grid_with_highlight(self, highlighted_index):
        for i in range(9):
            row_display = []
            for j in range(9):
                index = i * 9 + j
                if index == highlighted_index:
                    row_display.append("\033[92;5m?\033[0m")
                else:
                    row_display.append(str(self.grid[index]) if self.grid[index] != 0 else "0")
            print(" ".join(row_display))

    def get_empty_cell(self):
        for i, value in enumerate(self.grid):
            if value == 0:
                return i
        return None
