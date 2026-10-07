from textual import events
from textual.app import App
from textual.widgets import Label, Static

class Tetris(App):

    _MAX_COLORS = 10
    color_index = 0
    
    COLORS = [
        "white",
        "maroon",
        "red",
        "purple",
        "fuchsia",
        "olive",
        "yellow",
        "navy",
        "teal",
        "aqua",
        ]


    def on_mount(self):
        # Styling the background
        self.screen.styles.background = "teal"
        # Styling the static
        self.static.styles.background = "darkgreen"
        self.static.styles.text_align = "center"
        self.static.styles.padding = 1, 1
        self.static.styles.margin = 0, 0


    def compose(self):
        self.static = Static(
            "[bold]Tetris[/bold]",
        )
        yield self.static
    
    def on_key(self, event: events.Key) -> None:
        if event.key == "right":
            if self.color_index < self._MAX_COLORS - 1:
                self.color_index = self.color_index + 1
                self.screen.styles.background = self.COLORS[self.color_index]
                
        if event.key == "left":
            if self.color_index > 0:
                self.color_index = self.color_index - 1
                self.screen.styles.background = self.COLORS[self.color_index]

if __name__ == "__main__":
    app = Tetris()
    app.run()