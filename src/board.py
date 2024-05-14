import pyglet
from pyglet.graphics import Batch
from pyglet.shapes import Rectangle
from pyglet.window import Window

class ChessBoard:
    def __init__(self, size=64):
        self.size = size
        self.background = Batch()
        self.tokens = Batch()
        self.add_tiles()

    def draw(self):
        self.background.draw()

    def add_tiles(self):
        size = self.size
        tiles = []
        for row in range(8):
            for col in range(8):
                is_dark = (row + col) % 2 == 1
                if is_dark:
                    color = (64, 64, 64)
                else:
                    color = (192, 192, 192)

                tiles.append(
                    Rectangle(col * size, row * size, size, size, color=color,
                        batch=self.background))

        self.tiles = tiles


window = Window(64 * 8, 64 * 8)
board_batch = Batch()

board = ChessBoard(size=64)

@window.event
def on_draw():
    window.clear()
    board.draw()

if __name__ == '__main__':
    pyglet.app.run()
