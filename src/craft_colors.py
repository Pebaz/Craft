"""
A collection of constants for use in making the usage of terminal coloring as
simple as possible.
These constants can be used very easily by taking advantage of Python's built-
in string format literal:
>>> age = 
"""

import colorama

colorama.init(convert=True)

# Foreground Colors
_CLRfbl = colorama.Fore.BLACK
_CLRfr = colorama.Fore.RED
_CLRfg = colorama.Fore.GREEN
_CLRfy = colorama.Fore.YELLOW
_CLRfb = colorama.Fore.BLUE
_CLRfm = colorama.Fore.MAGENTA
_CLRfc = colorama.Fore.CYAN
_CLRfw = colorama.Fore.WHITE
_CLRfreset = colorama.Fore.RESET

# Background Colors
_CLRbbl = colorama.Back.BLACK
_CLRbr = colorama.Back.RED
_CLRbg = colorama.Back.GREEN
_CLRby = colorama.Back.YELLOW
_CLRbb = colorama.Back.BLUE
_CLRbm = colorama.Back.MAGENTA
_CLRbc = colorama.Back.CYAN
_CLRbw = colorama.Back.WHITE
_CLRbreset = colorama.Back.RESET

# Styles
_CLRreset = colorama.Style.RESET_ALL

__all__ = [i for i in globals() if i.startswith("_CLR")]

if __name__ == "__main__":
    print(f"This color is {_CLRfg}green{_CLRreset}!")
