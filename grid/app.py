from flask import Flask, render_template, session, request

import random

app = Flask(__name__)
app.secret_key = "theMostSecretOfKeys"

@app.get("/")
@app.get("/showgrid")
def display_the_grid():
    session["count"] = 0
    return render_template(
        "grid.html",
        rowcount=8,
        colcount=6,
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

@app.get("/spawn_block/<int:rowcount>/<int:colcount>")
def spawn_random_block(rowcount, colcount):
    # random_row = random.randint(0, rowcount - 1)
    random_row = 0
    random_col = random.randint(0, colcount - 1)

    html = render_template(
        "snippet.html",
        row=random_row,
        col=random_col,
        colour="black",
    )

    return html, {
        "HX-Retarget": f"[id='{random_col}, {random_row}']",
        "HX-Reswap": "outerHTML",
    }


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
