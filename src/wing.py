"""Wing Programming Language

Usage:
  {0}
  {0} [-d | --debug] FILENAME
  {0} (-v | --version)

Options:
  FILE            Run a Wing Program From Source
  -v --version    Display Wing Version and Exit
  -d --debug      Debug a Wing Program

To run the Wing REPL, supply no arguments:
  {0}
"""


import sys, pprint, yaml, pyparsing
import traceback
from docopt import docopt

# When importing, only load ast['Program']
# When running, first run ast['Program'], then run ast['Main']



# -----------------------------------------------------------------------------
#                        G L O B A L   V A R I A B L E S
# -----------------------------------------------------------------------------

pp = pprint.PrettyPrinter(width=1)

Identifier = pyparsing.Word(
	pyparsing.alphas + '_', bodyChars=pyparsing.alphanums + '_-.'
)


# -----------------------------------------------------------------------------
#                W I N G   E X C E P T I O N   C L A S S E S
# -----------------------------------------------------------------------------

class WingFunctionReturnException(Exception):
	"""
	For returning values from functions. The `wing_call` function will catch
	these exceptions and return the value contained in this class as the return
	value.
	"""
	def __init__(self, value):
		Exception.__init__(self)
		self.return_value = value


# -----------------------------------------------------------------------------
#            S T A N D A R D   L I B R A R Y   F U N C T I O N S
# -----------------------------------------------------------------------------

def wing_while(condition, statements):
	"""
	"""


def wing_hash():
	"""
	- set: [asdf, [[key, value], [key, value], [key, value]]]
	"""


def wing_foreach(*args):
	"""
	"""


def wing_and(*args):
	"""
	Logical AND operator.
	"""
	if len(args) > 2:
		raise Exception(f'Too many operands in logical AND: {args}')

	args = get_args(args)
	return args[0] and args[1]


def wing_or(*args):
	"""
	Logical OR operator.
	"""
	if len(args) > 2:
		raise Exception(f'Too many operands in logical OR: {args}')

	args = get_args(args)
	return args[0] or args[1]


def wing_not(*args):
	"""
	Logical NOT operator.
	"""
	if len(args) > 1:
		raise Exception(f'Too many operands in logical NOT: {args}')

	return not get_arg_value(args[0])


def wing_for(*args):
	"""
	"""
	control = args[0]

	var, start, stop, step = [None] * 4

	if len(control) == 4:
		var, start, stop, step = get_arg_value(control)

	elif len(control) == 3:
		var, start, stop, step = *get_arg_value(control), 1

	elif len(control) == 2:
		var, stop, start, step = *get_arg_value(control), 0, 1

	else:
		raise Exception(f'Malformed control value: (var, start, stop, step)')

	wing_push_scope()

	for i in range(start, stop, step):
		wing_set(var, i)

		get_args(args[1:])

	wing_pop_scope()


def wing_if(*args):
	"""
	"""
	if len(args) > 3 or len(args) < 2:
		raise Exception(f'Malformed if statement at:\n{args}')
	
	# Testing condition
	c = get_arg_value(args[0])[0]

	# Run the THEN function if the condition is equal to True
	if handle_expression(c) if isinstance(c, dict) else handle_value(c):
		wing_push_scope()
		handle_expression(args[1])
		wing_pop_scope()

	# Handle ELSE clause if it was added
	elif len(args) == 3:
		wing_push_scope()
		handle_expression(args[2])
		wing_pop_scope()


def wing_then(*args):
	"""
	"""
	args = get_args(args)


def wing_else(*args):
	"""
	"""
	args = get_args(args)


def wing_globals(*args):
	"""
	"""
	pp.pprint(SYMBOL_TABLE)


def wing_exit(*args):
	"""
	"""
	exit()


def wing_comment(*args):
	"""
	"""


