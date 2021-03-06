import sys, pprint, traceback, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import yaml, os
import pyparsing as pyp
from craft_core import *
from craft_parser import *


# Since craft_core.py doesn't define it's own __craft__ variable, we'll do it.
# NOTE(pebaz): This is defined up top because when the `@expose()` decorators
# are run, they will overwrite names defined within here.
__craft__ = {
	'set' : craft_set,
	'raise' : craft_raise,
	'call' : craft_call,
	'exec' : craft_exec,
	'create-named-scope' : craft_create_named_scope,
	'get-symbol-table' : craft_get_symbol_table,
	'get-scope' : craft_get_scope,
	'get-return-points' : craft_get_return_points,
	'get-traceback' : craft_get_traceback,
	'get-path' : craft_get_path,
	'get-is-debug' : craft_get_is_debug,
	'get-exceptions' : craft_get_exceptions,
	'push-scope' : craft_push_scope,
	'pop-scope' : craft_pop_scope,
}


pp = pprint.PrettyPrinter(width=1)

# -----------------------------------------------------------------------------
#            S T A N D A R D   L I B R A R Y   F U N C T I O N S
# -----------------------------------------------------------------------------


@branch()
@expose()
def craft_try(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	global SCOPE
	catches = [i for i in args if getkey(i) == 'catch']
	finale = [i for i in args if getkey(i) == 'finally']
	exceptors = catches + finale

	craft_push_scope()
	pushed = True
	try:
		for i in args:
			if i not in exceptors:
				get_arg_value(i)

	# If an exception occurs, Craft will have already registered it!
	except Exception as e:
		
		# Make sure to keep track of enclosing scope
		craft_pop_scope()
		pushed = False

		error_code = query_symbol_table(e.name, SCOPE)

		for catch in catches:
			if len(getvalue(catch)) == 0:
				continue
			exceptions = get_args(getvalue(catch)[0])
			except_matches = any(i in [error_code, e.name] for i in exceptions)

			# This is the `as` functionality
			the_as = getvalue(catch)[1]
			the_exception = {
				'name' : e.name, 'desc' : e.desc, 'meta' : e.meta
			}

			if len(exceptions) == 0 or except_matches:
				# Make the second statement that the catch function interprets
				# to be binding the exception to local scope since it ignores
				# the first one in the list.
				if isinstance(the_as, list):
					catch[getkey(catch)][1] = {
						'set' : [the_as[0], { 'byval' : [the_exception] }]
					}

				get_arg_value(catch)

				# Stop since the error has already been caught
				break
	finally:
		if pushed:
			craft_pop_scope()

		if len(finale) > 0:
			get_args(finale)


@branch()
@expose()
def craft_catch(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	# Must ignore first argument since `craft_try` reads it.
	craft_push_scope()
	get_args(args[1:])
	craft_pop_scope()


@branch()
@expose()
def craft_finally(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	craft_push_scope()
	get_args(args)
	craft_pop_scope()


@expose()
def craft_exception(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	register_exception(*get_args(args))


@branch()
@expose()
def craft_switch(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	match = get_arg_value(args[0])
	cases = [i for i in args[1:] if getkey(i) == 'case']
	default = [i for i in args[1:] if getkey(i) == 'default']

	# Create a blank program function call if there is no default
	if len(default) == 0:
		default = { 'Program' : [] }

	# Handle malformed switch statement
	elif len(default) > 1:
		ldefs = len(default)
		raise Exception(f'Only 1 default clause excepted, found: {ldefs}')

	# Get the only one that is there
	else:
		default = default[0]

	# Run the case block if the value matches
	for case in cases:
		# Obtain the first value in the case block and potentially match it
		statements = getvalue(case)
		if get_arg_value(statements[0]) == match:
			get_args(statements[1:])
			break

	# Matching case was not found, handle default clause
	else:
		get_arg_value(default)


@branch()
@expose()
def craft_case(*args):
	"""
	Ignores the first argument since it is a value to use with `switch`.
	"""
	get_args(args[1:])


@branch()
@expose()
def craft_default(*args):
	"""
	Run the code therein since there is no match condition.
	"""
	get_args(args)


@expose()
def craft_break(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	raise CraftLoopBreakException()


@expose()
def craft_continue(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	raise CraftLoopContinueException()


@branch()
@expose()
def craft_while(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	condition = args[0]

	push_return_point()

	craft_push_scope()

	while get_arg_value(condition):
		try:
			get_args(args[1:])
		except CraftLoopContinueException:
			pass
		except CraftLoopBreakException:
			break

	cull_scopes(pop_return_point())


@branch()
@expose()
def craft_until(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	<Argument List>

	Returns:
	<Description of Return Value>
	"""
	condition = args[0]

	push_return_point()

	craft_push_scope()

	while not get_arg_value(condition):
		try:
			get_args(args[1:])
		except CraftLoopContinueException:
			pass
		except CraftLoopBreakException:
			break

	cull_scopes(pop_return_point())


def __craft_import__query_dir(filename):
	"""
	Returns the YAML/CRAFT/PY file after searching the path.
	"""
	global CRAFT_PATH

	for path in CRAFT_PATH + [str(Path())]:
		p = Path(path)
		mod_yaml = p / f'{filename}.yaml'
		mod_craft = p / f'{filename}.craft'
		mod_py = p / f'{filename}.py'

		if mod_yaml.exists():
			return mod_yaml

		elif mod_craft.exists():
			return mod_craft

		elif mod_py.exists():
			return mod_py

	# If none has been returned, it doesn't exist in CRAFT_PATH
	raise Exception(f'Cannot import name: {filename}. No matching .CRAFT, .YAML or .PY was found in CRAFT_PATH.')


@expose()
def craft_import(*args):
	"""
	1. YAML import
	2. Craft import
	3. Py import

	```YAML
	# Import searches start from CWD and go inward:
	import: [craft.lang.builtins]
	# It would look in <CWD>/craft/lang/builtins

	# From imports:
	import: [[craft.lang.builtins, name1]]
	# from craft.lang.builtins import name1
	```

	1. Get import name.
	2. If no dots, search CWD
	3. If not found, search CraftPath (in future)
	4. If dots, search all CraftPath dirs for it
	"""
	args = get_args(args)

	for impp in args:
		to_import = impp if isinstance(impp, str) else impp[0]
		module = __craft_import__query_dir(to_import.replace('.', '/'))

		with open(str(module)) as file:
			if module.suffix == '.yaml':
				ast = yaml.load(file.read())
				if ast != None:
					handle_expression({ 'Program' : ast['Program'] })

			elif module.suffix == '.craft':
				ast = craft_parse(file.read())
				handle_expression({ 'Program' : ast['Program'] })

			else:
				# TODO(Pebaz): Update to allow for importing PYDs
				sys.path.append(str(module.parent))

				pymod = module.name.replace(module.suffix, '')
				pymod = imp.load_source(pymod, str(module))

				if '__craft__' not in dir(pymod):
					raise Exception('Unable to import Python module: no __craft__ variable.')

				if isinstance(impp, str):
					for name in pymod.__craft__:
						craft_set(name, pymod.__craft__[name])
				else:
					for name in impp[1:]:
						craft_set(name, pymod.__craft__[name])


@expose()
def craft_and(*args):
	"""
	Logical AND operator.
	"""
	if len(args) > 2:
		raise Exception(f'Too many operands in logical AND: {args}')

	args = get_args(args)
	return args[0] and args[1]


@expose()
def craft_or(*args):
	"""
	Logical OR operator.
	"""
	if len(args) > 2:
		raise Exception(f'Too many operands in logical OR: {args}')

	args = get_args(args)
	return args[0] or args[1]


@expose()
def craft_not(*args):
	"""
	Logical NOT operator.
	"""
	if len(args) > 1:
		raise Exception(f'Too many operands in logical NOT: {args}')

	return not get_arg_value(args[0])


@branch()
@expose()
def craft_foreach(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	var, iterable = get_args(args[0])

	push_return_point()
	craft_push_scope()

	for i in iterable:
		try:
			craft_set(var, i)
			get_args(args[1:])
		except CraftLoopContinueException:
			continue
		except CraftLoopBreakException:
			break
		except Exception:
			traceback.print_exc()

	cull_scopes(pop_return_point())


@branch()
@expose()
def craft_for(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	control = get_args(args[0])

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
	craft_push_scope()

	for i in range(start, stop, step):
		try:
			craft_set(var, i)
			get_args(args[1:])
		except CraftLoopContinueException:
			continue
		except CraftLoopBreakException:
			break
		except Exception as e:
			traceback.print_exc()

	pnt = pop_return_point()
	cull_scopes(pnt)


@branch()
@expose()
def craft_if(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	if len(args) > 3 or len(args) < 2:
		raise Exception(f'Malformed if statement at:\n{args}')

	# Testing condition
	c = args[0]

	# Run the THEN function if the condition is equal to True
	if handle_expression(c) if isinstance(c, dict) else handle_value(c):
		craft_push_scope()
		handle_expression(args[1])
		craft_pop_scope()

	# Handle ELSE clause if it was added
	elif len(args) == 3:
		craft_push_scope()
		handle_expression(args[2])
		craft_pop_scope()


@branch()
@expose()
def craft_unless(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	if len(args) > 3 or len(args) < 2:
		raise Exception(f'Malformed unless statement at:\n{args}')

	# Testing condition
	c = args[0]

	# Run the THEN function if the condition is equal to True
	if not handle_expression(c) if isinstance(c, dict) else not handle_value(c):
		craft_push_scope()
		handle_expression(args[1])
		craft_pop_scope()

	# Handle ELSE clause if it was added
	elif len(args) == 3:
		craft_push_scope()
		handle_expression(args[2])
		craft_pop_scope()


@branch()
@expose()
def craft_then(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	args = get_args(args)


@branch()
@expose()
def craft_else(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	args = get_args(args)


@expose()
def craft_globals(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	#pp.pprint(SYMBOL_TABLE)
	#pp.pprint(EXCEPTIONS)
	return SYMBOL_TABLE, EXCEPTIONS


@expose()
def craft_locals(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	global SYMBOL_TABLE, SCOPE
	#pp.pprint(SYMBOL_TABLE[SCOPE])
	return SYMBOL_TABLE[SCOPE]


@expose()
def craft_exit(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	sys.exit()


@expose()
def craft_comment(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""


@expose()
def craft_print(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	print(*get_args(args))


@expose()
def craft_prin(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	print(*get_args(args), end='')


@branch()
@expose()
def craft_def(*args):
	"""
	Bind function name to variable in current scope. This will allow it to be
	called.
	"""
	declaration = get_arg_value(args[0])
	func_name = declaration[0]
	func_args = declaration[1:]
	func_definition = args[1:]

	#craft_set(func_name, [func_args, func_definition])
	craft_set(func_name, Function(func_name, [func_args, func_definition]))


@expose()
def craft_return(*args):
	"""
	The `craft_call` function will catch this exception and then return the
	value from it.
	"""
	if len(args) > 1:
		ex = f'Only 1 value can be returned from function, got {len(args)}.'

		# TODO(Pebaz): Should this return a tuple rather than crash?

		raise Exception(ex)

	value = get_arg_value(args[0])
	raise CraftFunctionReturnException(value)


@expose('fn')
def craft_lambda(*args):
	"""
	TODO(Pebaz): Fix `craft_call` to be able to handle lambdas.
	"""
	arguments = get_arg_value(args[0])
	definition = args[1:]
	#return [arguments, definition]
	return Function('lambda', [arguments, definition])


@expose()
def craft_struct(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	args = get_args(args)
	struct_name = args[0]
	struct_members = args[1:]
	craft_set(struct_name, struct_members)


@expose()
def craft_new(*args):
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


@expose('Program')
def craft_program(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	global TRACEBACK

	# NOTE(Pebaz): To show a Python internal error, simply call: get_args(args)
	# TODO(Pebaz): Make it so that a command line switch can show the traceback

	if True:
		try:
			return get_args(args)
		except Exception as e:
			TRACEBACK.show_trace(e)
	else:
		return get_args(args)


@expose()
def craft_byval(*args):
	"""
	Since functions only try one round of evaluation for arguments, arguments
	can be passed "by value" instead of "by reference/name".
	"""
	return args[0]


@expose()
def craft_byref(*args):
	"""
	Wrap the dictionary in a protective layer.
	"""
	return get_args(args)[0]


@expose()
def craft_dir(value):
	"""
	Equivalent to `dir()` in Python.
	"""
	#global pp
	if isinstance(value, str):
		#pp.pprint(get_arg_value(value))
		return get_arg_value(value)
	#elif isinstance(value, dict):
	#	pp.pprint(dict)


@expose('fmt')
def craft_format(*args):
	"""
	Formats a given string with the given arguments.

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	args = get_args(args)
	return args[0].format(*args[1:])


@expose()
def get_result(*args):
	"""
	Args:
		val(object): the object to return from a JIT-compiled function.
		err(Exception): the error that occurred.
	"""
	args = get_args(args)
	val, err = args
	return Result(val, err)


@expose()
def craft_eval(*args):
	"""
	Evaluate a given chunk of code, without introducing a new scope and without
	capturing errors. Propogates errors up so that they can be caught
	elsewhere.

	Primary use case of this function is via the Jit compiler. Code branches
	are evaluated using this function and errors need to be caught by the one
	who called this function, not this function itself.

	It is important to note that this function can access names within the
	scope that called it.
	"""
	get_args(args)


@expose()
def craft_type(*args):
	"""
	Args:
		obj(object): return the type name of this object's class.
	"""
	obj = get_args(args)[0]
	return type(obj).__name__


@expose()
def craft_sleep(*args):
	"""
	Args:
		duration_in_seconds(float): the amount of time to sleep in seconds.
	"""
	duration_in_seconds = get_args(args)[0]
	time.sleep(duration_in_seconds)


@expose()
def craft_get(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	if len(args) > 2:
		raise Exception(f'Too many arguments supplied, got: {len(args)}')

	args = get_args(args)
	return args[0][args[1]]


@expose()
def craft_cut(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	args = get_args(args)
	raise Exception('Not implemented yet: cut')


@expose()
def craft_len(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	args = get_args(args)
	return len(args[0])


# -----------------------------------------------------------------------------
# Data Types
# -----------------------------------------------------------------------------

@expose()
def craft_hash(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	if len(args) % 2 != 0:
		raise Exception(f'Expected even number of arguments, got {len(args)}.')

	args = get_args(args)

	ret = {
		args[i] : args[i + 1]
		for i in range(0, len(args), 2)
	}

	return ret
	

@expose()
def craft_str(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	return str(get_arg_value(args[0]))


@expose()
def craft_int(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	return int(get_arg_value(args[0]))


@expose()
def craft_bool(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	return bool(get_arg_value(args[0]))


@expose()
def craft_float(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	return float(get_arg_value(args[0]))


@expose()
def craft_tuple(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	if len(args) == 0:
		raise Exception(f'Expected a list of values, got nothing.')
	return tuple(get_arg_value(args[0]))


@expose()
def craft_list(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	return list(get_arg_value(args[0]))


@expose()
def craft_collected_set(*args):
	"""
	<Short Description>

	<Long Description>

	Args:
	  <Argument List>

	Returns:
	  <Description of Return Value>
	"""
	return set(get_arg_value(args[0]))
