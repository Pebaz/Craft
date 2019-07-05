try:
	import context
except ImportError:
	from . context import *
finally:
	from craft_test_utils import *


def test_add_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [+: [1 2]]
		""",
		"""
		3
		"""
	)


def test_add_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [+: [1.1 2.1]]
		""",
		"""
		3.2
		"""
	)


def test_add_neg_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [+: [neg: [1] 2]]
		""",
		"""
		1
		"""
	)


def test_add_neg_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [+: [neg: [1.1] 2.1]]
		""",
		"""
		1.0
		"""
	)


def test_sub_int():
	""""""
	
	run_test_program(
		"""
		print: [-: [1 2]]
		""",
		"""
		-1
		"""
	)


def test_sub_float():
	""""""
	
	run_test_program(
		"""
		print: [-: [1.1 2.1]]
		""",
		"""
		-1.0
		"""
	)


def test_sub_neg_int():
	""""""
	
	run_test_program(
		"""
		print: [-: [neg: [1] 2]]
		""",
		"""
		-3
		"""
	)


def test_sub_neg_float():
	""""""
	
	run_test_program(
		"""
		print: [-: [neg: [1.1] 2.1]]
		""",
		"""
		-3.2
		"""
	)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
