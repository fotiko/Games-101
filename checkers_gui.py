import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

class CheckersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Checkers")
        self.board = []
        self.selected_piece = None
        self.turn = "red"
        self.multi_capture_piece = None
        self.init_board()
        self.create_board_gui()

    def init_board(self):
        self.board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]
        ]

    def create_board_gui(self):
        self.buttons = []
        bold_font = tkfont.Font(weight="bold")
        for i in range(8):
            row = []
            for j in range(8):
                button = tk.Button(self.master, width=5, height=2, command=lambda x=i, y=j: self.on_click(x, y))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.update_board_gui()

    def update_board_gui(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.buttons[i][j].config(bg="white")
                else:
                    self.buttons[i][j].config(bg="black")
                
                if self.board[i][j] == 1:
                    self.buttons[i][j].config(text="R", fg="red")
                elif self.board[i][j] == 2:
                    self.buttons[i][j].config(text="B", fg="blue")
                elif self.board[i][j] == 3:  # Red King
                    self.buttons[i][j].config(text="R", fg="red", font=tkfont.Font(weight="bold"))
                elif self.board[i][j] == 4:  # Black King
                    self.buttons[i][j].config(text="B", fg="blue", font=tkfont.Font(weight="bold"))
                else:
                    self.buttons[i][j].config(text="")

    def on_click(self, row, col):
        if self.selected_piece:
            if self.is_valid_move(self.selected_piece[0], self.selected_piece[1], row, col):
                self.move_piece(self.selected_piece[0], self.selected_piece[1], row, col)
                if not self.multi_capture_piece:
                    self.turn = "black" if self.turn == "red" else "red"
                self.selected_piece = None
                self.update_board_gui()
                if self.check_winner():
                    messagebox.showinfo("Game Over", f"{self.turn.capitalize()} wins!")
                    self.master.quit()
            else:
                self.selected_piece = None
                self.multi_capture_piece = None
        else:
            if ((self.turn == "red" and self.board[row][col] in [1, 3]) or 
                (self.turn == "black" and self.board[row][col] in [2, 4])):
                self.selected_piece = (row, col)

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        if self.board[end_row][end_col] != 0:
            return False

        piece = self.board[start_row][start_col]
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if self.multi_capture_piece and (start_row, start_col) != self.multi_capture_piece:
            return False

        if piece in [1, 2]:  # Regular pieces
            if piece == 1 and row_diff < 0:  # Red moves down
                return False
            if piece == 2 and row_diff > 0:  # Black moves up
                return False

        if abs(row_diff) == 1 and abs(col_diff) == 1:
            return not self.multi_capture_piece
        elif abs(row_diff) == 2 and abs(col_diff) == 2:
            jump_row = (start_row + end_row) // 2
            jump_col = (start_col + end_col) // 2
            jumped_piece = self.board[jump_row][jump_col]
            return (piece in [1, 3] and jumped_piece in [2, 4]) or (piece in [2, 4] and jumped_piece in [1, 3])

        return False

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        
        # Check if the piece becomes a king
        if (piece == 1 and end_row == 7) or (piece == 2 and end_row == 0):
            self.board[end_row][end_col] = piece + 2  # Convert to king (3 for red, 4 for black)
        else:
            self.board[end_row][end_col] = piece

        if abs(end_row - start_row) == 2:
            jump_row = (start_row + end_row) // 2
            jump_col = (start_col + end_col) // 2
            self.board[jump_row][jump_col] = 0

            # Check for multi-capture
            if self.has_further_captures(end_row, end_col):
                self.multi_capture_piece = (end_row, end_col)
            else:
                self.multi_capture_piece = None
        else:
            self.multi_capture_piece = None

    def has_further_captures(self, row, col):
        piece = self.board[row][col]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for d_row, d_col in directions:
            if 0 <= row + 2*d_row < 8 and 0 <= col + 2*d_col < 8:
                if self.is_valid_move(row, col, row + 2*d_row, col + 2*d_col):
                    return True
        return False

    def check_winner(self):
        red_pieces = sum(row.count(1) + row.count(3) for row in self.board)
        black_pieces = sum(row.count(2) + row.count(4) for row in self.board)
        return red_pieces == 0 or black_pieces == 0

if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()