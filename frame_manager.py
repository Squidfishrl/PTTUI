from typing import Type

from frame import Frame
from terminal import Terminal
from widget import Widget


class FrameManager():
    """
    Class managing multiple frames, including:
    - tilling window manager like frame creation (splitv and splith)
    - listening to terminal resize events to update a frame
    - combining all frames into a string, (TODO: passed to terminal print)
    TODO: Frame overlay - perhaps use multiple frame managers or separate property for that?
    Uses a 2 dimensional matrix with the size of the terminal when printing
    """

    def __init__(self, terminal: Terminal = Terminal()) -> None:
        self.terminal: Terminal = terminal

        self.frames: list[Frame] = []  # create an empty frame
        self._create_first_frame()

        """
        +1 is added to the columns make space for \n
        Frankly, the \n won't be seen as it's outside of the terminal, but it wraps the lines
        """

        # create a matrix holding all the characters to be printed to the term
        char_grid: list[list[str]] = [ ['\n' if column == terminal.columns else ' ' for column in range(terminal.columns+1)] for row in range(terminal.rows)] 


    def _create_first_frame(self) -> Frame:
        """
        Create and return a new frame
        Is called on init (there's always one empty frame)
        Works only when no frames have been created (use splith/v if one exists) for the current overlay level
        """

        # create a new frame taking up the entire terminal 
        initial_frame: Frame = Frame(self.terminal.rows, self.terminal.columns, (1, 1))  
        self.frames.append(initial_frame)  # append it to a list of all frames
        self._register_frame(initial_frame)


    def _register_frame(self, frame: Frame) -> None:
        """
        Registers a frame for terminal resize event 
        Called when a frame is created
        """

        self.terminal.on_resize(frame.resize)

    def print(self) -> None:
        """ Conver char_grid to a string via list coprehension and print it """

        """
        # Non-comprehension sollution

        for row in range(0, rows):
            for column in range(0, columns):
                buf += char_grid[row][column]
        """

        self.terminal.write((''.join([[char for char in self.char_grid[row]] for row in range(self.terminal.rows)])))


if __name__ == '__main__':
    frame_manager = FrameManager()
    first_frame: Frame = frame_manager.frames[-1]
    first_frame.add_border()
    print(first_frame.rows)
    print(first_frame.columns)
    print(first_frame.top_left_point)

    # print frame
    print(first_frame, end='')
    input()
