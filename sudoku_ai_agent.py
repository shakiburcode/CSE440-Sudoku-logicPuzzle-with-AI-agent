import tkinter as tk
from tkinter import messagebox
# ==== AI SUDOKU AGENT ====
class SudokuAgent:
    def __init__(self, board):
        self.board = board
        self.domains = {
            (r, c): {board[r][c]} if board[r][c] != 0 else set(range(1, 10))
            for r in range(9) for c in range(9)
        }

    def is_valid(self, r, c, val):
        for i in range(9):
            if self.board[r][i] == val or self.board[i][c] == val:
                return False
        box_r, box_c = r // 3 * 3, c // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.board[box_r + i][box_c + j] == val:
                    return False
        return True

    def select_unassigned_variable(self):
        unassigned = [(len(self.domains[(r, c)]), r, c)
                      for r in range(9) for c in range(9)
                      if self.board[r][c] == 0]
        if not unassigned:
            return None, None
        _, r, c = min(unassigned)
        return r, c

    def forward_checking(self, r, c, val):
        changes = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and (i == r or j == c or (i // 3 == r // 3 and j // 3 == c // 3)):
                    if val in self.domains[(i, j)]:
                        self.domains[(i, j)].remove(val)
                        changes.append((i, j, val))
                        if not self.domains[(i, j)]:
                            return False, changes
        return True, changes

    def restore_domains(self, changes):
        for r, c, val in changes:
            self.domains[(r, c)].add(val)

    def solve(self):
        r, c = self.select_unassigned_variable()
        if r is None:
            return True

        for val in sorted(self.domains[(r, c)]):
            if self.is_valid(r, c, val):
                self.board[r][c] = val
                saved_domain = self.domains[(r, c)].copy()
                self.domains[(r, c)] = {val}

                ok, changes = self.forward_checking(r, c, val)
                if ok and self.solve():
                    return True

                self.restore_domains(changes)
                self.domains[(r, c)] = saved_domain
                self.board[r][c] = 0
        return False

# ==== GUI SETUP ====
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Sudoku Solver")
        self.entries = []

        for r in range(9):
            row_entries = []
            for c in range(9):
                entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=r, column=c, padx=1, pady=1)
                row_entries.append(entry)
            self.entries.append(row_entries)

        solve_button = tk.Button(root, text="Solve", command=self.solve, font=("Arial", 14), bg="lightgreen")
        solve_button.grid(row=9, column=0, columnspan=9, sticky="we")

        # Load an example puzzle
        self.load_example()

    def get_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.entries[r][c].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def update_board(self, board):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    self.entries[r][c].insert(0, str(board[r][c]))

    def load_example(self):
        example = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.update_board(example)

    def solve(self):
        board = self.get_board()
        agent = SudokuAgent(board)
        if agent.solve():
            self.update_board(agent.board)
        else:
            messagebox.showerror("Error", "No solution found!")

# ==== RUN THE GUI ====
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
