try:
	import context
except ImportError:
	from . context import *
finally:
	from wing_test_utils import *


def test_set_int():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [age 24]
		""",
		"""
		"""
	)
	assert(query_symbol_table('age', SCOPE) == 24)


def test_set_float():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [age 25.0]
		""",
		"""
		"""
	)
	assert(query_symbol_table('age', SCOPE) == 25.0)


def test_set_str_no_quotes():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [name Pebaz]
		""",
		"""
		"""
	)
	assert(query_symbol_table('name', SCOPE) == 'Pebaz')


def test_set_str_double_quotes():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [name "Pebaz"]
		""",
		"""
		"""
	)
	assert(query_symbol_table('name', SCOPE) == 'Pebaz')


def test_set_str_single_quotes():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [name 'Pebaz']
		""",
		"""
		"""
	)
	assert(query_symbol_table('name', SCOPE) == 'Pebaz')


def test_set_bool():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [alive True]
		""",
		"""
		"""
	)
	assert(query_symbol_table('alive', SCOPE) == True)


def test_set_list():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [nums list: [[1 2 3]]]
		""",
		"""
		"""
	)
	assert(query_symbol_table('nums', SCOPE) == [1, 2, 3])


def test_set_dict():
	"""
	Test and see if the for loop counter is destroyed when out of scope.
	"""
	
	run_test_program(
		"""
		set: [ages hash: [Pebaz 24 Protodip 27 Yelbu 22]]
		""",
		"""
		"""
	)
	assert(
		query_symbol_table('ages', SCOPE) == dict(
			Pebaz=24, Protodip=27, Yelbu=22
		)
	)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
