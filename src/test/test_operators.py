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


def test_add_str():
	""""""
	
	run_test_program(
		"""
		print: [+: [one two]]
		""",
		"""
		onetwo
		"""
	)


def test_add_list():
	""""""
	
	run_test_program(
		"""
		print: [+: [[1] [2]]]
		""",
		"""
		[1, 2]
		"""
	)


def test_add_tuple():
	""""""
	
	run_test_program(
		"""
		print: [+: [
			tuple: [[1]]
			tuple: [[2]]
		]]
		""",
		"""
		(1, 2)
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


def test_mul_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [*: [1 2]]
		""",
		"""
		2
		"""
	)


def test_mul_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [*: [1.1 2.1]]
		""",
		"""
		2.3100000000000005
		"""
	)


def test_mul_neg_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [*: [neg: [1] 2]]
		""",
		"""
		-2
		"""
	)


def test_mul_neg_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [*: [neg: [1.1] 2.1]]
		""",
		"""
		-2.3100000000000005
		"""
	)


def test_mul_str_int():
	""""""
	
	run_test_program(
		"""
		print: [*: [one 2]]
		""",
		"""
		oneone
		"""
	)


def test_mul_list_int():
	""""""
	
	run_test_program(
		"""
		print: [*: [[1] 2]]
		""",
		"""
		[1, 1]
		"""
	)


def test_mul_tuple_int():
	""""""
	
	run_test_program(
		"""
		print: [*: [
			tuple: [[1]]
			2
		]]
		""",
		"""
		(1, 1)
		"""
	)


def test_div_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [/: [1 2]]
		""",
		"""
		0.5
		"""
	)


def test_div_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [/: [1.1 2.1]]
		""",
		"""
		0.5238095238095238
		"""
	)


def test_div_neg_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [/: [neg: [1] 2]]
		""",
		"""
		-0.5
		"""
	)


def test_div_neg_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		print: [/: [neg: [1.1] 2.1]]
		""",
		"""
		-0.5238095238095238
		"""
	)


def test_add_eq_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		set: [var 1]
		+=: [$var 2]
		print: [$var]
		""",
		"""
		3
		"""
	)


def test_add_eq_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		set: [var 1.1]
		+=: [$var 2.1]
		print: [$var]
		""",
		"""
		3.2
		"""
	)


def test_add_eq_neg_int():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		set: [var neg: [1]]
		+=: [$var 2]
		print: [$var]
		""",
		"""
		1
		"""
	)


def test_add_eq_neg_float():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		set: [var neg: [1.1]]
		+=: [$var 2.1]
		print: [$var]
		""",
		"""
		1.0
		"""
	)


def test_add_eq_str():
	""""""
	
	run_test_program(
		"""
		set: [var one]
		+=: [$var two]
		print: [$var]
		""",
		"""
		onetwo
		"""
	)


def test_add_eq_list():
	""""""
	
	run_test_program(
		"""
		set: [var [1]]
		+=: [$var [2]]
		print: [$var]
		""",
		"""
		[1, 2]
		"""
	)


def test_add_eq_tuple():
	""""""
	
	run_test_program(
		"""
		set: [var tuple: [[1]]]
		+=: [$var tuple: [[2]]]
		print: [$var]
		""",
		"""
		(1, 2)
		"""
	)


def test_sub_eq_int():
	""""""
	
	run_test_program(
		"""
		set: [var 1]
		-=: [$var 2]
		print: [$var]
		""",
		"""
		-1
		"""
	)


def test_sub_eq_float():
	""""""
	
	run_test_program(
		"""
		set: [var 1.1]
		-=: [$var 2.1]
		print: [$var]
		""",
		"""
		-1.0
		"""
	)


def test_sub_eq_neg_int():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [1]]
		-=: [$var 2]
		print: [$var]
		""",
		"""
		-3
		"""
	)


def test_sub_eq_neg_float():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [1.1]]
		-=: [$var 2.1]
		print: [$var]
		""",
		"""
		-3.2
		"""
	)


def test_mul_eq_int():
	""""""
	
	run_test_program(
		"""
		set: [var 1]
		*=: [$var 2]
		print: [$var]
		""",
		"""
		2
		"""
	)


def test_mul_eq_float():
	""""""
	
	run_test_program(
		"""
		set: [var 1.1]
		*=: [$var 2.1]
		print: [$var]
		""",
		"""
		2.3100000000000005
		"""
	)


def test_mul_eq_neg_int():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [1]]
		*=: [$var 2]
		print: [$var]
		""",
		"""
		-2
		"""
	)


