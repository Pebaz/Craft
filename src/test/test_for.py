try:
	import context
except ImportError:
	from . context import *
finally:
	from wing_test_utils import *

import textwrap

def test_print_stop():
	"""
	Test to see if the print function will print a string value.
	"""

	source = \
	"""
	Program:
	[
		for:
		[
			[i 3]
			print: [$i]
		]
	]
	"""

	result = textwrap.dedent(
		"""
		0
		1
		2
		"""
	)
	assert(capture_stdout(parse_source(source)) == result)


if __name__ == '__main__':
	test_for_stop()
