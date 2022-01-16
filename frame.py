class Frame():

    """
    Class that creates a frame for a widget
    Frames should be used similarly to a tiling window manager
    There's one main frame, allowing one window - or in this case one widget
    The frame can then be split vertically (splitv) or horizontally (splith) by the frame manager
    Manages frame manages widget position, when terminal resizes for unified looks
    """

    def __init__(self, rows: int, columns: int, top_left_point: tuple[int]) -> None:
        """ Initialize a frame which covers the entire screen """ 
        self.rows: int = rows 
        self.columns: int = columns 

        self.top_left_point: tuple[int] = top_left_point 

        # matrix holding how the frame should look in the temrinal
        self.chars: list[list[str]] = [ [' ' for i in range(columns)] for row in range(rows)] 

    def add_border(self):
        """
        add a border to the frame 
        useful for visualization and debug
        OPT: use list comprehension for better performance? tradeoff readability
        """

        for row_count, row in enumerate(self.chars):
            for column_count, char in enumerate(row):
                if column_count == 0 or column_count == self.columns - 1:
                    self.chars[row_count][column_count] = "║"

                if row_count == 0 or row_count == self.rows - 1:
                    self.chars[row_count][column_count] = "═"

        # fix corner pieces
        self.chars[0][0] = '╔'
        self.chars[0][-1] = '╗'
        self.chars[-1][-1] = '╝'
        self.chars[-1][0] = '╚'



    def resize(self) -> None:
        """
        Resizes frame on terminal resize
        Frame manager should subscribe this function to the term event
        """
        pass

    def __str__(self) -> str:
        """
        Converts 'self.chars' to a string
        Mainly used for visualization and debug of individual frames
        TODO: use list comprehension here
        """

        buffer: str =  ""

        for row_count, row in enumerate(self.chars):

            for char in row:
                buffer += f"{char}"

            if row_count != self.rows - 1:
                buffer += f"\n"



        return buffer





