"""Wing Programming Language

Usage:
  {0}
  {0} (-v | --version)
  {0} [-y | --yaml]
  {0} [-y | --yaml] FILENAME
  {0} [-d | --debug] FILENAME

Options:
  FILE            Run a Wing Program From Source
  -v --version    Display Wing Version and Exit
  -d --debug      Debug a Wing Program
  -y --yaml       Interpret YAML as a Wing program

To run the Wing REPL, supply no arguments:
  {0}
"""


import sys, os, os.path, pprint, traceback, imp
from pathlib import Path
import yaml
import pyparsing as pyp
from docopt import docopt

from wing_core import *
from wing_parser import *
from wing_exceptions import *

# When importing, only load ast['Program']
# When running, first run ast['Program'], then run ast['Main']


'''
Part out the different sections:

1. Wing (launches either interpreter or REPL)
2. Interpreter
3. REPL
4. Wing Parser
5. Built-Ins/Operators
6. Wing Internals (Exceptions, etc)
'''


# -----------------------------------------------------------------------------
#                        G L O B A L   V A R I A B L E S
# -----------------------------------------------------------------------------

pp = pprint.PrettyPrinter(width=1)




# -----------------------------------------------------------------------------
#            S T A N D A R D   L I B R A R Y   F U N C T I O N S
# -----------------------------------------------------------------------------

def wing_while(condition, statements):
	"""
	"""


def __wing_import__query_dir(filename):
	"""
	Returns the YAML/WING/PY file after searching the path.
	"""
	global WING_PATH

	for path in WING_PATH:
		p = Path(path)

		# Importing a module not in a package

		mod_yaml = p / f'{filename}.yaml'
		mod_wing = p / f'{filename}.wing'
		mod_py = p / f'{filename}.py'
		
		if mod_yaml.exists():
			return mod_yaml

		elif mod_wing.exists():
			return mod_wing

		elif mod_py.exists():
			return mod_py

	# If none has been returned, it doesn't exist in WING_PATH
	raise Exception(f'Cannot import name: {filename}. No matching .WING, .YAML or .PY was found in WING_PATH.')
		

def wing_import(*args):
	"""
	1. YAML import
	2. Wing import
	3. Py import

	```YAML
	# Import searches start from CWD and go inward:
	import: [wing.lang.builtins]
	# It would look in <CWD>/wing/lang/builtins

	# From imports:
	import: [[wing.lang.builtins, name1]]
	# from wing.lang.builtins import name1
	```

	1. Get import name.
	2. If no dots, search CWD
	3. If not found, search WingPath (in future)
	4. If dots, search all WingPath dirs for it
	"""
	args = get_args(args)

	for impp in args:
		to_import = impp if isinstance(impp, str) else impp[0]
		module = __wing_import__query_dir(to_import.replace('.', '/'))

		with open(str(module)) as file:
			if module.suffix == '.yaml':
				ast = yaml.load(file.read())
				if ast != None:
					handle_expression({ 'Program' : ast['Program'] })

			elif module.suffix == '.wing':
				ast = wing_parse(file.read())
				handle_expression({ 'Program' : ast['Program'] })

			else:
				pymod = module.name.replace(module.suffix, '')
				pymod = imp.load_source(pymod, str(module))

				if '__wing__' not in dir(pymod):
					raise Exception('Unable to import Python module: no __wing__ variable.')

				for name in pymod.__wing__:
					wing_set(name, pymod.__wing__[name])
					
		


	# If python import, simply set(key, value) for key in __wing__
	# from pymod import __wing__ <- doesn't run code?


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
	c = args[0]

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


def wing_locals(*args):
	"""
	"""
	global SYMBOL_TABLE, SCOPE
	pp.pprint(SYMBOL_TABLE[SCOPE])


def wing_exit(*args):
	"""
	"""
	exit()


def wing_comment(*args):
	"""
	"""


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





def wing_byval(*args):
	"""
	Since functions only try one round of evaluation for arguments, arguments
	can be passed "by value" instead of "by reference/name".
	"""
	return args[0]


def wing_byref(*args):
	"""
	Wrap the dictionary in a protective layer.
	"""
	return get_args(args)


def wing_dir(value):
	global pp
	if isinstance(value, str):
		pp.pprint(get_arg_value(value))
	elif isinstance(value, dict):
		pp.pprint(dict)



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





# -----------------------------------------------------------------------------
#                       W I N G   I N T E R P R E T E R
# -----------------------------------------------------------------------------

# Print debugging for now



def run_file(filename):
	"""
	"""
	# Handle the top-level function named "Program" recursively
	with open(filename) as file:
		extension = os.path.splitext(filename)[1]

		ast = None

		if extension.lower() == '.yaml':
			ast = yaml.load(file)

		elif extension.lower() == '.wing':
			ast = wing_parse(file.read())

		if ast != None:

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


def run_cli(yaml_lang):
	"""
	"""
	print('Wing Programming Language')
	print('Version: 0.1.0\n')
	print('Press <enter> twice for running single commands.')
	print('Type "quit: []" or press CTCL > C to leave the program.\n')

	if yaml_lang:
		print('NOTE: Interpreting YAML code as Wing syntax.')

	try:
		code = ''
		while True:
			line = input('>>> ') if code == '' else input('... ')

			if line.strip() != '':
				code += line + '\n'

			else:
				if code.strip() == '':
					continue

				if yaml_lang:
					code = __cli_sanitize_code(code)

				# Run the code
				try:
					ast = yaml.load(code) if yaml_lang else wing_parse(code)
					output = handle_expression(ast)
					
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


SYMBOL_TABLE.append({
	# Operators
	'+' : wing_add,
	'+=' : wing_add_equal,
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
	'Program' : wing_program,
	'push-scope' : wing_push_scope,
	'pop-scope' : wing_pop_scope,
	'create-named-scope': wing_create_named_scope,
	'globals' : wing_globals,
	'locals' : wing_locals,
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
	'byval' : wing_byval,
	'import' : wing_import,
	'dir' : wing_dir,
})


def main(args):
	"""
	"""
	global DEBUG

	# Make the docstring .EXE friendly
	usage = __doc__.format(args[0])
	arguments = docopt(usage, argv=args[1:], version='Wing 0.1.0')

	if arguments['FILENAME'] != None:
		DEBUG = arguments['--debug']
		run_file(arguments['FILENAME'])	
	else:
		run_cli(arguments['--yaml'])


if __name__ == '__main__':
	sys.exit(main(sys.argv))

	'''
	import cProfile
	def profile():
		main(sys.argv)
	cProfile.run('profile()', sort='ncalls')
	'''