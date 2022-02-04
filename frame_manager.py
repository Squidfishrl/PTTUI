from math import ceil, floor
from typing import Type

from frame import Frame
from terminal import Terminal
from widget import Widget


class FrameManager():
    """
    Class managing multiple frames, including:
    - tilling window manager like frame creation (splitv and splith)
    - listening to terminal resize events to update a frame
    - combining all frames into a string 
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
        TODO: Don't resize individual frames, just subscribe the frame manager which resizes all the frames
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
        """ Convert char_grid to a string via list comprehension and print it """

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

    def splitv(self, frame: Frame) -> Frame:
        """
        Splits a frame vertically, creating 2 frames
        TODO: More arguments such as % % split..
        if there is frame x " x "
        after split and a new frame y will be " x|y "

        TODO: three+ way event splits..
        """
        # Create a new frame in the above described way
        new_frame: Frame = Frame(frame.rows, ceil(frame.columns/2), (frame.top_left_point[0], frame.top_left_point[1] + floor(frame.columns/2)))
        self.frames.append(new_frame)
        
        # TODO Resize old frame -> Also take in account dividing odd numbers, use math.floor or ceil
        frame.resize(frame.rows, floor(frame.columns/2), frame.top_left_point)

        # register new frame
        self._register_frame(new_frame)

        return new_frame

    def splith(self, frame: Frame) -> Frame:
        """
        Splits a frame horisontally, creating 2 frames
        TODO: More arguments such as % % split..
        if there is frame x 
        "   "
        " x "
        "   "
        after split and a new frame y will be and:
        " x "
        "---"
        " y "

        TODO: three+ way event splits..
        """
        # Create a new frame in the above described way
        new_frame: Frame = Frame(ceil(frame.rows/2), frame.columns, (frame.top_left_point[0] + floor(frame.rows/2), frame.top_left_point[1]))
        self.frames.append(new_frame)

        # TODO Resize old frame -> Also take in account dividing odd numbers, use math.floor or ceil
        frame.resize(floor(frame.rows/2), frame.columns, frame.top_left_point)

        # register new frame
        self._register_frame(new_frame)

        return new_frame

    def __str__(self) -> str:
        """ Get string of char_grid in the way you would get it printed """
        return ''.join([char for row in self.char_grid for char in row])


if __name__ == '__main__':
    frame_manager = FrameManager()
    frame_manager.frames[-1].add_border()
    print(frame_manager.terminal.size)
    """
    first_frame: Frame = frame_manager.frames[-1]
    first_frame.add_border()

    second_frame: Frame = frame_manager.splitv(first_frame)
    second_frame.add_border()

    third_frame: Frame = frame_manager.splith(second_frame)
    third_frame.add_border()
    """

    for i in range(4):
        frame_manager.splitv(frame_manager.frames[-1]).add_border()
        frame_manager.splith(frame_manager.frames[-1]).add_border()
    # print frame -> intended way
    # frame_manager.print() 
    
    # manual print (no \n when program exits (no loop due to no events in example
    frame_manager._update_chars()
    print(frame_manager, end='')
    input()
