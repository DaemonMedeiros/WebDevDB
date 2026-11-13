from flask import Flask, render_template, session, request
import random

app = Flask(__name__)
app.secret_key = "theMostSecretOfKeys"

ROWS = 8
COLS = 6

def make_grid(rows, columns, value):

    grid = []

    for row in range(rows):
        grid.append([value] * columns)

    return grid


@app.get("/")
@app.get("/showgrid")
def display_the_grid():

    session["game"] = {
        "block_dropping": False,
        "active": {},
        "count": 0,
        "right_pressed": False,
        "left_pressed": False,
        "occupied_cells": make_grid(ROWS, COLS, False),
    }

    return render_template(
        "grid.html",
        rowcount=ROWS,
        colcount=COLS,
        colour="white",
    )

@app.post("/drop_block")
def drop_block():
    game = session["game"]

    # Spawn a block in a random col of the first row
    if not game["block_dropping"]:
        col = random.randint(0, COLS - 1)
        game["active"] = {"row": 0, "col": col}
        game["block_dropping"] = True
        session.modified = True
        return color_cell(0, col, "black")

    # creating shorter variable names/ prep for movment 
    row = game["active"]["row"]
    old_col = game["active"]["col"]
    new_col = old_col

    # check my booleans that are set in which_key_pressed
    if game["right_pressed"] and old_col < COLS - 1:
        if not game["occupied_cells"][row][old_col + 1]:
            new_col = old_col + 1
    if game["left_pressed"] and old_col > 0:
        if not game["occupied_cells"][row][old_col - 1]:
            new_col = old_col - 1

    game["right_pressed"] = False
    game["left_pressed"] = False

    # if next block is not occupied move the active block down/ sideways
    if row < ROWS - 1 and not game["occupied_cells"][row + 1][new_col]:
        game["active"]["row"] = row + 1
        game["active"]["col"] = new_col
        session.modified = True
        return (
            color_cell(row, old_col, "white")
            + color_cell(row + 1, new_col, "black")
        )

    # mark cell as occupied and reset block dropping bool
    game["occupied_cells"][row][old_col] = True
    game["block_dropping"] = False
    session.modified = True
    return ""

def color_cell(row, col, colour):
    return render_template(
        "snippet.html",
        row=row,
        col=col,
        colour=colour,
        oob=True,
    )

@app.post("/location/<row>/<col>/<colour>")
def process_the_click(row, col, colour):
    set_colour = "white" if colour == "black" else "black"
    return render_template(
        "snippet.html",
        row=row,
        col=col,
        colour=set_colour,
    )

@app.post("/counting")
def maintain_count():
    session["game"]["count"] = session["game"]["count"] + 1
    return "Time is ticking: " + str(session["game"]["count"])

@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]

    if key_pressed == "ArrowRight":
        session["game"]["right_pressed"] = True
        session.modified = True
    elif key_pressed == "ArrowLeft":
        session["game"]["left_pressed"] = True
        session.modified = True

    return f"You pressed: {key_pressed}."


if __name__ == "__main__":
    app.run(debug=True)
