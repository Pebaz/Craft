import pprint, traceback
from pathlib import Path
import yaml
import pyparsing as pyp
from wing_core import *
from wing_parser import *

pp = pprint.PrettyPrinter(width=1)

# -----------------------------------------------------------------------------
#            S T A N D A R D   L I B R A R Y   F U N C T I O N S
# -----------------------------------------------------------------------------


def wing_break(*args):
	raise WingLoopBreakException()

def wing_while(*args):
	"""
	"""
	condition = args[0]

	push_return_point()

	wing_push_scope()

	try:
		while get_arg_value(condition):
			get_args(args[1:])

	except WingLoopBreakException:
		pass

	cull_scopes(pop_return_point())


def wing_until(*args):
	"""
	"""
	condition = args[0]

	push_return_point()

	wing_push_scope()

	try:
		while not get_arg_value(condition):
			get_args(args[1:])

	except WingLoopBreakException:
		pass

	cull_scopes(pop_return_point())


def __wing_import__query_dir(filename):
	"""
	Returns the YAML/WING/PY file after searching the path.
	"""
	global WING_PATH

	for path in WING_PATH:
		p = Path(path)
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

	push_return_point()
	wing_push_scope()

	try:
		for i in range(start, stop, step):
			wing_set(var, i)
			get_args(args[1:])
	except WingLoopBreakException:
		pass

	except Exception as e:
		traceback.print_exc()

	cull_scopes(pop_return_point())


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


def wing_unless(*args):
	"""
	"""
	if len(args) > 3 or len(args) < 2:
		raise Exception(f'Malformed if statement at:\n{args}')
	
	# Testing condition
	c = args[0]

	# Run the THEN function if the condition is equal to True
	if not handle_expression(c) if isinstance(c, dict) else not handle_value(c):
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


__wing__ = {
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
	'unless' : wing_unless,
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
	'break' : wing_break,
	'while' : wing_while,
	'until' : wing_until,
}
