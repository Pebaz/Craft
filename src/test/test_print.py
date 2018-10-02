from . context import wing_test_utils

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
	ast = wing_test_utils.parse_source(source)
	assert(wing_test_utils.capture_stdout(ast) == 'Hello World!\n')
