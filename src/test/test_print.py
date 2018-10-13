try:
	import context
except ImportError:
	from . context import *
finally:
	from wing_test_utils import *


def test_print_str():
	"""
	Test to see if the print function will print a string value.
	"""
	source = \
	"""
	Program:
	[
		print: ["Hello World!"]
	]
	"""
	assert(capture_stdout(parse_source(source)) == 'Hello World!\n')


def test_print_int():
	"""
	Test to see if the print function will print an int value.
	"""
	source = \
	"""
	Program:
	[
		print: [123]
	]
	"""
	assert(capture_stdout(parse_source(source)) == '123\n')


def test_print_float():
	"""
	Test to see if the print function will print a float value.
	"""
	source = \
	"""
	Program:
	[
		print: [3.14]
	]
	"""
	assert(capture_stdout(parse_source(source)) == '3.14\n')


def test_print_bool():
	"""
	Test to see if the print function will print a bool value.
	"""
	source = \
	"""
	Program:
	[
		print: [True]
	]
	"""
	assert(capture_stdout(parse_source(source)) == 'True\n')


def test_print_float():
	"""
	Test to see if the print function will print a dict value.
	"""
	source = \
	"""
	Program:
	[
		print: [hash: [name Pebaz age 23]]
	]
	"""
	assert(capture_stdout(parse_source(source)) == "{'name': 'Pebaz', 'age': 23}\n")


if __name__ == '__main__':
	test_print_str()
	test_print_int()
	test_print_float()
