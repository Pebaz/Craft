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


import sys, os.path, pprint, traceback
import yaml
import pyparsing as pyp
from docopt import docopt
from wing_parser import WingParser
import wing_operators
import wing_keywords

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

Identifier = pyp.Word(
	pyp.alphas + '_', bodyChars=pyp.alphanums + '_-.'
)

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
	Should this recursively eval expressions? What will that do to dictionaries?
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
	return [get_arg_value(i) for i in args]

	'''
	return [
		handle_expression(i)
		if isinstance(i, dict)
		else handle_value(i)
		for i in args
	]
	'''


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
	global pp, SCOPE, DEBUG
	func = query_symbol_table(getkey(dictn), SCOPE)

	if DEBUG:
		print(f'Expression: {"    " * SCOPE + getkey(dictn)}')

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

SYMBOL_TABLE = [dict()]
SYMBOL_TABLE[0].update(wing_operators.__wing__)
SYMBOL_TABLE[0].update(wing_keywords.__wing__)
SCOPE = 0
RETURN_POINTS = []


# -----------------------------------------------------------------------------
#                       W I N G   I N T E R P R E T E R
# -----------------------------------------------------------------------------

# Print debugging for now
DEBUG = False



def run_file(filename):
	"""
	"""
	parser = WingParser()

	# Handle the top-level function named "Program" recursively
	with open(filename) as file:
		extension = os.path.splitext(filename)[1]

		ast = None

		if extension.lower() == '.yaml':
			ast = yaml.load(file)

		elif extension.lower() == '.wing':
			ast = parser.parse(file.read())

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

	parser = WingParser()

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
					ast = yaml.load(code) if yaml_lang else parser.parse(code)
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