def test_mul_eq_neg_float():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [1.1]]
		*=: [$var 2.1]
		print: [$var]
		""",
		"""
		-2.3100000000000005
		"""
	)


def test_mul_eq_str_int():
	""""""
	
	run_test_program(
		"""
		set: [var one]
		*=: [$var 2]
		print: [$var]
		""",
		"""
		oneone
		"""
	)


def test_mul_eq_list_int():
	""""""
	
	run_test_program(
		"""
		set: [var [1]]
		*=: [$var 2]
		print: [$var]
		""",
		"""
		[1, 1]
		"""
	)


def test_mul_eq_tuple_int():
	""""""
	
	run_test_program(
		"""
		set: [var tuple: [[1]]]
		*=: [$var 2]
		print: [$var]
		""",
		"""
		(1, 1)
		"""
	)


def test_div_eq_int():
	""""""
	
	run_test_program(
		"""
		set: [var 1]
		/=: [$var 2]
		print: [$var]
		""",
		"""
		0.5
		"""
	)


def test_div_eq_float():
	""""""
	
	run_test_program(
		"""
		set: [var 1.1]
		/=: [$var 2.1]
		print: [$var]
		""",
		"""
		0.5238095238095238
		"""
	)


def test_div_eq_neg_int():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [1]]
		/=: [$var 2]
		print: [$var]
		""",
		"""
		-0.5
		"""
	)


def test_div_eq_neg_float():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [1.1]]
		/=: [$var 2.1]
		print: [$var]
		""",
		"""
		-0.5238095238095238
		"""
	)


def test_mod_int():
	""""""
	
	run_test_program(
		"""
		print: [%: [10 2]]
		""",
		"""
		0
		"""
	)


def test_mod_eq_int():
	""""""
	
	run_test_program(
		"""
		set: [var 10]
		%=: [$var 2]
		print: [$var]
		""",
		"""
		0
		"""
	)


def test_mod_float():
	""""""
	
	run_test_program(
		"""
		print: [%: [3.14 2]]
		""",
		"""
		1.1400000000000001
		"""
	)


def test_mod_eq_float():
	""""""
	
	run_test_program(
		"""
		set: [var 3.14]
		%=: [$var 2]
		print: [$var]
		""",
		"""
		1.1400000000000001
		"""
	)


def test_mod_neg_int():
	""""""
	
	run_test_program(
		"""
		print: [%: [neg: [10] 4]]
		""",
		"""
		2
		"""
	)


def test_mod_eq_neg_int():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [10]]
		%=: [$var 4]
		print: [$var]
		""",
		"""
		2
		"""
	)


def test_mod_neg_float():
	""""""
	
	run_test_program(
		"""
		print: [%: [neg: [3.14] 2]]
		""",
		"""
		0.8599999999999999
		"""
	)


def test_mod_eq_neg_float():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [3.14]]
		%=: [$var 2]
		print: [$var]
		""",
		"""
		0.8599999999999999
		"""
	)


def test_exp_int():
	""""""
	
	run_test_program(
		"""
		print: [**: [10 2]]
		""",
		"""
		100
		"""
	)


def test_exp_eq_int():
	""""""
	
	run_test_program(
		"""
		set: [var 10]
		**=: [$var 2]
		print: [$var]
		""",
		"""
		100
		"""
	)


def test_exp_float():
	""""""
	
	run_test_program(
		"""
		print: [**: [3.14 2]]
		""",
		"""
		9.8596
		"""
	)


def test_exp_eq_float():
	""""""
	
	run_test_program(
		"""
		set: [var 3.14]
		**=: [$var 2]
		print: [$var]
		""",
		"""
		9.8596
		"""
	)


def test_exp_neg_int():
	""""""
	
	run_test_program(
		"""
		print: [**: [neg: [10] 4]]
		""",
		"""
		10000
		"""
	)


def test_exp_eq_neg_int():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [10]]
		**=: [$var 4]
		print: [$var]
		""",
		"""
		10000
		"""
	)


def test_exp_neg_float():
	""""""
	
	run_test_program(
		"""
		print: [**: [neg: [3.14] 2]]
		""",
		"""
		9.8596
		"""
	)


def test_exp_eq_neg_float():
	""""""
	
	run_test_program(
		"""
		set: [var neg: [3.14]]
		**=: [$var 2]
		print: [$var]
		""",
		"""
		9.8596
		"""
	)


def test_equals():
	""""""
	
	run_test_program(
		"""
		print: [=: [a a]]
		print: [=: [a b]]
		print: [=: [1 1.0]]
		print: [=: ["1" 1]]
		""",
		"""
		True
		False
		True
		False
		"""
	)


def test_not_equals():
	""""""
	
	run_test_program(
		"""
		print: [!=: [a a]]
		print: [!=: [a b]]
		print: [!=: [1 1.0]]
		print: [!=: ["1" 1]]
		""",
		"""
		False
		True
		False
		True
		"""
	)


def test_greater_than():
	""""""
	
	run_test_program(
		"""
		print: [>: [2 1]]
		print: [>: [2.0 1.0]]
		print: [>: [2.0 57]]
		""",
		"""
		True
		True
		False
		"""
	)


