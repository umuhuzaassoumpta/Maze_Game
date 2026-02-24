import tkinter as tk
from tkinter import messagebox
import random

class MazeExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Explorer")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        
        # Game variables
        self.current_level = 1
        self.max_level = 3
        self.score = 0
        self.player_pos = [0, 0]
        self.goal_pos = [0, 0]
        self.enemies = []
        self.coins = []
        self.walls = []
        self.grid_size = 10
        self.cell_size = 50
        
        # Colors
        self.colors = {
            "background": "#f0f0f0",
            "player": "#3498db",
            "goal": "#2ecc71",
            "wall": "#34495e",
            "enemy": "#e74c3c",
            "coin": "#f1c40f"
        }
        
        # Create frames
        self.top_frame = tk.Frame(root, bg=self.colors["background"])
        self.top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(padx=10, pady=10)
        
        # Create UI elements
        self.level_label = tk.Label(self.top_frame, text=f"Level: {self.current_level}/{self.max_level}", 
                                   font=("Arial", 14), bg=self.colors["background"])
        self.level_label.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(self.top_frame, text=f"Score: {self.score}", 
                                   font=("Arial", 14), bg=self.colors["background"])
        self.score_label.pack(side=tk.RIGHT)
        
        # Create game canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=self.grid_size*self.cell_size, 
                               height=self.grid_size*self.cell_size, bg=self.colors["background"])
        self.canvas.pack()
        
        # Create instruction frame
        self.instruction_frame = tk.Frame(root, bg=self.colors["background"])
        self.instruction_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.instruction_label = tk.Label(self.instruction_frame, 
                                        text="Use arrow keys to move. Collect coins, avoid enemies, reach the goal!",
                                        font=("Arial", 12), bg=self.colors["background"], wraplength=580)
        self.instruction_label.pack()
        
        # Bind keys
        self.root.bind("<Left>", lambda event: self.move_player(-1, 0))
        self.root.bind("<Right>", lambda event: self.move_player(1, 0))
        self.root.bind("<Up>", lambda event: self.move_player(0, -1))
        self.root.bind("<Down>", lambda event: self.move_player(0, 1))
        
        # Start game
        self.start_level()
    
    def start_level(self):
        # Reset canvas and game elements
        self.canvas.delete("all")
        self.walls = []
        self.enemies = []
        self.coins = []
        
        # Update level label
        self.level_label.config(text=f"Level: {self.current_level}/{self.max_level}")
        
        # Configure level based on current level number
        if self.current_level == 1:
            self.setup_level_1()
        elif self.current_level == 2:
            self.setup_level_2()
        elif self.current_level == 3:
            self.setup_level_3()
        
        # Draw grid
        self.draw_grid()
        
        # Draw game elements
        self.draw_game_elements()
    
    def setup_level_1(self):
        # Basic level with a few walls and enemies
        self.player_pos = [0, 0]
        self.goal_pos = [9, 9]
        
        # Create some walls
        self.walls = [
            [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
            [4, 5], [5, 5], [6, 5], [7, 5],
            [7, 2], [7, 3], [7, 4]
        ]
        
        # Add enemies
        self.enemies = [
            [3, 3], [6, 7], [8, 2]
        ]
        
        # Add coins
        self.coins = [
            [1, 2], [3, 6], [5, 8], [8, 4], [9, 1]
        ]
    
    def setup_level_2(self):
        # More complex level
        self.player_pos = [0, 0]
        self.goal_pos = [9, 9]
        
        # Create more walls - maze-like pattern
        self.walls = [
            [1, 1], [1, 2], [1, 3], [1, 5], [1, 6], [1, 7], [1, 9],
            [3, 1], [3, 3], [3, 5], [3, 7], [3, 9],
            [5, 0], [5, 1], [5, 3], [5, 5], [5, 7], [5, 9],
            [7, 1], [7, 3], [7, 5], [7, 7], [7, 8], [7, 9],
            [9, 1], [9, 3], [9, 5], [9, 7]
        ]
        
        # Add more enemies
        self.enemies = [
            [2, 2], [4, 4], [6, 6], [8, 8], [2, 8], [8, 2]
        ]
        
        # Add coins
        self.coins = [
            [0, 5], [2, 9], [4, 2], [6, 4], [8, 6], [4, 8], [9, 0]
        ]
        
        # Add moving enemies
        self.enemy_timer = self.root.after(500, self.move_enemies)
    
    def setup_level_3(self):
        # Most complex level with moving walls
        self.player_pos = [0, 0]
        self.goal_pos = [9, 9]
        
        # Create complex wall pattern
        self.walls = []
        # Outer border walls (with gaps)
        for i in range(1, 9):
            if i != 3 and i != 7:
                self.walls.append([i, 0])
                self.walls.append([i, 9])
                self.walls.append([0, i])
                self.walls.append([9, i])
        
        # Inner maze structure
        inner_walls = [
            [2, 2], [2, 3], [2, 4], [2, 6], [2, 7], [2, 8],
            [4, 2], [4, 3], [4, 4], [4, 6], [4, 7], [4, 8],
            [6, 2], [6, 3], [6, 4], [6, 6], [6, 7], [6, 8],
            [8, 2], [8, 3], [8, 4], [8, 6], [8, 7], [8, 8],
            [3, 5], [5, 5], [7, 5]
        ]
        self.walls.extend(inner_walls)
        
        # Add many enemies
        self.enemies = [
            [1, 3], [3, 1], [3, 8], [5, 3], [7, 1], [7, 8], [8, 5]
        ]
        
        # Add coins
        self.coins = [
            [1, 1], [1, 8], [3, 3], [3, 7], [5, 1], [5, 8], [7, 3], [7, 7], [8, 1], [8, 8]
        ]
        
        # Start enemy movement
        self.enemy_timer = self.root.after(300, self.move_enemies)
        
        # Start wall movement
        self.wall_timer = self.root.after(2000, self.move_walls)
    
    def move_enemies(self):
        # Move enemies randomly
        for i in range(len(self.enemies)):
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x = self.enemies[i][0] + direction[0]
            new_y = self.enemies[i][1] + direction[1]
            
            # Check bounds and walls
            if (0 <= new_x < self.grid_size and 
                0 <= new_y < self.grid_size and 
                [new_x, new_y] not in self.walls):
                self.enemies[i] = [new_x, new_y]
        
        # Redraw game elements
        self.draw_game_elements()
        
        # Check if player collided with an enemy
        if self.player_pos in self.enemies:
            self.game_over("You were caught by an enemy!")
            return
        
        # Continue movement
        if self.current_level >= 2:
            self.enemy_timer = self.root.after(500, self.move_enemies)
    
    def move_walls(self):
        if self.current_level == 3:
            # Move some random walls
            movable_walls = [wall for wall in self.walls if wall not in [[0, 0], [9, 9]]]
            
            if movable_walls:
                wall_to_move = random.choice(movable_walls)
                self.walls.remove(wall_to_move)
                
                # Find a new position for the wall
                while True:
                    new_x = random.randint(0, self.grid_size - 1)
                    new_y = random.randint(0, self.grid_size - 1)
                    
                    if ([new_x, new_y] != self.player_pos and 
                        [new_x, new_y] != self.goal_pos and 
                        [new_x, new_y] not in self.walls):
                        self.walls.append([new_x, new_y])
                        break
            
            # Redraw game elements
            self.draw_game_elements()
            
            # Continue wall movement
            self.wall_timer = self.root.after(2000, self.move_walls)
    
    def draw_grid(self):
        # Draw grid lines
        for i in range(self.grid_size + 1):
            self.canvas.create_line(0, i * self.cell_size, 
                                  self.grid_size * self.cell_size, i * self.cell_size, 
                                  fill="#d0d0d0")
            self.canvas.create_line(i * self.cell_size, 0, 
                                  i * self.cell_size, self.grid_size * self.cell_size, 
                                  fill="#d0d0d0")
    
    def draw_game_elements(self):
        # Clear existing elements
        self.canvas.delete("game_element")
        
        # Draw walls
        for wall in self.walls:
            x, y = wall
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill=self.colors["wall"], tags="game_element"
            )
        
        # Draw coins
        for coin in self.coins:
            x, y = coin
            self.canvas.create_oval(
                x * self.cell_size + 15, y * self.cell_size + 15,
                (x + 1) * self.cell_size - 15, (y + 1) * self.cell_size - 15,
                fill=self.colors["coin"], tags="game_element"
            )
        
        # Draw enemies
        for enemy in self.enemies:
            x, y = enemy
            self.canvas.create_oval(
                x * self.cell_size + 5, y * self.cell_size + 5,
                (x + 1) * self.cell_size - 5, (y + 1) * self.cell_size - 5,
                fill=self.colors["enemy"], tags="game_element"
            )
        
        # Draw goal
        x, y = self.goal_pos
        self.canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill=self.colors["goal"], tags="game_element"
        )
        
        # Draw player
        x, y = self.player_pos
        self.canvas.create_oval(
            x * self.cell_size + 10, y * self.cell_size + 10,
            (x + 1) * self.cell_size - 10, (y + 1) * self.cell_size - 10,
            fill=self.colors["player"], tags="game_element"
        )
    
    def move_player(self, dx, dy):
        # Calculate new position
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Check if move is valid (within bounds and not into a wall)
        if (0 <= new_x < self.grid_size and 
            0 <= new_y < self.grid_size and 
            [new_x, new_y] not in self.walls):
            
            # Update player position
            self.player_pos = [new_x, new_y]
            
            # Check for coin collection
            if self.player_pos in self.coins:
                self.coins.remove(self.player_pos)
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
            
            # Check for enemy collision
            if self.player_pos in self.enemies:
                self.game_over("You were caught by an enemy!")
                return
            
            # Check for goal reached
            if self.player_pos == self.goal_pos:
                if self.current_level < self.max_level:
                    self.current_level += 1
                    messagebox.showinfo("Level Complete", 
                                        f"Level {self.current_level-1} complete! Moving to level {self.current_level}.")
                    
                    # Cancel any running timers
                    if hasattr(self, 'enemy_timer'):
                        self.root.after_cancel(self.enemy_timer)
                    if hasattr(self, 'wall_timer'):
                        self.root.after_cancel(self.wall_timer)
                    
                    self.start_level()
                else:
                    self.game_over("Congratulations! You've completed all levels!")
                return
            
            # Redraw game elements
            self.draw_game_elements()
    
    def game_over(self, message):
        # Cancel any running timers
        if hasattr(self, 'enemy_timer'):
            self.root.after_cancel(self.enemy_timer)
        if hasattr(self, 'wall_timer'):
            self.root.after_cancel(self.wall_timer)
        
        # Show game over message
        answer = messagebox.askquestion("Game Over", 
                                     f"{message}\nYour score: {self.score}\nDo you want to restart?")
        
        if answer == 'yes':
            # Reset game
            self.current_level = 1
            self.score = 0
            self.score_label.config(text=f"Score: {self.score}")
            self.start_level()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeExplorer(root)
    root.mainloop()
