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


if __name__ == '__main__':
	test_print_str()