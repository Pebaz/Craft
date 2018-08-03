import yaml, pprint

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



def handle_function(line):
	operation = getkey(line)

	if operation == 'set':
		#wing_set(getvalue(line))
		if isinstance(getvalue(line), dict):
			result = handle_op(getvalue(line))
			print(result)


with open('test/test.yaml') as file:
	ast = yaml.load(file)

	ast['imported_modules'] = list()
	ast['built-ins'] = dict()

	#pprint.pprint(ast)

	for line in ast['Program']:

		if not isinstance(line, dict):
			raise Exception('Line is not dictionary: %s' % repr(line))

		handle_function(line)

		

