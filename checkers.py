import tkinter as tk
from tkinter import messagebox
import random

class CheckersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Checkers")
        self.board = []
        self.selected_piece = None
        self.turn = "red"
        self.multi_capture_piece = None
        self.square_size = 60
        self.piece_margin = 5
        self.ai_mode = False
        self.create_menu()
        self.init_board()
        self.create_board_gui()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Play vs AI", command=self.start_ai_game)
        game_menu.add_separator()
        game_menu.add_command(label="Quit", command=self.master.quit)

    def new_game(self):
        self.ai_mode = False
        self.init_board()
        self.turn = "red"
        self.selected_piece = None
        self.multi_capture_piece = None
        self.draw_pieces()

    def start_ai_game(self):
        self.new_game()
        self.ai_mode = True
        messagebox.showinfo("AI Game", "You are playing as Red. \nThe AI will play as White.")

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
        self.canvas = tk.Canvas(self.master, width=self.square_size*8, height=self.square_size*8)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "tan" if (row + col) % 2 == 0 else "brown"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                piece = self.board[row][col]
                if piece != 0:
                    color = "red" if piece in [1, 3] else "white"
                    outline_color = "white" if piece in [1, 3] else "black"
                    self.canvas.create_oval(
                        x - self.square_size//2 + self.piece_margin,
                        y - self.square_size//2 + self.piece_margin,
                        x + self.square_size//2 - self.piece_margin,
                        y + self.square_size//2 - self.piece_margin,
                        fill=color, outline=outline_color, width=2, tags="piece"
                    )
                    if piece in [3, 4]:  # King
                        self.canvas.create_text(x, y, text="K", fill=outline_color, font=("Arial", 24, "bold"), tags="piece")

    def on_canvas_click(self, event):
        if self.ai_mode and self.turn == "black":
            return  # Prevent player from moving during AI's turn
        col = event.x // self.square_size
        row = event.y // self.square_size
        self.on_click(row, col)

    def on_click(self, row, col):
        if self.selected_piece:
            if self.is_valid_move(self.selected_piece[0], self.selected_piece[1], row, col):
                self.move_piece(self.selected_piece[0], self.selected_piece[1], row, col)
                if not self.multi_capture_piece:
                    self.turn = "black" if self.turn == "red" else "red"
                    if self.ai_mode and self.turn == "black":
                        self.master.after(500, self.ai_move)  # Delay AI move for better visualization
                self.selected_piece = None
                self.draw_pieces()
                if self.check_winner():
                    messagebox.showinfo("Game Over", f"{self.turn.capitalize()} wins!")
                    self.new_game()
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

    def ai_move(self):
        valid_moves = self.get_all_valid_moves("black")
        if valid_moves:
            start, end = random.choice(valid_moves)
            self.move_piece(start[0], start[1], end[0], end[1])
            self.turn = "red"
            self.draw_pieces()
            if self.check_winner():
                messagebox.showinfo("Game Over", "White (AI) wins!")
                self.new_game()

    def get_all_valid_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                if (color == "red" and self.board[row][col] in [1, 3]) or \
                   (color == "black" and self.board[row][col] in [2, 4]):
                    for end_row in range(8):
                        for end_col in range(8):
                            if self.is_valid_move(row, col, end_row, end_col):
                                moves.append(((row, col), (end_row, end_col)))
        return moves

if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()
