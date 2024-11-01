from solver import SudokuSolver
from sudoku_grid import SudokuGrid

def main():
    grid = SudokuGrid()
    grid.load_grid('sudoku.txt')
    
    solver = SudokuSolver(grid)
    solver.solve()

if __name__ == "__main__":
    main()