def wing_set(name, value):
	"""
	"""
	global SYMBOL_TABLE, SCOPE

	if not is_identifier(name):
		raise Exception(f'"{name}" not a valid identifier.')

	value = get_arg_value(value)
	keys = name.split('.')
	var_name = keys[-1]

	if len(keys) > 1:
		dict_recursive_get(SYMBOL_TABLE[SCOPE], keys[:-1])[var_name] = value
	else:
		SYMBOL_TABLE[SCOPE][var_name] = value


def wing_print(*args):
	"""
	"""
	print(*get_args(args))


def wing_def(*args):
	"""
	Bind function name to variable in current scope. This will allow it to be
	called.
	"""
	declaration = get_arg_value(args[0])
	func_name = declaration[0]
	func_args = declaration[1:]
	func_definition = args[1:]
	wing_set(func_name, [func_args, func_definition])


def wing_return(*args):
	"""
	The `wing_call` function will catch this exception and then return the
	value from it.
	"""
	if len(args) > 1:
		ex = f'Only 1 value can be returned from function, got {len(args)}.'
		raise Exception(ex)

	value = get_arg_value(args[0])
	raise WingFunctionReturnException(value)


def wing_call(*args):
	"""
	6. Return value.
	"""
	global SCOPE

	args = get_args(args)
	func_name = args[0]
	func_args = args[1:]
	arg_names, func_definition = query_symbol_table(func_name, SCOPE)

	if len(arg_names) != len(func_args):
		err = f'Argument count mismatch for function: '
		err += f'{func_name}. Expected {len(arg_names)}, got {len(func_args)}.'
		raise Exception()

	# Scope index to return to after call is done
	push_return_point()

	# Push a new scope to bind all local variables to
	wing_push_scope()

	# Bind each variable to the new function scope
	for i in range(len(arg_names)):
		wing_set(arg_names[i], func_args[i])

	# Return value
	return_value = None

	# Handle each statement in the function
	for statement in func_definition:

		# Run the statement
		try:
			get_arg_value(statement)

		# Get return value and stop handling expressions
		except WingFunctionReturnException as wfre:
			return_value = wfre.return_value
			break

		# A real error has occurred :(
		except Exception as e:
			traceback.print_exc()
			break

	# Return the scope to where it was before the call,
	# deleting any scopes in between
	return_point = pop_return_point()
	for i in range(SCOPE - return_point):
		wing_pop_scope()

	# Return the value returned from the function (if any)
	return return_value


def wing_lambda(*args):
	"""
	TODO(Pebaz): Fix `wing_call` to be able to handle lambdas.
	"""

def wing_struct(*args):
	"""
	"""
	args = get_args(args)
	struct_name = args[0]
	struct_members = args[1:]
	wing_set(struct_name, struct_members)


def wing_new(*args):
	"""
	Must be able to be extended to build classes/types later.

	Structs: hold only vars
	Types: hold vars and functions
	Classes: hold vars, functions, and support oop
	"""
	args = get_args(args)
	definition, member_values = args[0], args[1:]

	# If the values provided do not match the definition given,
	# initialize the blank members to zero.
	if len(definition) > len(member_values):
		member_values.extend([
			None for i in range(len(definition) - len(member_values))
		])

	# Create a dictionary out of the names and values of the members
	struct = dict(zip(definition, member_values))
	return struct


def wing_program(*args):
	"""
	"""
	get_args(args)


def wing_create_named_scope(name):
	"""
	"""
	global SCOPE, SYMBOL_TABLE
	SYMBOL_TABLE[SCOPE][name] = dict()


def wing_push_named_scope(name):
	"""
	Used in classes:
	push "this"

	this.name
	this.age

	Note that this is pushed DURING execution of a class constructor or method.
	"""


def wing_pop_named_scope(name):
	"""
	Used to remove a named scope temporarily?
	"""


def wing_push_scope():
	"""
	"""
	global SCOPE, SYMBOL_TABLE
	SCOPE += 1
	SYMBOL_TABLE.append(dict())


def wing_pop_scope():
	"""
	"""
	global SCOPE, SYMBOL_TABLE
	SCOPE -= 1
	SYMBOL_TABLE.pop()


