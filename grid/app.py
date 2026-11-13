from flask import Flask, render_template, session, request, make_response

import random

app = Flask(__name__)
app.secret_key = "theMostSecretOfKeys"

@app.get("/")
@app.get("/showgrid")
def display_the_grid():
    session["count"] = 0
    session["active_cell"] = {}
    session["block_dropping"] = False
    return render_template(
        "grid.html",
        rowcount=8,
        colcount=6,
        colour="white",
    )

@app.post("/drop_block/<rowcount>/<colcount>")
def drop_block(rowcount, colcount):

    if not session["block_dropping"]:

        newRow = 0
        newCol = random.randint(0, int(colcount) - 1)
        session["active_cell"] = {"row": newRow, "col": newCol}
        session["block_dropping"] = True

        return color_cell(newRow, newCol)

    else:

        currentRow = session["active_cell"]["row"]
        currentCol = session["active_cell"]["col"]

        if currentRow < int(rowcount) - 1:
            nextRow = currentRow + 1
            session["active_cell"] = {"row": nextRow, "col": currentCol}
            return color_cell(nextRow, currentCol)

        session["block_dropping"] = False
        return ""

def color_cell(row, col):
    response = make_response(render_template(
        "snippet.html",
        row=row,
        col=col,
        colour="black",
    ))
    response.headers["HX-Retarget"] = f"#cell-{row}-{col}"
    response.headers["HX-Reswap"] = "outerHTML"
    return response


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
    session["count"] = session["count"] + 1
    return "Time is ticking: " + str(session["count"])


@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]
    return f"You pressed: {key_pressed}."



if __name__ == "__main__":
    app.run(debug=True)
