"""
The wing_core.py must be able to be imported by everyone so that extensions can
be made.
"""

def wing_func1(*args):
	print("wing_func1!!!")

def wing_func2(*args):
	print("wing_func2!!!")

__wing__ = {
	"func1" : wing_func1,
	"func2" : wing_func2
}
