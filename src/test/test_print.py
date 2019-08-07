try:
	import context
except ImportError:
	from . context import *
finally:
	from craft_test_utils import *



def test_print_var():
	"""
	Test to see if the print function will print a string value.
	"""
	source = \
	"""
	Program:
	[
		set: [age 24]
		print: [$age]
	]
	"""
	result = '24\n'
	assert(capture_stdout(parse_source(source)) == result)


def test_print_byval_var():
	"""
	Test to see if the print function will print a string value.
	"""
	source = \
	"""
	Program:
	[
		set: [age 24]
		print: [$$age]
	]
	"""
	result = '$age\n'
	assert(capture_stdout(parse_source(source)) == result)


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
	result = 'Hello World!\n'
	assert(capture_stdout(parse_source(source)) == result)


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
	result = '123\n'
	assert(capture_stdout(parse_source(source)) == result)


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
	result = '3.14\n'
	assert(capture_stdout(parse_source(source)) == result)


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
	result = 'True\n'
	assert(capture_stdout(parse_source(source)) == result)


def test_print_dict():
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
	result = "{'name': 'Pebaz', 'age': 23}\n"
	assert(capture_stdout(parse_source(source)) == result)


def test_print_list():
	"""
	Test to see if the print function will print a dict value.
	"""
	source = \
	"""
	Program:
	[
		print: [[name Pebaz age 23]]
	]
	"""
	result = "['name', 'Pebaz', 'age', 23]\n"
	assert(capture_stdout(parse_source(source)) == result)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
