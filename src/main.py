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

pp = pprint.PrettyPrinter(width=1)
Identifier = pyparsing.Word(pyparsing.alphas + '_', bodyChars=pyparsing.alphanums + '_-.')

def is_identifier(string):
	try:
		Identifier.parseString(string)
		return True
	except:
		return False



def dict_recursive_peek(dictn, keys):
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

# When importing, only load ast['Program']
# When running, first run ast['Program'], then run ast['Main']

def wing_while(condition, statements):
	pass


def wing_hash():
	"""
	- set: [asdf, [[key, value], [key, value], [key, value]]]
	"""




def wing_foreach(*args):
	pass


def wing_for(*args):
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
	if len(args) > 3 or len(args) < 2:
		raise Exception(f'Malformed if statement at:\n{args}')
	
	condition = args[0]
	if (handle_expression(condition) if isinstance(condition, dict) else handle_value(condition)):
		wing_push_scope()
		handle_expression(args[1])
		wing_pop_scope()

	elif len(args) == 3:
		wing_push_scope()
		handle_expression(args[2])
		wing_pop_scope()


def wing_then(*args):
	args = get_args(args)


def wing_else(*args):
	args = get_args(args)


def wing_globals(*args):
	pp.pprint(SYMBOL_TABLE)


def wing_exit(*args):
	exit()

def wing_comment(*args):
	pass


def wing_add(*args):
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v += i
	return v

def wing_mod(*args):
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v %= i
	return v

def wing_sub(*args):
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v -= i
	return v

def wing_greater_than(*args):
	args = get_args(args)
	if len(args) > 2:
		raise Exception(f'Too many values ({len(args)}) to compare for greater than operator.')
	return args[0] > args[1]


def wing_less_than(*args):
	args = get_args(args)
	if len(args) > 2:
		raise Exception(f'Too many values ({len(args)}) to compare for greater than operator.')
	return args[0] < args[1]


def wing_set(name, value):
	global SYMBOL_TABLE, SCOPE

	if not is_identifier(name):
		raise Exception(f'"{name}" not a valid identifier.')


	#SYMBOL_TABLE[SCOPE][name] = get_arg_value(value)

	value = get_arg_value(value)
	keys = name.split('.')
	var_name = keys[-1]

	if len(keys) > 1:
		dict_recursive_get(SYMBOL_TABLE[SCOPE], keys[:-1])[var_name] = value
	else:
		SYMBOL_TABLE[SCOPE][var_name] = value



def wing_print(*args):
	print(*get_args(args))


def wing_program(*args):
	get_args(args)


def get_arg_value(arg):
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
	return [i for i in symbol.keys()][0]


def getvalue(symbol):
	return symbol[getkey(symbol)]


def wing_create_named_scope(name):
	global SCOPE, SYMBOL_TABLE
	SYMBOL_TABLE[SCOPE][name] = dict()


def wing_push_scope():
	global SCOPE, SYMBOL_TABLE
	SCOPE += 1
	SYMBOL_TABLE.append(dict())


def wing_pop_scope():
	global SCOPE, SYMBOL_TABLE
	SCOPE -= 1
	SYMBOL_TABLE.pop()


# Represents a list of lists of key-value pairs (variables/names)
SYMBOL_TABLE = [
	# Program
	# Operators
	# Built-Ins
	{
		'Program' : wing_program, # Everyone has access to names in level 0
		'+' : wing_add,
		'-' : wing_sub,
		'>' : wing_greater_than,
		'<' : wing_less_than,
		'%' : wing_mod,
		'push-scope' : wing_push_scope,
		'pop-scope' : wing_pop_scope,
		'create-named-scope': wing_create_named_scope,
		'quit' : wing_exit,
		'globals' : wing_globals,
		'exit' : wing_exit,
		'set' : wing_set,
		'for' : wing_for,
		'if' : wing_if,
		'then' : wing_then,
		'else' : wing_else,
		'print' : wing_print,
		'comment' : wing_comment,
	}
]
SCOPE = 0 # For now, functions have to increment and decrement scope


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
	except:
		if scope > 0:
			return query_symbol_table(name, scope - 1)
		else:
			raise Exception(f'"{var_name}" not found.')


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
	global pp, SCOPE
	func = query_symbol_table(getkey(dictn), SCOPE)
	return func(*getvalue(dictn))


def run_file(filename):
	# Handle the top-level function named "Program" recursively
	with open(filename) as file:
		ast = yaml.load(file)
		handle_expression({ 'Program' : ast['Program'] })




def cli_sanitize_code(code):
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
	print('Wing Programming Language')
	print('Version: 0.1.0\n')
	print('Press <enter> twice for running single commands.')
	print('Type "quit" or press CTCL > C to leave the program.\n')

	code = ''
	while True:
		line = input('>>> ') if code == '' else input('... ')

		if line.strip() != '':
			code += line + '\n'

		else:
			if code.strip() == '':
				continue

			code = cli_sanitize_code(code)

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




def main(args):

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
