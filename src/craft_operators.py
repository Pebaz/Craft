# -----------------------------------------------------------------------------
#           S T A N D A R D   L I B R A R Y   O P E R A T O R S
# -----------------------------------------------------------------------------

from craft_core import *


@expose('+')
def craft_add(*args):
	"""
	Addition operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v += i
	return v


@expose('+=')
def craft_add_equal(*args):
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

	craft_set(var_name, v)


@expose('-')
def craft_sub(*args):
	"""
	Subtraction operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v -= i
	return v


@expose('-=')
def craft_sub_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v -= i

	craft_set(var_name, v)


@expose('*')
def craft_mul(*args):
	"""
	Multiplication operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v *= i
	return v


@expose('*=')
def craft_mul_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v *= i

	craft_set(var_name, v)


@expose('/')
def craft_div(*args):
	"""
	Division operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v /= i
	return v


@expose('/=')
def craft_div_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v /= i

	craft_set(var_name, v)


@expose('%')
def craft_mod(*args):
	"""
	Modulus operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v %= i
	return v


@expose('%=')
def craft_mod_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v %= i

	craft_set(var_name, v)


@expose('**')
def craft_exp(*args):
	"""
	Exponent operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v **= i
	return v


@expose('**=')
def craft_exp_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v **= i

	craft_set(var_name, v)


@expose('=')
def craft_equals(*args):
	"""
	Equality operator.
	"""
	args = get_args(args)
	return len(set(args)) <= 1


@expose('!=')
def craft_not_equals(*args):
	"""
	Inequality operator.
	"""
	args = get_args(args)
	return not len(set(args)) <= 1


@expose('>')
def craft_greater_than(*args):
	"""
	Greater than operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v > i for i in args[1:]
	])


@expose('<')
def craft_less_than(*args):
	"""
	Less than operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v < i for i in args[1:]
	])


@expose('>=')
def craft_greater_than_or_equal_to(*args):
	"""
	Greater than or equal to operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v >= i for i in args[1:]
	])


@expose('<=')
def craft_less_than_or_equal_to(*args):
	"""
	Less than or equal to operator.
	"""
	args = get_args(args)
	v = args[0]
	return all([
		v <= i for i in args[1:]
	])


@expose('&')
def craft_bitwise_and(*args):
	"""
	Bitwise AND operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v &= i
	return v


@expose('&=')
def craft_bitwise_and_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v &= i

	craft_set(var_name, v)


@expose('|')
def craft_bitwise_or(*args):
	"""
	Bitwise OR operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v |= i
	return v


@expose('|=')
def craft_bitwise_or_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v |= i

	craft_set(var_name, v)


@expose('^')
def craft_bitwise_xor(*args):
	"""
	Bitwise XOR operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v ^= i
	return v


@expose('^=')
def craft_bitwise_xor_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v ^= i

	craft_set(var_name, v)


@expose('~')
def craft_bitwise_complement(*args):
	"""
	Bitwise complement operator.

	Inverts all bits.
	"""
	if len(args) > 1:
		raise Exception(f'Too many arguments in bitwise complement: {args}')

	return ~get_arg_value(args[0])


@expose('<<')
def craft_bitwise_left_shift(*args):
	"""
	Bitwise left shift operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v <<= i
	return v


@expose('<<=')
def craft_bitwise_left_shift_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v <<= i

	craft_set(var_name, v)


@expose('>>')
def craft_bitwise_right_shift(*args):
	"""
	Bitwise right shift operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v >>= i
	return v


@expose('>>=')
def craft_bitwise_right_shift_equal(*args):
	"""
	"""
	var_name = args[0].replace('$', '')
	args = get_args(args)
	v = get_arg_value(args[0])
	for i in args[1:]:
		v -= i

	craft_set(var_name, v)


@expose('neg')
def craft_negative(*args):
	"""
	Looks like I can't parse negative numbers :(
	"""
	args = get_args(args)
	if len(args) > 1:
		raise Exception('Too many arguments for inversion of signage.')

	return -args[0]
