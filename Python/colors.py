# By Pytel

"""
Color codes for terminal.

Sources:   
https://replit.com/talk/learn/ANSI-Escape-Codes-in-Python/22803
https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
"""

from sys import stdout, stdin
from time import sleep

# Reset
Color_Off = '\033[0m'       # Text Reset
NC = '\033[0m'

# Regular Colors
Black = '\033[0;30m'        # Black
Red = '\033[0;31m'          # Red
Green = '\033[0;32m'        # Green
Yellow = '\033[0;33m'       # Yellow
Blue = '\033[0;34m'         # Blue
Purple = '\033[0;35m'       # Purple
Cyan = '\033[0;36m'         # Cyan
White = '\033[0;37m'        # White

# Bold
BBlack = '\033[1;30m'       # Black
BRed = '\033[1;31m'         # Red
BGreen = '\033[1;32m'       # Green
BYellow = '\033[1;33m'      # Yellow
BBlue = '\033[1;34m'        # Blue
BPurple = '\033[1;35m'      # Purple
BCyan = '\033[1;36m'        # Cyan
BWhite = '\033[1;37m'       # White

# Underline
UBlack = '\033[4;30m'       # Black
URed = '\033[4;31m'         # Red
UGreen = '\033[4;32m'       # Green
UYellow = '\033[4;33m'      # Yellow
UBlue = '\033[4;34m'        # Blue
UPurple = '\033[4;35m'      # Purple
UCyan = '\033[4;36m'        # Cyan
UWhite = '\033[4;37m'       # White

# Background
On_Black = '\033[40m'       # Black
On_Red = '\033[41m'         # Red
On_Green = '\033[42m'       # Green
On_Yellow = '\033[43m'      # Yellow
On_Blue = '\033[44m'        # Blue
On_Purple = '\033[45m'      # Purple
On_Cyan = '\033[46m'        # Cyan
On_White = '\033[47m'       # White

# High Intensity
IBlack = '\033[0;90m'       # Black
IRed = '\033[0;91m'         # Red
IGreen = '\033[0;92m'       # Green
IYellow = '\033[0;93m'      # Yellow
IBlue = '\033[0;94m'        # Blue
IPurple = '\033[0;95m'      # Purple
ICyan = '\033[0;96m'        # Cyan
IWhite = '\033[0;97m'       # White

# Bold High Intensity
BIBlack = '\033[1;90m'      # Black
BIRed = '\033[1;91m'        # Red
BIGreen = '\033[1;92m'      # Green
BIYellow = '\033[1;93m'     # Yellow
BIBlue = '\033[1;94m'       # Blue
BIPurple = '\033[1;95m'     # Purple
BICyan = '\033[1;96m'       # Cyan
BIWhite = '\033[1;97m'      # White

# High Intensity backgrounds
On_IBlack = '\033[0;100m'   # Black
On_IRed = '\033[0;101m'     # Red
On_IGreen = '\033[0;102m'   # Green
On_IYellow = '\033[0;103m'  # Yellow
On_IBlue = '\033[0;104m'    # Blue
On_IPurple = '\033[0;105m'  # Purple
On_ICyan = '\033[0;106m'    # Cyan
On_IWhite = '\033[0;107m'   # White


class fg:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"


class bg:
    black = "\u001b[40m"
    red = "\u001b[41m"
    green = "\u001b[42m"
    yellow = "\u001b[43m"
    blue = "\u001b[44m"
    magenta = "\u001b[45m"
    cyan = "\u001b[46m"
    white = "\u001b[47m"

    def rgb(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"


class util:
    reset = "\u001b[0m"
    bold = "\u001b[1m"
    underline = "\u001b[4m"
    reverse = "\u001b[7m"
    clear = "\u001b[2J"
    clearline = "\u001b[2K"
    up = "\u001b[1A"
    down = "\u001b[1B"
    right = "\u001b[1C"
    left = "\u001b[1D"
    nextline = "\u001b[1E"
    prevline = "\u001b[1F"
    top = "\u001b[0;0H"

    def to(x, y):
        return f"\u001b[{y};{x}H"

    def write(text="\n"):
        stdout.write(text)
        stdout.flush()

    def writew(text="\n", wait=0.5):
        for char in text:
            stdout.write(char)
            stdout.flush()
            sleep(wait)

    def read(begin=""):
        text = ""
        stdout.write(begin)
        stdout.flush()
        while True:
            char = ord(stdin.read(1))

            if char == 3:
                return
            elif char in (10, 13):
                return text
            else:
                text += chr(char)

    def readw(begin="", wait=0.5):
        text = ""
        for char in begin:
            stdout.write(char)
            stdout.flush()
            sleep(wait)
        while True:
            char = ord(stdin.read(1))

            if char == 3:
                return
            elif char in (10, 13):
                return text
            else:
                text += chr(char)

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

if __name__ == "__main__":
    print_format_table()

# END
