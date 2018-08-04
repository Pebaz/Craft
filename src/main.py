import yaml, pprint

pp = pprint.PrettyPrinter(width=1)

def wing_recursive_get(dictn, keys):
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

def wing_if():
	pass

def wing_hash():
	"""
	- set: [asdf, [[key, value], [key, value], [key, value]]]
	"""























def wing_add(*args):
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v += i
	return v

def wing_sub(*args):
	args = get_args(args)
	v = args[0]
	for i in args[1:]:
		v -= i
	return v


def wing_set(name, value):
	global SYMBOL_TABLE, SCOPE

	if not name.isidentifier():
		raise Exception(f'"{name}" not a valid identifier.')

	SYMBOL_TABLE[SCOPE][name] = get_arg_value(value)


def wing_print(*args):
	print(*get_args(args))


def wing_program(*args):
	#print('Wing Programming Language\nVersion: 0.1.1\n')
	return get_args(args)


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


def push_scope():
	global SCOPE, SYMBOL_TABLE
	SCOPE += 1
	SYMBOL_TABLE.append(dict())


def pop_scope():
	global SCOPE, SYMBOL_TABLE
	SYMBOL_TABLE[SCOPE]
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
		'print' : wing_print,
		'set' : wing_set
	}
]
SCOPE = 0 # For now, functions have to increment and decrement scope


def query_symbol_table(name, scope):
	"""
	Looks at each scope starting at the scope index given and works its way up
	to zero.
	"""

	global SYMBOL_TABLE

	if name not in SYMBOL_TABLE[scope]:
		if scope > 0:
			return query_symbol_table(name, scope - 1)
		else:
			pp.pprint(SYMBOL_TABLE)
			raise Exception(f'"{name}" not found.')

	else:
		try:
			#return getvalue(SYMBOL_TABLE[scope])
			return SYMBOL_TABLE[scope][name]
		except KeyError as e:
			raise Exception(f'"{name}" not found.') from e


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
	#print('\n')
	#print(f'Handling Expression: {getkey(dictn)}')
	#pp.pprint(dictn)

	'''
	args = [
		handle_expression(i)
		if isinstance(i, dict)
		else handle_value(i)
		for i in getvalue(dictn)
	]
	'''

	func = query_symbol_table(getkey(dictn), SCOPE)

	#return func(*args)
	return func(*getvalue(dictn))


with open('test/test.yaml') as file:
	ast = yaml.load(file)

	ast['imported_modules'] = list()
	ast['built-ins'] = dict()
	ast['variables'] = dict()

	# Handle the top-level function named "Program" recursively
	handle_expression({ 'Program' : ast['Program'] })

		

