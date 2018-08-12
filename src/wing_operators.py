# -----------------------------------------------------------------------------
#           S T A N D A R D   L I B R A R Y   O P E R A T O R S
# -----------------------------------------------------------------------------

from wing_core import *

def wing_add(*args):
	"""
	Addition operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v += i
	return v


def wing_add_equal(*args):
	"""
	Usage:

	set: [a, 5]
	'+=' : [$$a, 2]
	print: [$a] # prints 7

	Error condtion:
	'+=' : [15, 2]
	# Error name 15 not found
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v += i
	
	wing_set(var_name, v)


def wing_sub(*args):
	"""
	Subtraction operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v -= i
	return v


def wing_mul(*args):
	"""
	Multiplication operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v *= i
	return v


def wing_div(*args):
	"""
	Division operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v /= i
	return v

def wing_mod(*args):
	"""
	Modulus operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v %= i
	return v


def wing_exp(*args):
	"""
	Exponent operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v **= i
	return v


def wing_equals(*args):
	"""
	Equality operator.
	"""
	args = get_args(args)
	return len(set(args)) <= 1


def wing_not_equals(*args):
	"""
	Inequality operator.
	"""
	args = get_args(args)
	return not len(set(args)) <= 1


def wing_greater_than(*args):
	"""
	Greater than operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v > i for i in args[1:]
	])


def wing_less_than(*args):
	"""
	Less than operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v < i for i in args[1:]
	])


def wing_greater_than_or_equal_to(*args):
	"""
	Greater than or equal to operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v >= i for i in args[1:]
	])


def wing_less_than_or_equal_to(*args):
	"""
	Less than or equal to operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v <= i for i in args[1:]
	])


def wing_bitwise_and(*args):
	"""
	Bitwise AND operator.	
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v &= i
	return v


def wing_bitwise_or(*args):
	"""
	Bitwise OR operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v |= i
	return v


def wing_bitwise_xor(*args):
	"""
	Bitwise XOR operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v ^= i
	return v


def wing_bitwise_complement(*args):
	"""
	Bitwise complement operator.

	Inverts all bits.
	"""
	if len(args) > 1:
		raise Exception(f'Too many arguments in bitwise complement: {args}')

	return ~get_arg_value(args[0])


def wing_bitwise_left_shift(*args):
	"""
	Bitwise left shift operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v <<= i
	return v


def wing_bitwise_right_shift(*args):
	"""
	Bitwise right shift operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v >>= i
	return v
