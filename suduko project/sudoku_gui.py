import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sudoku_solver import SudokuSolver
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Sudoku Solver Pro")
        self.root.geometry("650x750")
        self.root.configure(bg="#f0f2f5")
        self.solver = SudokuSolver()
        
        # Sample puzzles
        self.sample_puzzles = [
            # Easy
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ],
            # Medium
            [
                [0, 0, 0, 2, 6, 0, 7, 0, 1],
                [6, 8, 0, 0, 7, 0, 0, 9, 0],
                [1, 9, 0, 0, 0, 4, 5, 0, 0],
                [8, 2, 0, 1, 0, 0, 0, 4, 0],
                [0, 0, 4, 6, 0, 2, 9, 0, 0],
                [0, 5, 0, 0, 0, 3, 0, 2, 8],
                [0, 0, 9, 3, 0, 0, 0, 7, 4],
                [0, 4, 0, 0, 5, 0, 0, 3, 6],
                [7, 0, 3, 0, 1, 8, 0, 0, 0]
            ],
            # Hard
            [
                [0, 0, 0, 6, 0, 0, 4, 0, 0],
                [7, 0, 0, 0, 0, 3, 6, 0, 0],
                [0, 0, 0, 0, 9, 1, 0, 8, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 0, 1, 8, 0, 0, 0, 3],
                [0, 0, 0, 3, 0, 6, 0, 4, 5],
                [0, 4, 0, 2, 0, 0, 0, 6, 0],
                [9, 0, 3, 0, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 1, 0, 0]
            ],
            # Expert
            [
                [0, 0, 0, 0, 0, 0, 6, 8, 0],
                [0, 0, 0, 0, 7, 3, 0, 0, 9],
                [3, 0, 9, 0, 0, 0, 0, 4, 5],
                [4, 9, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 3, 0, 5, 0, 9, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 3, 6],
                [9, 6, 0, 0, 0, 0, 3, 0, 8],
                [7, 0, 0, 6, 8, 0, 0, 0, 0],
                [0, 2, 8, 0, 0, 0, 0, 0, 0]
            ],
            # Empty
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        ]
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#4a6fa5", height=80)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text="SUDOKU SOLVER PRO",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        ).pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=10)
        main_container.pack(fill="both", expand=True)
        
        # Sudoku grid frame
        grid_frame = tk.Frame(main_container, bg="#4a6fa5", padx=5, pady=5)
        grid_frame.pack()
        
        # Create Sudoku grid
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Entry(
                    grid_frame,
                    width=2,
                    font=("Arial", 24),
                    justify="center",
                    bg="white",
                    relief="solid",
                    borderwidth=1,
                    fg="#333333",
                    highlightthickness=0
                )
                cell.grid(row=i, column=j, ipadx=5, ipady=5)
                
                # Add thicker borders for 3x3 boxes
                if i % 3 == 0:
                    cell.grid(pady=(3, 0))
                if j % 3 == 0:
                    cell.grid(padx=(3, 0))
                
                cell.bind("<FocusIn>", lambda e, i=i, j=j: self.highlight_cells(i, j))
                row.append(cell)
            self.cells.append(row)
        
        # Control buttons
        btn_frame = tk.Frame(main_container, bg="#f0f2f5", pady=15)
        btn_frame.pack()
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=6)
        
        ttk.Button(
            btn_frame,
            text="Solve (Backtracking)",
            command=lambda: self.solve("backtracking"),
            style="TButton"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Solve (Brute Force)",
            command=lambda: self.solve("bruteforce"),
            style="TButton"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_grid,
            style="TButton"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Load Image",
            command=self.load_image,
            style="TButton"
        ).pack(side="left", padx=5)
        
        # Sample puzzles dropdown
        sample_frame = tk.Frame(main_container, bg="#f0f2f5")
        sample_frame.pack(pady=(10, 0))
        
        tk.Label(
            sample_frame,
            text="Sample Puzzles:",
            font=("Arial", 10),
            bg="#f0f2f5"
        ).pack(side="left")
        
        self.puzzle_var = tk.StringVar()
        self.puzzle_var.set("Select Difficulty")
        
        puzzle_menu = ttk.OptionMenu(
            sample_frame,
            self.puzzle_var,
            "Select Difficulty",
            "Easy", "Medium", "Hard", "Expert", "Empty",
            command=self.load_sample
        )
        puzzle_menu.pack(side="left", padx=5)
        
        # Status label
        self.status_label = tk.Label(
            main_container,
            text="",
            font=("Arial", 12),
            bg="#f0f2f5",
            fg="#4a6fa5"
        )
        self.status_label.pack(pady=10)
        
        # Footer
        footer = tk.Frame(self.root, bg="#4a6fa5", height=40)
        footer.pack(fill="x", side="bottom")
        
        tk.Label(
            footer,
            text="Rajan Rajput @copyright reseverd DAA project",
            font=("Arial", 8),
            fg="white",
            bg="#4a6fa5"
        ).pack(pady=10)
    
    def highlight_cells(self, row, col):
        """Highlight related cells (row, column, and 3x3 box)"""
        # Reset all cells first
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(bg="white", fg="#333333")
        
        # Highlight current cell
        self.cells[row][col].config(bg="#e6f3ff")
        
        # Highlight row and column
        for i in range(9):
            self.cells[row][i].config(bg="#f0f7ff")
            self.cells[i][col].config(bg="#f0f7ff")
        
        # Highlight 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                self.cells[box_row + i][box_col + j].config(bg="#f0f7ff")
        
        # Re-highlight current cell
        self.cells[row][col].config(bg="#e6f3ff")
    
    def get_grid(self):
        """Get current grid values from GUI"""
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].get()
                row.append(int(val) if val.isdigit() and 1 <= int(val) <= 9 else 0)
            grid.append(row)
        return grid
    
    def set_grid(self, grid):
        """Update GUI with grid values"""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.cells[i][j].insert(0, str(grid[i][j]))
    
    def clear_grid(self):
        """Clear the entire grid"""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(bg="white", fg="#333333")
        self.status_label.config(text="")
    
    def solve(self, algorithm):
        """Solve the current puzzle"""
        grid = self.get_grid()
        solution = self.solver.solve(grid, algorithm)
        
        if solution:
            self.set_grid(solution)
            # Color the solved cells
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:  # Only color cells that were empty
                        self.cells[i][j].config(fg="#4a6fa5")
            self.status_label.config(
                text=f"Solved with {algorithm} in {self.solver.solving_time:.4f} seconds",
                fg="#2e7d32"  # Green
            )
        else:
            messagebox.showerror("Error", "No solution exists for this puzzle")
            self.status_label.config(text="No solution exists", fg="#d32f2f")  # Red
    
    def load_image(self):
        """Load Sudoku puzzle from image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            grid = self.solver.read_from_image(file_path)
            if grid:
                self.clear_grid()
                self.set_grid(grid)
                self.status_label.config(text="Puzzle loaded from image", fg="#4a6fa5")
            else:
                messagebox.showerror("Error", "Could not read Sudoku from image")
    
    def load_sample(self, difficulty):
        """Load a sample puzzle"""
        difficulties = {
            "Easy": 0,
            "Medium": 1,
            "Hard": 2,
            "Expert": 3,
            "Empty": 4
        }
        idx = difficulties.get(difficulty, 0)
        self.clear_grid()
        self.set_grid(self.sample_puzzles[idx])
        self.status_label.config(text=f"Loaded {difficulty} puzzle", fg="#4a6fa5")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()