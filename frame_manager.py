from itertools import chain
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
        self.char_grid: list[list[str]] = [ ['\n' if column == terminal.columns else ' ' for column in range(terminal.columns+1)] for row in range(terminal.rows)] 
        self.char_grid[-1][-1] = ''  # remove last new line


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

    def _update_chars(self, target_frame: Frame = None) -> None:
        """
        Updates the char_grid buffer with the char buffer of all frames or a specified frame
        """

        # iterate over all frames
        for frame in self.frames:
            # load target frame (exit out of for after)
            if target_frame is not None:
                frame = target_frame

            # -1 because first character is considered (1, 1) but lists start from 0
            row_offset: int = frame.top_left_point[0] - 1
            column_offset: int = frame.top_left_point[1] - 1

            for row in range(frame.rows):
                for column in range(frame.columns):
                    # replace previous frame chars with new ones
                    self.char_grid[row + row_offset][column + column_offset] = frame.chars[row][column]

            if target_frame is not None:
                break




    def print(self) -> None:
        """ Conver char_grid to a string via list coprehension and print it """

        self._update_chars()

        """
        # Non-comprehension sollution

        buffer: str = ''
        for row in self.char_grid:
            for char in row:
                buffer += f"{char}"

        self.terminal.write(buffer)
        """
        
        self.terminal.write(''.join([char for row in self.char_grid for char in row]))

    def __str__(self) -> str:
        """ Get string of char_grid in the way you would get it printed """
        return ''.join([char for row in self.char_grid for char in row])


if __name__ == '__main__':
    frame_manager = FrameManager()
    frame_manager.frames[-1].add_border()
    # print frame -> intended way
    # frame_manager.print() 
    
    # manual print (no \n when program exits (no loop due to no events in example
    frame_manager._update_chars()
    print(frame_manager, end='')
    input()
