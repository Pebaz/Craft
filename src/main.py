import yaml, pprint


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

def wing_set(name, value, parent):
	# Handle expressions
	parent[name] = value

def getkey(symbol):
	return [i for i in symbol.keys()][0]

def getvalue(symbol):
	return symbol[getkey(symbol)]

def query_symbol_table(name, ast, scope):
	pass



def handle_function(line, ast, keys):
	print(ast)
	#print(line)
	operation = getkey(line)

	if operation == 'set':

		value = getvalue(line)

		# Expressions are dictionaries
		if isinstance(value, dict):
			result = handle_op(getvalue(line))
			print(result)

		# Should
		elif isinstance(value, list):
			if len(value) == 2:
				name = value[0]

				# For right now, we are assuming that there is no expression
				# (dict) here:
				set_to_value = value[1]

				ast = [{ name : set_to_value }] + ast # <-------------- doesn't change it because ast is local copy




with open('test/test.yaml') as file:
	ast = yaml.load(file)

	ast['imported_modules'] = list()
	ast['built-ins'] = dict()

	#pprint.pprint(ast)

	for line in ast['Program']:

		if not isinstance(line, dict):
			raise Exception('Line is not dictionary: %s' % repr(line))

		handle_function(line, ast['Program'], [])

		

