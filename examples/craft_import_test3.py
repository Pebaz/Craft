"""
The craft_core.py must be able to be imported by everyone so that extensions can
be made.
"""


def craft_func1(*args):
    print("craft_func1!!!")


def craft_func2(*args):
    print("craft_func2!!!")


__craft__ = {"func1": craft_func1, "func2": craft_func2}
