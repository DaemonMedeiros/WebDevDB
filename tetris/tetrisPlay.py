import time
import random
import queue
import sys
from pynput import keyboard
from IPython.display import clear_output

rows = 0
columns = 0

_ROW = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"

gameOver = False
key_pressed = None
action_queue = queue.Queue()

def process_key_press(key):
    global key_pressed
    try:
        key_pressed = key.char
    except AttributeError:
        key_pressed = str(key)

listener = keyboard.Listener(on_press = process_key_press)

def clear_grid(row, col):
    grid = [[_BLANK for i in range(row) ] for i in range (col)]
    return grid

def clear_terminal():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def drop_block(grid, column_number):
    try:
        n = grid[column_number].index(_BLOCK)
        n = n-1
    except:
        n = -1
    grid[column_number][n] = _BLOCK
    return grid

def display_grid(grid):
    global rows
    global columns
    
    col = tuple(range(0,columns))
    row = tuple(range(0,rows))
    for r in row:
        print("|", sep="", end = "")
        for c in col:
            print(grid[c][r], "|", sep="", end = "")
        print()

def show_dropping_block(grid, column_number):

    global rows
    global columns
    global key_pressed
    global gameOver
    
    if(check_bounds(grid) and not gameOver):
        
        while grid[column_number][0] == _BLOCK:
            column_number += 1
            
            if column_number >= columns:
                column_number = 0

        if key_pressed == "Key.Q" or key_pressed == "Key.q":
            gameOver = True
                
        for row in range(_ROW):
            
            if key_pressed == "Key.left" and column_number > 0:
                if grid[column_number - 1][row] != _BLOCK:
                    column_number -= 1
                    
            if key_pressed == "Key.right" and column_number < columns - 1:
                if grid[column_number + 1][row] != _BLOCK:
                    column_number += 1

            key_pressed = ""
            
            grid[column_number][row] = _BLOCK
            clear_terminal()
            
            display_grid(grid)
            
            time.sleep(_INTERVAL)
            
            clear_output(wait = True)
            
            grid[column_number][row] = _BLANK
            
            if row + 1 < rows:
                if grid[column_number][row + 1] == _BLOCK: break
                    
            display_grid(grid)
            clear_output(wait = True)
            
        drop_block(grid, column_number)
        return column_number

def drop_group(grid, amount):
    for i in range(amount):
        show_dropping_block(grid, random.randint(0, _COLUMNS-1))
        #randomise
    return grid

def check_bounds(grid):
    global columns
    for i in range(columns):
        if grid[i][0] == _BLOCK:
            print("Game Over")
            return False
    return True

def getPlayerInput():
    global rows
    global columns
    
    rows = int(input("Enter number of rows: "))
    columns = int(input("Enter number of columns: "))
    
    
def run():
    global rows
    global columns
    global gameOver

    getPlayerInput()
    grid = clear_grid(rows, columns)
    col = random.randint(0, columns)
    listener.start()
    while check_bounds(grid) and not gameOver:
        col = show_dropping_block(grid,col)
        col = random.randint(0, 4)
    listener.stop()