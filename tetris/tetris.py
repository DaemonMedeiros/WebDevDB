from textual.app import App
from textual.widgets import Label, Button
from textual.containers import Container
from textual import events
import time
import random

class TetrisGame:
    def __init__(self):
        self.rows = 10
        self.columns = 5
        self.grid = []
        self.game_over = False
        self.seconds = 0
        self.block_char = "██"
        self.blank_char = "  "
        
    def clear_grid(self):
        """Create a new empty grid"""
        self.grid = [[self.blank_char for _ in range(self.rows)] for _ in range(self.columns)]
    
    def check_bounds(self):
        """Check if game is over (blocks at top)"""
        for col in range(self.columns):
            if self.grid[col][0] == self.block_char:
                return False
        return True
    
    def is_row_full(self, row):
        """Check if a row is full"""
        if row < 0 or row >= self.rows:
            return False
        for col in range(self.columns):
            if self.grid[col][row] == self.blank_char:
                return False
        return True
    
    def clear_row(self, row):
        """Clear a specific row"""
        for col in range(self.columns):
            self.grid[col][row] = self.blank_char
    
    def shift_rows_down(self, start_row):
        """Shift rows down from start_row"""
        for row in range(start_row - 1, -1, -1):
            for col in range(self.columns):
                self.grid[col][row + 1] = self.grid[col][row]
                self.grid[col][row] = self.blank_char
    
    def handle_full_rows(self):
        """Handle full rows"""
        for i in range(self.rows):
            if self.is_row_full(i):
                self.clear_row(i)
                self.shift_rows_down(i)

class TetrisApp(App):
    
    def __init__(self):
        super().__init__()
        self.game = TetrisGame()
        self.game.clear_grid()
        
    def compose(self):
        """Create the UI"""
        yield Container(
            Label("TETRIS GAME"),
            Label("", id="game-display"),  # Will show grid
            Label("Time: 0s", id="time-label"),
            Button("Quit", id="quit-button"),
            id="main-container"
        )
    
    def on_mount(self):
        """Called when app starts"""
        self.update_grid_display()
        self.set_interval(1.0, self.game_loop)  # Update every 1 second for timing
    
    def update_grid_display(self):
        """Update the visual grid display"""
        display = ""
        for row in range(self.game.rows):
            for col in range(self.game.columns):
                display += self.game.grid[col][row] + " "
            display += "\n"
        
        display_widget = self.query_one("#game-display")
        display_widget.update(display)
    
    def game_loop(self):
        """Main game loop - runs once per second"""
        if not self.game.game_over:
            # Update time counter
            self.game.seconds += 1
            
            # Update display
            time_label = self.query_one("#time-label")
            time_label.update(f"Time: {self.game.seconds}s")
            
            # Handle dropping block logic (this makes the game progress)
            if self.game.check_bounds():
                col = random.randint(0, self.game.columns - 1)
                self.drop_block(col)
                self.game.handle_full_rows()
                self.update_grid_display()
            else:
                # Game over condition - top row is filled
                self.game_over()
    
    def drop_block(self, column):
        """Drop a block in the specified column"""
        # Find the lowest empty position
        row = self.game.rows - 1
        while row >= 0 and self.game.grid[column][row] != self.game.blank_char:
            row -= 1
        
        if row >= 0:
            self.game.grid[column][row] = self.game.block_char
    
    def game_over(self):
        """Handle game over"""
        self.game.game_over = True
        display_widget = self.query_one("#game-display")
        display_widget.update("GAME OVER!")
        
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard input"""
        if event.key == "q":
            self.exit()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "quit-button":
            self.exit()

if __name__ == "__main__":
    app = TetrisApp()
    app.run()
