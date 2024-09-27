import tkinter as tk
from tkinter import messagebox
import random


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def make_king(self):
        self.king = True

    def __repr__(self):
        return f"{self.color}{'K' if self.king else ''}"


class CheckersGame:
    def __init__(self):
        self.board = self.create_board()
        self.current_turn = 'X'  # X starts the game
        self.selected_piece = None
        self.valid_moves = []
        self.chain_capture = False
        self.move_history = []
        self.vs_ai = False
        self.ai_difficulty = 'Easy'

    def create_board(self):
        board = [[None] * 8 for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = Piece('O')
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = Piece('X')
        return board

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        if self.board[end_row][end_col] is not None:
            return False

        is_valid_simple_move = (
            abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1
        )

        is_valid_capture = (
            abs(start_row - end_row) == 2
            and abs(start_col - end_col) == 2
            and self.board[(start_row + end_row) // 2][(start_col + end_col) // 2]
            and self.board[(start_row + end_row) // 2][(start_col + end_col) // 2].color != piece.color
        )

        return is_valid_simple_move or is_valid_capture

    def get_valid_moves(self, piece_pos):
        row, col = piece_pos
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.is_valid_move((row, col), (r, c)):
                moves.append((r, c))

            # Check for captures
            r, c = row + 2 * dr, col + 2 * dc
            if 0 <= r < 8 and 0 <= c < 8 and self.is_valid_move((row, col), (r, c)):
                moves.append((r, c))
        return moves

    def get_capture_moves(self, piece_pos):
        row, col = piece_pos
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + 2 * dr, col + 2 * dc
            if 0 <= r < 8 and 0 <= c < 8 and self.is_valid_move((row, col), (r, c)):
                moves.append((r, c))
        return moves

    def switch_turn(self):
        self.current_turn = 'O' if self.current_turn == 'X' else 'X'


class CheckersGUI:
    def __init__(self, root):
        self.game = CheckersGame()
        self.root = root
        self.root.title("Checkers Game")
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.click)
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Play vs AI", command=self.play_vs_ai)
        game_menu.add_command(label="Play vs Player", command=self.play_vs_player)
        game_menu.add_command(label="Quit", command=self.root.quit)

        difficulty_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="AI Difficulty", menu=difficulty_menu)
        difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty('Easy'))
        difficulty_menu.add_command(label="Medium", command=lambda: self.set_difficulty('Medium'))
        difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty('Hard'))

    def set_difficulty(self, level):
        self.game.ai_difficulty = level
        messagebox.showinfo("AI Difficulty", f"Difficulty set to {level}")

    def new_game(self):
        self.game = CheckersGame()
        self.draw_board()

    def play_vs_ai(self):
        self.new_game()
        self.game.vs_ai = True
        self.draw_board()

    def play_vs_player(self):
        self.new_game()
        self.game.vs_ai = False
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color
                )

                piece = self.game.board[row][col]
                if piece:
                    x = col * 50 + 25
                    y = row * 50 + 25
                    piece_color = "red" if piece.color == "O" else "black"
                    self.canvas.create_oval(
                        x - 20, y - 20, x + 20, y + 20, fill=piece_color
                    )

                    if piece.king:
                        self.canvas.create_text(x, y, text="K", fill="yellow")

        # Highlight valid moves
        if self.game.selected_piece:
            for move in self.game.valid_moves:
                row, col = move
                self.canvas.create_rectangle(
                    col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, outline="green", width=3
                )

    def click(self, event):
        col, row = event.x // 50, event.y // 50
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        piece = self.game.board[row][col]

        if piece and piece.color == self.game.current_turn and not self.game.chain_capture:
            self.game.selected_piece = (row, col)
            self.game.valid_moves = self.game.get_valid_moves((row, col))

        elif self.game.selected_piece:
            start = self.game.selected_piece
            end = (row, col)

            if end in self.game.valid_moves:
                self.move_piece(start, end)

                if abs(start[0] - end[0]) == 2:
                    if self.game.get_capture_moves(end):
                        self.game.selected_piece = end
                        self.game.valid_moves = self.game.get_capture_moves(end)
                        self.game.chain_capture = True
                    else:
                        self.end_turn()
                else:
                    self.end_turn()

        self.draw_board()

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.game.board[start_row][start_col]

        self.game.board[start_row][start_col] = None
        self.game.board[end_row][end_col] = piece

        if abs(start_row - end_row) == 2:
            capture_row = (start_row + end_row) // 2
            capture_col = (start_col + end_col) // 2
            self.game.board[capture_row][capture_col] = None

        # King the piece if it reaches the last row
        if (piece.color == 'X' and end_row == 0) or (piece.color == 'O' and end_row == 7):
            piece.make_king()

    def end_turn(self):
        self.game.chain_capture = False
        self.game.selected_piece = None
        self.game.valid_moves = []
        self.game.switch_turn()

        # If AI is playing and it's AI's turn
        if self.game.vs_ai and self.game.current_turn == 'O':
            self.ai_move()

    def ai_move(self):
        difficulty = self.game.ai_difficulty
        moves = self.get_all_valid_moves('O')

        if difficulty == 'Easy':
            move = random.choice(moves)
        elif difficulty == 'Medium':
            move = self.get_best_move(moves)
        else:  # Hard
            move = self.get_best_move(moves, hard=True)

        self.move_piece(move[0], move[1])
        self.end_turn()

    def get_all_valid_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]
                if piece and piece.color == color:
                    valid_moves = self.game.get_valid_moves((row, col))
                    for move in valid_moves:
                        moves.append(((row, col), move))
        return moves

    def get_best_move(self, moves, hard=False):
        capture_moves = [move for move in moves if abs(move[0][0] - move[1][0]) == 2]
        if capture_moves:
            return random.choice(capture_moves)
        return random.choice(moves) if not hard else self.minimax_choice(moves)

    def minimax_choice(self, moves):
        # Placeholder for a more sophisticated AI strategy (like minimax)
        return random.choice(moves)


root = tk.Tk()
app = CheckersGUI(root)
root.mainloop()
