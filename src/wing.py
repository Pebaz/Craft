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


import sys, pprint, traceback
from docopt import docopt

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


def is_identifier(string):
	"""
	"""
	Identifier = pyp.Word(
		pyp.alphas + '_', bodyChars=pyp.alphanums + '_-.'
	)
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



class Wing:

	def __init__(self):
		self.DEBUG = False
		self.SCOPE = 0
		self.RETURN_POINTS = []
		self.SYMBOL_TABLE = []
		self.is_yaml = True
		self.pp = PrettyPrinter(width=1)

	def main(self, args):
		"""
		"""
		usage = __doc__.format(args[0])
		arguments = docopt(usage, argv=args[1:], version='Wing 0.1.0')

		self.build_symbol_table()

		if arguments['FILENAME'] != None:
			self.DEBUG = arguments['--debug']
			interpreter = WingInterpreter(self)
			interpreter.run_file(arguments['FILENAME'])	
		else:
			repl = WingREPL(self, arguments['--yaml'])
			repl.run_cli()

	def build_symbol_table(self):
		"""
		"""
		self.SYMBOL_TABLE[0] = dict()

		import keywords
		import operators	

		for keyword in dir(keywords):
			if keywords.startswith('wing_'):
				func_name = keyword[5:]
				function = keywords[keywords]
				self.SYMBOL_TABLE[0][func_name] = function

		for operator in dir(operators):
			function = operators[operator]
			if callable(function):
				self.SYMBOL_TABLE[0][operator] = function



if __name__ == '__main__':
	wing = Wing()
	sys.exit(wing.main(sys.argv))

	'''
	import cProfile
	def profile():
		main(sys.argv)
	cProfile.run('profile()', sort='ncalls')
	'''