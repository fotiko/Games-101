import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        # Initialize game state
        self.board = [' ' for _ in range(9)]
        self.current_player = "X"  # Player is "X", AI is "O"
        self.game_over = False
        self.buttons = []
        self.difficulty = StringVar(root)
        self.difficulty.set("Easy")  # Default difficulty level

        # Create difficulty dropdown
        difficulty_menu = OptionMenu(root, self.difficulty, "Easy", "Medium", "Hard")
        difficulty_menu.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Create the game board (3x3 grid of buttons)
        for i in range(9):
            button = tk.Button(root, text=' ', font=('normal', 20), width=5, height=2, command=lambda i=i: self.on_click(i))
            button.grid(row=(i // 3) + 1, column=i % 3)
            self.buttons.append(button)

        # Create reset button
        reset_button = tk.Button(root, text="Reset", command=self.reset_game)
        reset_button.grid(row=4, column=0, columnspan=3, sticky="nsew")

    def on_click(self, index):
        if self.board[index] == ' ' and not self.game_over:
            # Player move
            self.make_move(index, self.current_player)
            if not self.game_over:
                self.ai_move()  # AI makes a move after the player

    def make_move(self, index, player):
        if self.board[index] == ' ':
            self.board[index] = player
            self.buttons[index].config(text=player)

            # Check if current move wins the game
            if self.check_winner(player):
                self.game_over = True
                messagebox.showinfo("Game Over", f"Player {player} wins!")
            elif ' ' not in self.board:  # Check for a draw
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a draw!")

            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def ai_move(self):
        difficulty = self.difficulty.get()

        if difficulty == "Easy":
            self.ai_easy()
        elif difficulty == "Medium":
            self.ai_medium()
        elif difficulty == "Hard":
            self.ai_hard()

    def ai_easy(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == ' ']
        if available_moves:
            move = random.choice(available_moves)
            self.make_move(move, 'O')

    def ai_medium(self):
        # Block the player's winning move if possible
        for move in range(9):
            if self.board[move] == ' ':
                self.board[move] = 'X'
                if self.check_winner('X'):
                    self.board[move] = 'O'
                    self.buttons[move].config(text='O')
                    return
                self.board[move] = ' '

        # Otherwise make a random move (same as easy)
        self.ai_easy()

    def ai_hard(self):
        # Minimax algorithm for optimal play
        best_score = float('-inf')
        best_move = None
        for move in range(9):
            if self.board[move] == ' ':
                self.board[move] = 'O'
                score = self.minimax(False)
                self.board[move] = ' '
                if score > best_score:
                    best_score = score
                    best_move = move

        if best_move is not None:
            self.make_move(best_move, 'O')

    def minimax(self, is_maximizing):
        winner = self.check_winner('O') or self.check_winner('X')
        if winner:
            return 1 if winner == 'O' else -1
        elif ' ' not in self.board:  # Draw
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in range(9):
                if self.board[move] == ' ':
                    self.board[move] = 'O'
                    score = self.minimax(False)
                    self.board[move] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in range(9):
                if self.board[move] == ' ':
                    self.board[move] = 'X'
                    score = self.minimax(True)
                    self.board[move] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for combination in win_combinations:
            if all(self.board[i] == player for i in combination):
                return player
        return None

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = "X"
        self.game_over = False
        for button in self.buttons:
            button.config(text=' ')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
