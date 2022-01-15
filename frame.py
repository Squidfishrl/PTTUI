from .terminal import Terminal
from typing import Type

class FrameManager():
    """
    Class managing printing the frames
    Uses a 2 dimensional matrix with the size of the terminal
    """

    def __init__(self, rows: int, columns: int) -> None:
        self.rows: int = rows
        self.columns: int = columns
        frames: list[Frame] = []

        """
        +1 is added to the columns make space for \n
        Frankly, the \n won't be seen as it's outside of the terminal, but it wraps the lines
        """

        char_grid: list[list[str]] = [ ['\n' if i == columns else ' ' for i in range(columns+1)] * rows] 


    def print(self) -> None:
        """ Conver char_grid to a string via list coprehension and print it """

        """
        # Non-comprehension sollution

        for row in range(0, rows):
            for column in range(0, columns):
                buf += char_grid[row][column]
        """

        print(''.join([[char for char in self.char_grid[row]] for row in range(self.rows)]))

        
                

class Frame():
    """
    Class that creates a frame for a widget
    Frames work similarly to a tiling window manager
    There's one main frame, allowing one window - or in this case one widget
    the frame can then be split vertically (splitv) or horizontally (splith)
    """

    def __init__(self) -> None:
        """ Initialize a frame which covers the entire screen """ 
        width_percent: int = 100
        height_percent: int = 100

        top_left_point: tuple[int] = (1, 1)

        # width_characters: int
        # height_characters: int

    def splitv(self) -> Frame:
        pass

    def splith(self) -> Frame:
        pass