def test_less_than():
	""""""
	
	run_test_program(
		"""
		print: [<: [2 1]]
		print: [<: [2.0 1.0]]
		print: [<: [2.0 57]]
		""",
		"""
		False
		False
		True
		"""
	)


def test_greater_than_or_equal_to():
	""""""
	
	run_test_program(
		"""
		print: [>=: [2 1]]
		print: [>=: [2.0 1.0]]
		print: [>=: [2.0 57]]
		print: [>=: [2 2]]
		print: [>=: [2.0 2.0]]
		""",
		"""
		True
		True
		False
		True
		True
		"""
	)


def test_less_than_or_equal_to():
	""""""
	
	run_test_program(
		"""
		print: [<=: [2 1]]
		print: [<=: [2.0 1.0]]
		print: [<=: [2.0 57]]
		print: [<=: [2 2]]
		print: [<=: [2.0 2.0]]
		""",
		"""
		False
		False
		True
		True
		True
		"""
	)


def test_bitwise_and():
	""""""
	
	run_test_program(
		"""
		print: [&: [2 1]]
		print: [&: [100 101]]
		print: [&: [101 neg: [1]]]
		print: [&: [101 100]]
		""",
		"""
		0
		100
		101
		100
		"""
	)


def test_bitwise_and_eq():
	""""""
	
	run_test_program(
		"""
		set: [var 2]
		&=: [$var 1]
		print: [$var]
		set: [var 100]
		&=: [$var 101]
		print: [$var]
		set: [var 101]
		&=: [$var neg: [1]]
		print: [$var]
		set: [var 101]
		&=: [$var 100]
		print: [$var]
		""",
		"""
		0
		100
		101
		100
		"""
	)


def test_bitwise_or():
	""""""
	
	run_test_program(
		"""
		print: [|: [2 1]]
		print: [|: [100 101]]
		print: [|: [101 neg: [1]]]
		print: [|: [101 100]]
		""",
		"""
		3
		101
		-1
		101
		"""
	)


def test_bitwise_or_eq():
	""""""
	
	run_test_program(
		"""
		set: [var 2]
		|=: [$var 1]
		print: [$var]
		set: [var 100]
		|=: [$var 101]
		print: [$var]
		set: [var 101]
		|=: [$var neg: [1]]
		print: [$var]
		set: [var 101]
		|=: [$var 100]
		print: [$var]
		""",
		"""
		3
		101
		-1
		101
		"""
	)


def test_bitwise_xor():
	""""""
	
	run_test_program(
		"""
		print: [^: [2 1]]
		print: [^: [100 101]]
		print: [^: [101 neg: [1]]]
		print: [^: [101 100]]
		""",
		"""
		3
		1
		-102
		1
		"""
	)


def test_bitwise_xor_eq():
	""""""
	
	run_test_program(
		"""
		set: [var 2]
		^=: [$var 1]
		print: [$var]
		set: [var 100]
		^=: [$var 101]
		print: [$var]
		set: [var 101]
		^=: [$var neg: [1]]
		print: [$var]
		set: [var 101]
		^=: [$var 100]
		print: [$var]
		""",
		"""
		3
		1
		-102
		1
		"""
	)


def test_bitwise_complement():
	""""""
	
	run_test_program(
		"""
		print: [~: [1]]
		print: [~: [14]]
		print: [~: [neg: [14]]]
		""",
		"""
		-2
		-15
		13
		"""
	)


def test_bitwise_left_shift():
	""""""
	
	run_test_program(
		"""
		print: [<<: [2 1]]
		print: [<<: [100 101]]
		print: [<<: [101 100]]
		""",
		"""
		4
		253530120045645880299340641075200
		128032710623051169551167023742976
		"""
	)


def test_bitwise_left_shift_eq():
	""""""
	
	run_test_program(
		"""
		set: [var 2]
		<<=: [$var 1]
		print: [$var]
		set: [var 100]
		<<=: [$var 101]
		print: [$var]
		set: [var 101]
		<<=: [$var 100]
		print: [$var]
		""",
		"""
		4
		253530120045645880299340641075200
		128032710623051169551167023742976
		"""
	)



def test_bitwise_right_shift():
	""""""
	
	run_test_program(
		"""
		print: [>>: [2 1]]
		print: [>>: [100 101]]
		print: [>>: [101 100]]
		""",
		"""
		1
		0
		0
		"""
	)


def test_bitwise_right_shift_eq():
	""""""
	
	run_test_program(
		"""
		set: [var 2]
		>>=: [$var 1]
		print: [$var]

		set: [var 100]
		>>=: [$var 101]
		print: [$var]
		
		set: [var 101]
		>>=: [$var 100]
		print: [$var]
		""",
		"""
		1
		0
		0
		"""
	)




if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
