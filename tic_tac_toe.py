import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg="#333333")  # Set a dark background color for the main window

        # Initialize game state
        self.board = [' ' for _ in range(9)]
        self.current_player = "X"  # Player is "X", AI is "O"
        self.game_over = False
        self.buttons = []

        # Create the game board (3x3 grid of buttons)
        for i in range(9):
            button = tk.Button(
                root, 
                text=' ', 
                font=('normal', 20), 
                width=5, 
                height=2, 
                bg='#444444',   # Dark background for buttons
                fg='yellow',    # Yellow text for player marks
                command=lambda i=i: self.on_click(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        # Create reset button
        reset_button = tk.Button(root, text="Reset", command=self.reset_game, bg='#555555', fg='white')  # Reset button with dark theme
        reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

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
        # Minimax algorithm to choose the best move
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        if best_move is not None:
            self.make_move(best_move, 'O')

    def minimax(self, is_maximizing):
        # Check for terminal states
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif ' ' not in self.board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'O'
                    score = self.minimax(False)
                    self.board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'X'
                    score = self.minimax(True)
                    self.board[i] = ' '
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
                return True
        return False

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
