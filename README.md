Tic-Tac-Toe
-----------
The player ("X") makes the first move.
The AI ("O") responds using the Minimax algorithm, ensuring it plays optimally every time.
The game checks for a winner or draw after each move.

Snake
-----
Setup:
The snake is initialized with a starting length and position.
"Snake food" is appears randomly on the canvas, avoiding the snake's body.

Movement:
The snake moves continuously in the direction it’s currently facing.
Arrow key presses change the direction.

Collision Detection:
If the snake collides with the walls or itself, the game ends.

Food Consumption:
When the snake's head moves to the food's position, the food is "eaten" and the snake grows longer.

Checkers
--------
Piece Movement: Regular pawns can move forward only, and kings can move in both directions.
Capturing Logic: Pieces can capture diagonally over an opponent's piece.
Chained Captures: A player can capture multiple pieces in a row, if possible.

Features to Expand:
- End Game Conditions: Implement logic to determine the winner, or if no moves are available.
- Difficulty levels for the AI (e.g., easy, medium, hard).
- A move history or notation system.
- Ability to save and load game states.
- Sound effects for moves and captures.
- A timer for each player's turns.
- Improved Move Validation: Handle more complex scenarios and prevent any missed illegal moves more robustly.