# -----------------------------------------------------------------------------
#           S T A N D A R D   L I B R A R Y   O P E R A T O R S
# -----------------------------------------------------------------------------

def wing_add(*args):
	"""
	Addition operator.
	"""
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v += i
	return v


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


# -----------------------------------------------------------------------------
#                          W I N G   I N T E R N A L S
# -----------------------------------------------------------------------------

def is_identifier(string):
	"""
	"""
	try:
		Identifier.parseString(string)
		return True
	except:
		return False

def dict_recursive_peek(dictn, keys):
	"""
	"""
	try:
		if len(keys) == 1:
			dictn[keys[0]]
		else:
			get(dictn[keys[0]], keys[1:])
		return True
	except:
		return False

def dict_recursive_get(dictn, keys):
	"""
	Recursively indexes a dictionary to retrieve a value.

	Equivalent to:
	dictn[keys[0]][keys[1]][keys[2]][keys[n]]

	Args:
		dictn(dict): the dictionary to index.
		keys(list): the list of keys to index with.

	Returns:
		The value of the very last nested dict in the base dict.
	"""
	if len(keys) == 1:
		return dictn[keys[0]]
	else:
		return get(dictn[keys[0]], keys[1:])

def get_arg_value(arg):
	"""
	"""
	if isinstance(arg, dict):
		return handle_expression(arg)
	else:
		return handle_value(arg)


def get_args(args):
	"""
	Args:
		args: a list of expressions or values.
	"""
	return [
		handle_expression(i)
		if isinstance(i, dict)
		else handle_value(i)
		for i in args
	]


def getkey(symbol):
	"""
	"""
	return [i for i in symbol.keys()][0]


def getvalue(symbol):
	"""
	"""
	return symbol[getkey(symbol)]


def query_symbol_table(name, scope):
	"""
	Looks at each scope starting at the scope index given and works its way up
	to zero.
	"""
	global SYMBOL_TABLE

	keys = name.split('.')
	var_name = keys[-1]

	try:
		if len(keys) > 1:
			return dict_recursive_get(SYMBOL_TABLE[scope], keys[:-1])[var_name]
		else:
			return SYMBOL_TABLE[scope][var_name]
	except Exception as e:
		if scope > 0:
			return query_symbol_table(name, scope - 1)
		else:
			raise Exception(f'"{var_name}" not found.') from e


def handle_value(value):
	"""
	Can be a raw value or a name.

	Checks to see if the value is a straight value or a name. If a name is
	suspected, check to see if a leading tick: '$' is used, denoting that a
	string value is being passed, not a variable.
	"""

	# Is it a variable:
	if isinstance(value, str):

		# Force string value
		if value.startswith('$'):
			if value[1] != '$':
				return query_symbol_table(value[1:], SCOPE)
			else:
				return value[1:]
		else:
			return value
	else:
		return value


def handle_expression(dictn):
	"""
	"""
	global pp, SCOPE
	func = query_symbol_table(getkey(dictn), SCOPE)

	#print(f'Expression: {"    " * SCOPE + getkey(dictn)}')

	# Function is Python built-in function or operator
	# This is for argument passing
	if callable(func):
		return func(*getvalue(dictn))

	# Function is defined in Wing
	# Pass it's name to the call function
	else:
		return wing_call(getkey(dictn), *getvalue(dictn))


def push_return_point():
	"""
	Adds the scope at the current execution point in the event of a function
	return or (in the future) an exception occurs.
	"""
	global RETURN_POINTS
	RETURN_POINTS.append(SCOPE)


def pop_return_point():
	"""
	Return the scope that Wing should return to after a function call or
	an exception occurs.
	"""
	global RETURN_POINTS
	return RETURN_POINTS.pop()


# -----------------------------------------------------------------------------
#             W I N G   I N I T I A L   S Y M B O L   T A B L E
# -----------------------------------------------------------------------------

