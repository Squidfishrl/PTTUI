from os import get_terminal_size
from typing import Callable, Any 

class Terminal:
    """ 
    Class that holds useful information about the terminal
    Currently only size, and resize check
    """

    def __init__(self) -> None:
        self.size: terminal_size = get_terminal_size()
        self.listeners: set[Callable[..., Any]] = set() 

    @property
    def columns(self) -> int:
        """ Return the amount of columns that can be shown at once """

        return self.size[0]

    @property
    def rows(self) -> int:
        """ Return the amount of rows that can be shown at once """

        return self.size[1]

    def update(self) -> None:
        """ 
        Check for terminal size update 
        Update size and call listeners if so
        """

        size = get_terminal_size()  # get current terminal size
        
        if size != self.size:  # check if old size is different
            self.size = size  # update size
            
            # call listeners
            for callback in self.listeners:
                callback()


    def on_resize(self, callback: Callable[..., Any]) -> None:
        """ Subscribes callback function to resize event """

        self.listeners.add(callback)

    def unsubsribe(self, callback: Callable[..., Any]) -> None:
        """ Unsubscribe a function from resize event """

        self.listeners.remove(callback)



if __name__ == '__main__':

    term: Terminal = Terminal()

    def resize():
        print(f"New size: {term.rows};{term.columns}")

    term.on_resize(resize)


    while True:
        term.update()





        

