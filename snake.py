import tkinter as tk
import random

# Game configuration
WIDTH = 500
HEIGHT = 500
CELL_SIZE = 20
SPEED = 100  # Milliseconds between snake moves

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'Right'
        self.running = True

        self.food = self.place_food()
        self.draw_objects()

        self.master.bind("<KeyPress>", self.change_direction)
        self.move_snake()

    def draw_objects(self):
        self.canvas.delete(tk.ALL)
        # Draw Snake
        for segment in self.snake:
            self.canvas.create_rectangle(*segment, segment[0]+CELL_SIZE, segment[1]+CELL_SIZE, fill='blue')

        # Draw Food
        x, y = self.food
        self.canvas.create_oval(x, y, x+CELL_SIZE, y+CELL_SIZE, fill='green')

    def move_snake(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]
        new_head = {
            'Left': (head_x - CELL_SIZE, head_y),
            'Right': (head_x + CELL_SIZE, head_y),
            'Up': (head_x, head_y - CELL_SIZE),
            'Down': (head_x, head_y + CELL_SIZE)
        }[self.direction]

        # Check for collisions
        if (new_head in self.snake or
                not 0 <= new_head[0] < WIDTH or
                not 0 <= new_head[1] < HEIGHT):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Check for food
        if new_head == self.food:
            self.food = self.place_food()
        else:
            self.snake.pop()

        self.draw_objects()
        self.master.after(SPEED, self.move_snake)

    def change_direction(self, event):
        directions = {'Left', 'Right', 'Up', 'Down'}
        if event.keysym in directions:
            opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
            if self.direction != opposites[event.keysym]:
                self.direction = event.keysym

    def place_food(self):
        while True:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill="white", font=('Arial', 30))

# Run the game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
