from enum import Enum, auto
from os import system, read
from sys import stdout, stdin
from typing import Callable, Any


class Input:
    """
    Class that manages mouse and keyboard input
    Listening and reading from input and event callback subscriptions(TODO)
    """

    def __init__(self) -> None:
        self.mouse: Mouse = Mouse() 
        self.keyboard: Keyboard = Keyboard()


    def start_listen(self) -> None: 
        """
        Start listening for input
        Essentially allows the mouse to be used
        """

        system("stty -icanon")  # enable shell input
        system("stty -echo")  # disable characters printing

        stdout.write("\x1b[?1000;1003;1006;1015h")  # trap input
        stdout.flush()  # flush stdout buffer

    def stop_listen(self) -> None:
        """
        TODO: Call on program exit
        """

        stdout.write("\x1b[?1000;1003;1006;1015l")  # disable trap 
        stdout.flush()  # flush stdout buffer
        system("stty echo")  # enable characters printing

    def read_input(self) -> str:
        """
        Reads 16 bytes from stdin (max you can get when reading mouse input is that much)
        TODO: option to disable mouse to optimize reading to 1 byte at a time (shouldn't really make a difference but who knows)

        Checks if the read input belongs to a mouse or a keyboard and saves to them accordingly

        Mouse input would look something like:
        \x1b[<35;24;54M
        where 35 is the mouse event code (move pointer)
        24 is the row as a character in the terminal
        54 is the column in characters
        M indicates that the input isn't released
        m would be lower case on button release
        """

        line: str = read(stdin.fileno(), 16).decode()  # convert bytes to str

        if len(line) > 1:  # Input from mouse - format it 
            line = line.split("\x1b[<", -1)[-1]  # remove escape if there is one
            line: list[str] = line.split(";", -1)  # split into an array of code, row, column
            line.append(line[-1][-1])  # add M/m as last element of array
            line[-2] = line[-2][:-1]  # Remove the M from columns

            self.mouse.update(line)  # update mouse coords and callback on event
        else:
            self.keyboard.update(line)


class MouseEvent(Enum):
    """ An enumeration of all the polled mouse events """

    """ Mouse pointer moves when left/right/middle click isn't held """
    POINTER_MOVE: str = "35M" 

    """ Left click is pressed (and not released) """
    LEFT_CLICK_HOLD: str = "0M"

    """ Mouse pointer moves while left click is held """
    LEFT_CLICK_DRAG: str = "32M"

    """ Left click is released (no longer pressed) """
    LEFT_CLICK_RELEASE: str = "0m" 

    """ Right click is pressed (and not released) """
    RIGHT_CLICK_HOLD: str = "2M" 

    """ Mouse pointer moves while right click is held """
    RIGHT_CLICK_DRAG: str = "34M"

    """ Right click is released (no longer pressed) """
    RIGHT_CLICK_RELEASE: str = "2m"

    """ Middle click is pressed (and not released) """
    MIDDLE_CLICK_HOLD: str = "1M" 

    """ Mouse pointer moves while middle click is held """
    MIDDLE_CLICK_DRAG: str = "33M"

    """ Middle click is released (no longer pressed) """
    MIDDLE_CLICK_RELEASE: str = "1m"

    """ Upwards scroll """
    SCROLL_UP: str = "64M"

    """ Downwards scroll """
    SCROLL_DOWN: str = "65M"


class Mouse:
    """ Class that manages mouse position in character, last mouse event, and subscriptions """

    def __init__(self):
        self.row: int = -1
        self.column: int = -1
        self.last_event: MouseEvent = None

        self.subscriptions: dict[MouseEvent, set[Callable[..., Any]]] = {}

    def update(self, input_: list[str]):
        """
        input_ should be passed by Input.read_input
        and should contain [code, row, column, M/m]
        M - action, m - release event
        updates mouse position and last event
        updating last event will trigger callback functions if one is set
        """

        code = f"{input_[0]}{input_[-1]}"  # get mouse input code example: 35M
        self.row = input_[2]  # update mouse row pos
        self.column = input_[1]  # update mouse column pos
        self.last_event = self.get_event(code)
        print(f"Row {self.row}  Column {self.column}  {MouseEvent(code).name}")

        # call all functions, subscribed to the event
        try:
            for callback in self.subscriptions[self.last_event]:
                callback()
        except KeyError: 
            pass  # event has never had any subscribtions

    def get_event(self, code: str) -> MouseEvent:
        """
        Given a mouse input event code, convert it to the representing event
        """

        try:
            return MouseEvent(code).name
        except Exception as e:
            prZZint(e)

    def subscribe(self, event: MouseEvent, callback: Callable[..., Any]):
        """ Subscribe a function to an event. Duplicate callbacks cannot be added (no effect) """
        if self.subscriptions.get(event) is None:  # Check if event entry exists
            # event subscribtions are a set to avoid duplicate callback functions
            self.subscriptions[event] = set()  # add an empty set as a value

        self.subscriptions[event].add(callback)  # append function to callback

    def unsubscribe(self, event: MouseEvent, callback: Callable[..., Any]):
        """
        Unsibscribe a function from an event
        Raise a (TODO: Custom) Error if callback doesn't exist 
        """

        try:
            self.subscriptions[event].remove(callback)
        except KeyError:
            raise Exception("Callback doesn't exist.")


class Keyboard:
    """ TODO: HOTKEYS """

    def __init__(self):
        self.last_press: str = ''
        self.subscriptions: dict[str, set[Callable[..., Any]]] = {}

    def update(self, input_: str):
        """
        input_ should be passed by Input.read_input
        should always be 1 character long
        TODO: hotkey support
        """

        self.last_press = input_
        print(self.last_press)

        try:
            for callback in self.subscriptions[self.last_press]:
                callback()
        except KeyError: 
            pass  # event has never had any subscribtions

    def subscribe(self, event: str, callback: Callable[..., Any]):
        """ Subscribe a function to a keyboard button press. Duplicate callbacks cannot be added (no effect) """
        if self.subscriptions.get(event) is None:  # Check if event entry exists
            # event subscribtions are a set to avoid duplicate callback functions
            self.subscriptions[event] = set()  # add an empty set as a value

        self.subscriptions[event].add(callback)  # append function to callback

    def unsubscribe(self, event: MouseEvent, callback: Callable[..., Any]):
        """
        Unsibscribe a function from an event
        Raise a (TODO: Custom) Error if callback doesn't exist 
        """

        try:
            self.subscriptions[event].remove(callback)
        except KeyError:
            raise Exception("Callback doesn't exist.")




if __name__ == '__main__':
    def click():
        print("Left click subscription")
    def click2():
        print("Left click2")

    input_manager: Input = Input()
    input_manager.start_listen()
    input_manager.mouse.subscribe(MouseEvent.LEFT_CLICK_HOLD, click)
    input_manager.mouse.subscribe(MouseEvent.LEFT_CLICK_HOLD, click2)
    input_manager.mouse.unsubscribe(MouseEvent.LEFT_CLICK_HOLD, click2)

    while True:
        try:
            input_manager.read_input()

        except KeyboardInterrupt:
            input_manager.stop_listen()
            exit(0)
        except BaseException as e:
            input_manager.stop_listen()
            raise(e)


