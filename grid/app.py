from flask import Flask, render_template, session, request

import random

app = Flask(__name__)
app.secret_key = "theMostSecretOfKeys"

@app.get("/")
@app.get("/showgrid")
def display_the_grid():
    session["count"] = 0
    session["ROWS"] = 8
    session["COLS"] = 6
    return render_template(
        "grid.html",
        rowcount=session["ROWS"],
        colcount=session["COLS"],
        colour="white",
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

@app.post("/spawn_block/<rowcount>/<colcount>")
def spawn_random_block(rowcount, colcount):
    random_row = random.randint(0, rowcount - 1)
    random_col = random.randint(0, colcount - 1)


@app.post("/counting")
def maintain_count():
    session["count"] = session["count"] + 1
    return "Time is ticking: " + str(session["count"])


@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]
    return f"You pressed: {key_pressed}."



if __name__ == "__main__":
    app.run(debug=True)
