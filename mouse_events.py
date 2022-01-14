""" Mouse input test """

from os import system, read
from sys import stdout, stdin


def disable_mouse() -> None:
    stdout.write("\x1b[?1000;1003;1006;1015l")
    system("stty echo")


if __name__ == '__main__':
    system("stty -icanon")
    system("stty -echo")
    stdout.write("\x1b[?1000;1003;1006;1015h")

    key_codes: dict = {
        "35M": "Mouse Move",
        "0M": "Left click hold",
        "0m": "Left click release",
        "32M": "Left click drag",
        "2M": "Right click hold",
        "2m": "Right click release",
        "34M": "Right click drag",
        "65M": "Scroll down",
        "64M": "Scroll up",
        "1M": "Middle click hold",
        "1m": "Middle click release",
        "33M": "Middle click drag"
    }

    try:
        while True:
            line: str = read(stdin.fileno(), 16).decode()
            info = line.split("\x1b[<", -1)[-1]  # type;column;row
            info = info.split(";", -1)
            
            try:
                code = key_codes[f"{info[0]}{info[-1][-1]}"]
                print(f"{info[1]};{info[2]}  {code}")
            except KeyError as e:
                print(e)

    except KeyboardInterrupt:
        disable_mouse()
    except BaseException as e:
        disable_mouse()
        raise e
        


