import tkinter as tk
import random

# Constants for the game
GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_SIZE = 20
SNAKE_SPEED = 100  # Milliseconds delay for movement
FOOD_COLOR = "#FF4500"
SNAKE_COLOR = "#00FF00"
BACKGROUND_COLOR = "#1E1E1E"
WALL_COLOR = "#FFFFFF"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        # Create the canvas for the game
        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.canvas.pack()

        # Draw visible walls
        self.canvas.create_rectangle(0, 0, GAME_WIDTH, SNAKE_SIZE, fill=WALL_COLOR, outline=WALL_COLOR)  # Top wall
        self.canvas.create_rectangle(0, 0, SNAKE_SIZE, GAME_HEIGHT, fill=WALL_COLOR, outline=WALL_COLOR)  # Left wall
        self.canvas.create_rectangle(0, GAME_HEIGHT - SNAKE_SIZE, GAME_WIDTH, GAME_HEIGHT, fill=WALL_COLOR, outline=WALL_COLOR)  # Bottom wall
        self.canvas.create_rectangle(GAME_WIDTH - SNAKE_SIZE, 0, GAME_WIDTH, GAME_HEIGHT, fill=WALL_COLOR, outline=WALL_COLOR)  # Right wall

        # Initialize game state
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake coordinates
        self.snake_direction = 'Right'
        self.food_position = None
        self.food = None
        self.game_over = False

        # Draw the initial snake
        self.draw_snake()
        # Place the first food
        self.create_food()

        # Bind the arrow keys to control the snake
        self.root.bind("<KeyPress>", self.change_direction)

        # Start the game loop
        self.move_snake()

    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=SNAKE_COLOR, tag="snake")

    def create_food(self):
        """Create a single food item on the canvas after the previous one is eaten."""
        if self.food:
            self.canvas.delete(self.food)

        while True:
            x = random.randint(1, (GAME_WIDTH // SNAKE_SIZE) - 2) * SNAKE_SIZE
            y = random.randint(1, (GAME_HEIGHT // SNAKE_SIZE) - 2) * SNAKE_SIZE
            if (x, y) not in self.snake:
                self.food_position = (x, y)
                self.food = self.canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR, tag="food")
                break

    def change_direction(self, event):
        """Change the direction of the snake based on arrow key presses."""
        new_direction = event.keysym
        all_directions = ['Up', 'Down', 'Left', 'Right']
        opposites = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}

        if new_direction in all_directions and new_direction != opposites[self.snake_direction]:
            self.snake_direction = new_direction

    def move_snake(self):
        """Move the snake in the current direction and handle collisions."""
        if self.game_over:
            return

        # Get the current head position
        head_x, head_y = self.snake[0]

        # Calculate new head position based on direction
        if self.snake_direction == 'Up':
            head_y -= SNAKE_SIZE
        elif self.snake_direction == 'Down':
            head_y += SNAKE_SIZE
        elif self.snake_direction == 'Left':
            head_x -= SNAKE_SIZE
        elif self.snake_direction == 'Right':
            head_x += SNAKE_SIZE

        # Create new head position
        new_head = (head_x, head_y)

        # Check for collisions with the walls or itself
        if (
            head_x < SNAKE_SIZE or head_x >= GAME_WIDTH - SNAKE_SIZE or
            head_y < SNAKE_SIZE or head_y >= GAME_HEIGHT - SNAKE_SIZE or
            new_head in self.snake
        ):
            self.end_game()
            return

        # Insert the new head and remove the tail (unless food is eaten)
        self.snake.insert(0, new_head)
        if new_head == self.food_position:
            self.create_food()
        else:
            self.snake.pop()

        # Redraw the snake and schedule the next move
        self.draw_snake()
        self.root.after(SNAKE_SPEED, self.move_snake)

    def end_game(self):
        """Handle the end of the game."""
        self.game_over = True
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2,
            text="GAME OVER", fill="red", font=("Helvetica", 24)
        )

# Initialize the Tkinter window and start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
