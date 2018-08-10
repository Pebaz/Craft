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
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v += i
	
	wing_set()


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


def wing_bitwise_right_shift(*args):
	"""
	Bitwise right shift operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v >>= i
	return v


__wing__ = {
	'+' 	: wing_add,
	'+=' 	: wing_add_equal,
	'-' 	: wing_sub,
	'*' 	: wing_mul,
	'/' 	: wing_div,
	'%' 	: wing_mod,
	'**' 	: wing_exp,
	'=' 	: wing_equals,
	'<>' 	: wing_not_equals,
	'!=' 	: wing_not_equals,
	'>' 	: wing_greater_than,
	'<' 	: wing_less_than,
	'>=' 	: wing_greater_than_or_equal_to,
	'<=' 	: wing_less_than_or_equal_to,
	'&' 	: wing_bitwise_and,
	'|' 	: wing_bitwise_or,
	'^' 	: wing_bitwise_xor,
	'~' 	: wing_bitwise_complement,
	'<<' 	: wing_bitwise_left_shift,
	'>>' 	: wing_bitwise_right_shift,
}