# Represents a list of lists of key-value pairs (variables/names)
SYMBOL_TABLE = [
	# Scope level 0 (anyone can view and use)
	{
		# Operators
		'+' : wing_add,
		'-' : wing_sub,
		'*' : wing_mul,
		'/' : wing_div,
		'%' : wing_mod,
		'**' : wing_exp,
		'=' : wing_equals,
		'<>' : wing_not_equals,
		'!=' : wing_not_equals,
		'>' : wing_greater_than,
		'<' : wing_less_than,
		'>=' : wing_greater_than_or_equal_to,
		'<=' : wing_less_than_or_equal_to,
		'&' : wing_bitwise_and,
		'|' : wing_bitwise_or,
		'^' : wing_bitwise_xor,
		'~' : wing_bitwise_complement,
		'<<' : wing_bitwise_left_shift,
		'>>' : wing_bitwise_right_shift,

		# Built-Ins
		'Program' : wing_program, # Everyone has access to names in level 0
		'push-scope' : wing_push_scope,
		'pop-scope' : wing_pop_scope,
		'create-named-scope': wing_create_named_scope,
		'globals' : wing_globals,
		'quit' : wing_exit,
		'exit' : wing_exit,
		'def' : wing_def,
		'return' : wing_return,
		'call' : wing_call,
		'fn' : wing_lambda,
		'struct' : wing_struct,
		'new' : wing_new,
		'set' : wing_set,
		'for' : wing_for,
		'if' : wing_if,
		'then' : wing_then,
		'else' : wing_else,
		'print' : wing_print,
		'comment' : wing_comment,
		'and' : wing_and,
		'or' : wing_or,
		'not' : wing_not,
	}
]
SCOPE = 0 # For now, functions have to increment and decrement scope
RETURN_POINTS = []


# -----------------------------------------------------------------------------
#                       W I N G   I N T E R P R E T E R
# -----------------------------------------------------------------------------

def run_file(filename):
	"""
	"""
	# Handle the top-level function named "Program" recursively
	with open(filename) as file:
		ast = yaml.load(file)
		handle_expression({ 'Program' : ast['Program'] })

		# Handle "if __name__ == '__main__"
		if 'Main' in ast:
			handle_expression({ 'Program' : ast['Main'] })


def __cli_sanitize_code(code):
	"""
	"""
	new_code = 'Program:\n'

	for the_line in code.split('\n'):
		if the_line.strip() == '':
			continue

		if '  ' not in the_line:
			new_code += '  - ' + the_line + '\n'
		else:
			new_code += '  ' + the_line + '\n'

	return new_code


def run_cli():
	"""
	"""
	print('Wing Programming Language')
	print('Version: 0.1.0\n')
	print('Press <enter> twice for running single commands.')
	print('Type "quit: []" or press CTCL > C to leave the program.\n')

	try:
		code = ''
		while True:
			line = input('>>> ') if code == '' else input('... ')

			if line.strip() != '':
				code += line + '\n'

			else:
				if code.strip() == '':
					continue

				code = __cli_sanitize_code(code)

				# Run the code
				try:
					output = handle_expression(yaml.load(code))
					
					if output != None:
						print(f' -> {output}')

				except Exception as e:
					print('WING ERROR:')
					traceback.print_exc()
					code = ''
					continue

				if code.strip().replace('\n', '') == 'quit':
					break

				code = ''

	except KeyboardInterrupt:
		pass


def main(args):
	"""
	"""

	# Make the docstring .EXE friendly
	usage = __doc__.format(args[0])
	arguments = docopt(usage, argv=args[1:], version='Wing 0.1.0')

	#print(arguments)

	if arguments['FILENAME'] != None:
		if not arguments['--debug']:
			run_file(arguments['FILENAME'])	
		else:
			print('Wing debugger not yet implemented.')
	else:
		run_cli()


if __name__ == '__main__':
	sys.exit(main(sys.argv))

	'''
	import cProfile
	def profile():
		main(sys.argv)
	cProfile.run('profile()', sort='ncalls')
	'''