try:
	import context
except ImportError:
	from . context import *
finally:
	from wing_test_utils import *


def test_for_stop():
	"""
	For loop handle stop value.
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


def test_for_start():
	"""
	For loop handle start and stop values.
	"""
	run_test_program(
		"""
		for:
		[
			[i 2 10]
			print: [$i]
		]
		""",
		"""
		2
		3
		4
		5
		6
		7
		8
		9
		"""
	)


def test_for_step():
	"""
	For loop handle start, stop, and step values.
	"""
	run_test_program(
		"""
		for:
		[
			[i 1 10 2]
			print: [$i]
		]
		""",
		"""
		1
		3
		5
		7
		9
		"""
	)


def test_for_break():
	"""
	For loop handle breaking in the middle.
	"""
	run_test_program(
		"""
		for:
		[
			[i 10]
			print: [$i]
			if:
			[
				=: [$i 5]
				break: []
			]
		]
		""",
		"""
		0
		1
		2
		3
		4
		5
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
			[hidden-var 3]
			print: [$hidden-var]
		]

		try:
		[
			print: [$hidden-var]
			catch:
			[
				[] :: Catch any error
				print: ["Variable was hidden"]
			]
		]
		""",
		"0\n1\n2\nVariable was hidden"
	)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
