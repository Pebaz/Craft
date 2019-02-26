"""
Various utilities to reduce the amount of code needed to write a test case.
"""

import io
from contextlib import redirect_stdout
from wing_core import *
from wing_parser import *
import textwrap


PROGRAM = \
"""
Program:
[
%s
]
"""


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

def dedent_result(result):
	"""
	Since the result of each test is stored in a block string within the test,
	this requires that extra whitespace be removed on the left margin.
	"""
	return textwrap.dedent(result)


def capture_stdout(ast):
	"""
	Runs the given AST node and returns what was printed to STDOUT (if any).
	"""
	setup_sym_tab()

	wrapper = io.StringIO()
	with redirect_stdout(wrapper):
		handle_expression(ast)
	return wrapper.getvalue()


def run_test(source, expected_result):
	"""
	Test to see if the print function will print a string value.
	"""
	output = capture_stdout(parse_source(source)).strip()
	assert(output == expected_result)


def run_test_program(source, expected_result):
	"""
	"""
	run_test(PROGRAM % source, dedent_result(expected_result).strip())
