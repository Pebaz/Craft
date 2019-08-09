"""
A collection of constants for use in making the usage of terminal coloring as
simple as possible.
These constants can be used very easily along with the Craft `format` function.

print: [fmt: ["{0}Hello{1} again {0}World!{1}" $_CLRfb $_CLRreset]]
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

__craft__ = {
	i : globals()[i]
	for i in globals() if i.startswith('_CLR')
}
