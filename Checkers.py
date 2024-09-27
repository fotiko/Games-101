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
        self.current_turn = 'X'  # X goes first

    def create_board(self):
        # Create an 8x8 board with initial positions of pieces
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

    def display_board(self):
        print("  0 1 2 3 4 5 6 7")
        print(" +----------------")
        for row in range(8):
            print(f"{row}|", end=' ')
            for col in range(8):
                piece = self.board[row][col]
                print(piece if piece else '.', end=' ')
            print()

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        # Basic movement validation
        if not piece or piece.color != self.current_turn:
            print("Invalid move: not your piece.")
            return False

        if self.board[end_row][end_col] is not None:
            print("Invalid move: destination occupied.")
            return False

        direction = 1 if piece.color == 'X' else -1
        is_valid_simple_move = (
            abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1
        )

        # Check for captures
        is_valid_capture = (
            abs(start_row - end_row) == 2
            and abs(start_col - end_col) == 2
            and self.board[(start_row + end_row) // 2][(start_col + end_col) // 2]
            and self.board[(start_row + end_row) // 2][(start_col + end_col) // 2].color != piece.color
        )

        if not (is_valid_simple_move or is_valid_capture):
            print("Invalid move.")
            return False

        # Perform move
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece

        # Perform capture if valid
        if is_valid_capture:
            captured_row, captured_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            self.board[captured_row][captured_col] = None

        # Check if piece becomes a king
        if (piece.color == 'X' and end_row == 7) or (piece.color == 'O' and end_row == 0):
            piece.make_king()

        return True

    def switch_turn(self):
        self.current_turn = 'O' if self.current_turn == 'X' else 'X'

    def play(self):
        while True:
            self.display_board()
            print(f"Player {self.current_turn}'s turn.")
            try:
                start = tuple(map(int, input("Enter the start position (row col): ").split()))
                end = tuple(map(int, input("Enter the end position (row col): ").split()))
            except ValueError:
                print("Invalid input, please enter row and column as numbers.")
                continue

            if self.move_piece(start, end):
                self.switch_turn()


if __name__ == "__main__":
    game = CheckersGame()
    game.play()
