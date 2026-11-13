from flask import Flask, render_template, session, request, make_response

import random

app = Flask(__name__)
app.secret_key = "theMostSecretOfKeys"

@app.get("/")
@app.get("/showgrid")
def display_the_grid():

    session["game"] = {
        "ROWS": 8,
        "COLS": 6,
        "block_dropping": False,
        "active": {},
        "seconds": 0,
    }

    return render_template(
        "grid.html",
        rowcount=session["game"]["ROWS"],
        colcount=session["game"]["COLS"],
        colour="white",
    )


@app.post("/drop_block")
def drop_block():

    game = session["game"]

    if not game["block_dropping"]:
        col = random.randint(0, game["COLS"] - 1)
        game["active"] = {"row": 0, "col": col}
        game["block_dropping"] = True
        session.modified = True
        return color_cell(0, col, "black")

    row = game["active"]["row"]
    col = game["active"]["col"]

    if row < game["ROWS"] - 1:
        game["active"]["row"] = row + 1
        session.modified = True
        return color_cell(row, col, "white") + color_cell(row + 1, col, "black")

    game["block_dropping"] = False
    session.modified = True
    return ""


# AI Helped me with the color_cell function
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
    session["game"]["seconds"] += 1
    session.modified = True
    return "Time is ticking: " + str(session["game"]["seconds"])


@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]
    return f"You pressed: {key_pressed}."



if __name__ == "__main__":
    app.run(debug=True)
