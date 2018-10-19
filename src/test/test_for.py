try:
	import context
except ImportError:
	from . context import *
finally:
	from wing_test_utils import *


def test_for_stop():
	"""
	Test to see if the print function will print a string value.
	"""
	run_test_program(
		"""
		for:
		[
			[i 3]
			print: [$i]
		]
		""",
		"""
		0
		1
		2
		"""
	)


def test_for_scoping():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	run_test_program(
		"""
		for:
		[
			[i 3]
			print: [$i]
		]
		try:
		[
			
		]
		""",
		"""
		0
		1
		2
		"""
	)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
