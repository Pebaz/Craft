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


def wing_create_named_scope(*args):
	"""
	"""
	args = get_args(args)
	global SCOPE, SYMBOL_TABLE
	SYMBOL_TABLE[SCOPE][args[0]] = dict()


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


def wing_byval(*args):
	"""
	Since functions only try one round of evaluation for arguments, arguments
	can be passed "by value" instead of "by reference/name".
	"""
	return args[0]