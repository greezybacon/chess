import pyglet
from pyglet import image
from pyglet.graphics import Batch
from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite
from pyglet.window import Window

WHITE = 'white'
BLACK = 'black'

class Piece:
    sprite_image = 'piece_X.png'

    def __init__(self, color=WHITE):
        self.board = None
        self.board_pos = (0, 0)

    def draw_on(self, batch: Batch):
        # Add a sprite for this piece into batch
        img = pyglet.resource.image(self.sprite_image)

        # Find the larger of width / height
        larger = max(img.width, img.height)

        # Scale the image to fit in the 64x64 game space
        scale = 64 / larger
        img.width *= scale
        img.height *= scale

        # Add a sprite to be rendered on the board
        self.sprite = Sprite(img=img, batch=batch)

    def get_position(self, coords):
        # Convert algebraic notation into (y,x) coordinates
        col, row = coords
        return ('abcdefgh'.index(col), int(row) - 1)

    def place_at(self, coords):
        # Move the piece to the given algebraic coordinates
        x, y = self.get_position(coords)
        self.board_pos = (x, y)

        # Place the game piece in the center of the square. First, define
        # the location of the center of the square
        size = self.board.size
        x_center = (x + 0.5) * size
        y_center = (y + 0.5) * size

        # Add in the difference between the center of the sprite
        dw = 32 + (self.sprite.width - size) // 2
        dh = 32 + (self.sprite.height - size) // 2
        print(size, x_center, y_center, dw, dh)
        self.sprite.position = x_center - dw, y_center - dh, 0

    def valid_moves(self):
        # Return a list of valid positions to which this piece can be moved
        # based on its current position
        current = self.board_pos


class Knight(Piece):
    sprite_image = 'knight.png'


class ChessBoard:
    def __init__(self, size=64):
        self.size = size
        self.background = Batch()
        self.tiles = self.add_tiles()
        self.reset()

    def reset(self):
        # Clear all the pieces off the board.
        self.pieces = list()
        self.foreground = Batch()

    def setup(self):
        # Add all the pieces to the board for the initial game setup.
        self.add_piece(Knight(WHITE), 'b1')

    def draw(self):
        self.background.draw()
        self.foreground.draw()

    def add_tiles(self):
        # Draw the base tiles of the board
        size = self.size
        tiles = list()
        for row in range(8):
            for col in range(8):
                is_dark = (row + col) % 2 == 0
                if is_dark:
                    color = (64, 64, 64)
                else:
                    color = (192, 192, 192)

                tiles.append(
                    Rectangle(col * size, row * size, size, size, color=color,
                        batch=self.background))

        return tiles

    def add_piece(self, piece: Piece, coords: str):
        # Add a game piece, initially placed at place
        self.pieces.append(piece)
        piece.draw_on(self.foreground)

        # This is weird, but `self` is the actual ChessBoard object (this
        # object itself)
        piece.board = self
        piece.place_at(coords)


window = Window(64 * 8 + 32, 64 * 8 + 32)
board_batch = Batch()

board = ChessBoard(size=64)

@window.event
def on_draw():
    window.clear()
    board.draw()

if __name__ == '__main__':
    import os.path
    pyglet.resource.path = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources'),
    ]
    pyglet.resource.reindex()

    board.setup()
    pyglet.app.run()
