"""

"""

import io
from contextlib import redirect_stdout
from wing_core import *
from wing_parser import *

def parse_source(source):
	"""
	Converts the given string into AST.
	"""
	return wing_parse(source)


def load_source(filename):
	"""
	Returns the AST for the file provided.
	"""
	setup_sym_tab()
	with open(filename) as source:
		return parse_source(source.read())


def capture_stdout(ast):
	"""
	Runs the given AST node and returns what was printed to STDOUT (if any).
	"""
	setup_sym_tab()

	wrapper = io.StringIO()
	with redirect_stdout(wrapper):
		handle_expression(ast)
	return wrapper.getvalue()
