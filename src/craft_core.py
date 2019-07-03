
import sys, os, os.path, traceback, imp, inspect
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yaml
import pyparsing as pyp
from docopt import docopt


from craft_exceptions import *
from craft_colors import *


# -----------------------------------------------------------------------------
#                          W I N G   I N T E R N A L S
# -----------------------------------------------------------------------------

def is_identifier(string):
	"""
	Checks to see if a given string is a proper Craft identifier.
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
	Checks to see if a given set of keys can index a dictionary.

	If there is an issue with even one of the keys, return False, else True.
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
	Returns the value of or evaluates a given function argument.
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
	Returns the key of a one-element dictionary.

	Since Craft functions are represented like so in AST:
	{'func-name' : [arg1, 'arg2', 3, 4.0]}
	There needs to be a way of getting the key of the dictionary.
	"""
	#return [i for i in symbol.keys()][0]
	for i in symbol.keys():
		return i


def getvalue(symbol):
	"""
	Returns the value of a one-element dictionary.

	Since Craft functions are represented like so in AST:
	{'func-name' : [arg1, 'arg2', 3, 4.0]}
	There needs to be a way of getting the value of the dictionary.
	"""
	#return symbol[getkey(symbol)]
	for i in symbol.values():
		return i


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

	global SCOPE

	try:
		# Is it a variable:
		if isinstance(value, str):

			# Treat as variable if not second $
			if value.startswith('$'):
				if value[1] != '$':
					return query_symbol_table(value[1:], SCOPE)

				# Shorthand syntax for passing by value: $$var_name
				else:
					return value[1:]

		# Just return the value if there is nothing special about it
		return value

	except Exception as e:
		register_pyexception(e)
		craft_raise(type(e).__name__)


def handle_expression(dictn):
	"""
	Core interpreter functionality. Interprets a given function call.
	
	Uses the current scope and symbol table to lookup names and set values.

	When a Craft function is called, if it is a Python `callable` object, it
	will be called rather than interpreted.

	JITted functions will appear as callables before and after compilation.
	"""
	global SCOPE, DEBUG, TRACEBACK
	func = query_symbol_table(getkey(dictn), SCOPE)

	# Add the function name to the traceback
	# UNDO(Pebaz):
	the_args = [
		getkey(i) if isinstance(i, dict)
		else get_arg_value(i)
		for i in getvalue(dictn)
	]

	TRACEBACK.add_trace(getkey(dictn), the_args)

	if DEBUG:
		print(f'Expression: {"    " * SCOPE + getkey(dictn)}')

	# Function is Python built-in function or operator
	# This is for argument passing
	try:
		# Python function
		if callable(func):
			return func(*getvalue(dictn))

		# Craft function
		else:
			return craft_call(getkey(dictn), *getvalue(dictn))

	# These Exceptions are not errors so pass them on to be caught by craft_call
	except (CraftFunctionReturnException, CraftLoopBreakException, CraftLoopContinueException) as e:
		raise e

	except Exception as e:
		register_pyexception(e)
		craft_raise(type(e).__name__)



def push_return_point():
	"""
	Adds the scope at the current execution point in the event of a function
	return or an exception occurs.
	"""
	global RETURN_POINTS, SCOPE
	RETURN_POINTS.append(SCOPE)


def pop_return_point():
	"""
	Return the scope that Craft should return to after a function call or
	an exception occurs.
	"""
	global RETURN_POINTS
	return RETURN_POINTS.pop()


def cull_scopes(return_point):
	"""
	Removes scopes that were pushed but destroyed after a call to:
	`pop_return_point()`.
	"""
	global SCOPE
	for i in range(SCOPE - return_point):
		craft_pop_scope()


def craft_exec(*args):
	"""
	Call a function definition.

	A function definition is defined as:
	[[arg-name1 arg-name2] [body body body]]
	"""
	args = get_args(args)
	func_def, func_args = args
	arg_names, func_definition = func_def

	if len(arg_names) != len(func_args):
		err = f'Argument count mismatch for function: '
		err += f'Expected {len(arg_names)}, got {len(func_args)}.'
		raise Exception(err)

	# Scope index to return to after call is done
	push_return_point()

	# Push a new scope to bind all local variables to
	craft_push_scope()

	# Bind each variable to the new function scope
	for i in range(len(arg_names)):
		craft_set(arg_names[i], func_args[i])

	# Return value
	return_value = None

	# Handle each statement in the function
	for statement in func_definition:

		# Run the statement
		try:
			get_arg_value(statement)

		# Improper usage of keywords
		except (CraftLoopBreakException, CraftLoopContinueException):
			raise Exception(f'BREAK or CONTINUE used outside of loop: {statement}')

		# Get return value and stop handling expressions
		except CraftFunctionReturnException as wfre:
			return_value = wfre.return_value
			break

		# A real error has occurred :(
		except Exception as e:
			raise e from e


	# Return the scope to where it was before the call,
	# deleting any scopes in between
	return_point = pop_return_point()

	# Delete dangling scopes
	cull_scopes(return_point)

	# Return the value returned from the function (if any)
	return return_value


def craft_call(*args):
	"""
	Call a Craft function by name with arguments.
	"""
	global SCOPE

	args = get_args(args)
	func_name = args[0]
	func_args = args[1:]
	arg_names, func_definition = query_symbol_table(func_name, SCOPE)

	return craft_exec([arg_names, func_definition], func_args)


def craft_set(name, value):
	"""
	This function does not evaluate arguments because it needs the raw variable
	value untouched. For instance, if a map (dict) is passed, it will get run
	as a function rather than a value. This enforces that the value passed is
	exactly the value that is set.
	"""
	global SYMBOL_TABLE, SCOPE

	if not is_identifier(name):
		raise Exception(f'"{name}" not a valid identifier.')

	value = get_arg_value(value)
	keys = name.split('.')
	var_name = keys[-1]
	scope = SCOPE + 0

	# Look for an existing value to override
	while scope > 0:
		if len(keys) > 1:
			try:
				if var_name in dict_recursive_get(SYMBOL_TABLE[scope], keys[:-1])[var_name]:
					dict_recursive_get(SYMBOL_TABLE[scope], keys[:-1])[var_name] = value
					return
			except:
				pass
		else:
			if var_name in SYMBOL_TABLE[scope]:
				SYMBOL_TABLE[scope][var_name] = value
				return
		scope -= 1

	# If it doesn't exist, just set a new one
	if len(keys) > 1:
		dict_recursive_get(SYMBOL_TABLE[SCOPE], keys[:-1])[var_name] = value
	else:
		SYMBOL_TABLE[SCOPE][var_name] = value


def craft_create_named_scope(*args):
	"""
	Creates a new scope with a given name.

	Args:
		name(str): the name of the new scope.
	"""
	args = get_args(args)
	global SCOPE, SYMBOL_TABLE
	name = args[0]
	SYMBOL_TABLE[SCOPE][name] = dict()


def craft_get_symbol_table(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global SYMBOL_TABLE
	return SYMBOL_TABLE


def craft_get_scope(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global SCOPE
	return SCOPE


def craft_get_return_points(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global RETURN_POINTS
	return RETURN_POINTS


def craft_get_exceptions(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global EXCEPTIONS
	return EXCEPTIONS


def craft_get_traceback(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global TRACEBACK
	return TRACEBACK


def craft_get_path(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global CRAFT_PATH
	return CRAFT_PATH


def craft_get_is_debug(*args):
	"""
	Convenience function for the JIT compilation process.
	"""
	global IS_DEBUG
	return IS_DEBUG


def craft_push_scope():
	"""
	Create a new scope in the symbol table.
	"""
	global SCOPE, SYMBOL_TABLE
	SCOPE += 1
	SYMBOL_TABLE.append(dict())

	# UNDO(Pebaz):
	TRACEBACK.set_scope(SCOPE)


def craft_pop_scope():
	"""
	Delete a scope from the symbol table.
	"""
	global SCOPE, SYMBOL_TABLE, TRACEBACK
	SCOPE -= 1
	SYMBOL_TABLE.pop()

	# UNDO(Pebaz):
	TRACEBACK.set_scope(SCOPE)


def register_exception(name, desc, *args):
	"""
	Registers a new Exception with a new name and description of itself.
	An error code is added by default.

	 1. Register the exception as a variable with the exact name in scope level
		zero.
	 2. The exception can be raised using the name:
			 raise: [CraftException]

		Using the error code:
			raise: [1]

		Using the lookup for the error code:
			raise: [$CraftException]
	"""
	global EXCEPTIONS, SYMBOL_TABLE

	if name in EXCEPTIONS:
		return

	error_code = (len(EXCEPTIONS) / 2) + 1

	EXCEPTIONS[name] = {'name' : name, 'desc' : desc, 'meta' : args}
	EXCEPTIONS[error_code] = {'name' : name, 'desc' : desc, 'meta' : args}

	#craft_set(name, error_code)
	# Manually place exception var in global namespace
	SYMBOL_TABLE[0][name] = error_code


def register_pyexception(exception):
	"""
	Registers a new PyException.

	Args:
		exception(Exception): the exception object to register.
	"""
	global EXCEPTIONS, SYMBOL_TABLE

	name = type(exception).__name__

	if name in EXCEPTIONS:
		return

	desc = exception.args[0] if len(exception.args) > 0 else None
	meta = exception.args[1:] if len(exception.args) > 1 else None

	error_code = int((len(EXCEPTIONS) / 2) + 1)
	EXCEPTIONS[name]       = {'name' : name, 'desc' : desc, 'meta' : None}
	EXCEPTIONS[error_code] = {'name' : name, 'desc' : desc, 'meta' : None}

	#craft_set(name, error_code)
	# Manually place exception var in global namespace
	SYMBOL_TABLE[0][name] = error_code


def craft_raise(error_code, *args):
	"""
	Raises the given exception if it exists in the EXCEPTION list.
	"""
	global EXCEPTIONS, SCOPE

	if isinstance(error_code, str):
		error_code = query_symbol_table(error_code, SCOPE)

	name = EXCEPTIONS[error_code]['name']
	desc = EXCEPTIONS[error_code]['desc']
	meta = EXCEPTIONS[error_code]['meta'] if len(args) == 0 else args

	craft_exception = type(
		name,
		(Exception,),
		{
			'__init__' : lambda self: Exception.__init__(self, self.desc),
			'name' : name,
			'desc' : desc,
			'meta' : meta
		}
	)

	raise craft_exception


class Result:
	"""
	Used within JIT compiled functions to return either an error or a value
	back to Python.
	"""
	def __init__(self, value, err=False):
		self.value = value
		self.err = err


class Function(list):
	"""
	Since `craft_def()` defines functions as lists in SYMBOL_TABLE, it need to
	keep compatibility with this. However, it also need to JIT compile the body
	of the function asynchronously.
	"""
	def __init__(self, *args):
		global JIT_COMPILER
		self.name = args[0]
		list_args = args[1]
		list.__init__(self, list_args)
		self.__jit__ = self.compile_self() if JIT_COMPILER.ENABLED else None
		self.__code__ = None
		self.saved_hash = hash(self)

	def __repr__(self):
		"""
		Returns either the repr of `Function` or `JITFunction`.
		
		Proves useful when wanting a visible confirmation that a function has
		successfully been JITted.
		"""
		if self.__code__:
			return f'<{self.__code__.__class__.__name__} {self.name}:[]>'
		else:
			return f'<{self.__class__.__name__} {self.name}:[]>'

	def __call__(self, *args):
		"""
		Since calling a user-defined function will always call a callable, it
		need to only call the JIT compiled function if the hash hasn't changed.
		If it has, just `craft_exec(self, args)` which should do the trick.
		"""
		if not JIT_COMPILER.ENABLED:
			return craft_exec(self, args)
		
		# If the hash changed, we need to recompile
		#if hash(self) != self.saved_hash:
		#   if JIT_COMPILER.ENABLED: !!!
		#	self.__code__ = self.compile_self()

		# Call the JIT func if it is done compiling, else interpret self
		if not self.__jit__.ready():
			return craft_exec(self, args)

		# Whether done or already done, update the callable and call it
		else:
			self.__code__ = self.__jit__.get()
			# Guard against OSError: Access Violation Writing ...
			try:
				#return craft_exec(self, args)
				# To call __code__, JITFunction.__call__(*args) is defined.
				# So unpack the tuple of arguments for __call__().
				return self.__code__(*args)
			except OSError:
				return craft_exec(self, args)

	def __hash__(self):
		"""
		The string representation of the function body is fine for hashing.
		"""
		return hash(str(self))

	def compile_self(self):
		"""
		Convenience method to recompile the function defined within `self`.
		"""
		global JIT_COMPILER
		return JIT_COMPILER.compile({
			'def' : [
				[self.name] + self[0],
				*self[1]
			]
		})


def branch(name=None):
	"""
	Mark built-in function as branches so that they will be interpreted rather
	than JIT-compiled.

	Usage:

	>>> @branch()  # Don't forget to call it
	>>> def craft_something(*args):
	...     pass

	>>> @branch('some')  # Explicit name given
	>>> def craft_something(*args):
	...     pass
	"""
	def inner(func):
		nonlocal name
		if not name:
			name = func.__name__.replace('craft_', '')

		global BRANCH_FUNCTIONS
		BRANCH_FUNCTIONS.append(name)
		def wrapper(*args, **kwargs):
			func(*args, **kwargs)
		return wrapper
	return inner


def expose(name=None):
	def builtin(func):
		nonlocal name

		frame_records = inspect.stack()[1]
		current_module = inspect.getmodule(frame_records[0])

		if '__craft__' not in dir(current_module):
			setattr(current_module, '__craft__', dict())

		if not name:
			name = func.__name__.replace('craft_', '').replace('_', '-')

		current_module.__craft__[name] = func
		return func
	return builtin


class Trace:
	"""
	Provides a nice looking traceback when an exception happens.

	Shows every function call including the actual values passed to those
	functions since the error occurred up to `history` entries.
	"""
	def __init__(self, history=100):
		self.traceback = list()
		self.history = history

	def reset(self):
		self.traceback = list()

	def banner(self, text):
		print(_CLRfr, end='')
		print('-' * (len(text) + 2), file=sys.stderr)
		print('', text, file=sys.stderr)
		print('-' * (len(text) + 2), file=sys.stderr, end='')
		print(_CLRreset, file=sys.stderr)

	def add_trace(self, func_name, args):
		"""
		Append a new function call to the history list for displaying later.
		"""
		self.traceback.append((func_name, args))
		if len(self.traceback) > self.history:
			self.traceback = self.traceback[1:]

	def set_scope(self, scope):
		self.traceback.append(scope)

	def show_trace(self, error):
		"""
		Display a nice-looking "stack trace".
		"""

		print()
		self.banner(f'{error.name}: {error.desc}')
		print('\nCall stack trace:\n')

		# The index of the last function call (not scope popping)
		last_func_call_index = -1

		# Since both func calls and scope indexes are present, find a func call
		while isinstance(self.traceback[last_func_call_index], int):
			last_func_call_index -= 1

		tab = 0
		for i in self.traceback[1:last_func_call_index]:
			if isinstance(i, int):
				tab = i
				continue
			print(('    ' * tab), f'{_CLRfy}{i[0]}{_CLRreset}\t', *i[1:])

		# Get the function call that caused the error:
		fcall = self.traceback[last_func_call_index]

		# Print a customized stacktrace that shows the function call that failed
		print(('    ' * tab), f'{_CLRfy}{fcall[0]}{_CLRreset}\t', *fcall[1:])
		print()
		print(('    ' * tab), '^')
		for i in range(4):
			print(('    ' * tab), '|')
		print()
		print(('    ' * tab), f'{_CLRfy}Responsible Function Call{_CLRreset}')



# -----------------------------------------------------------------------------
#             W I N G   I N I T I A L   S Y M B O L   T A B L E
# -----------------------------------------------------------------------------

# Represents a list of lists of key-value pairs (variables/names)
SYMBOL_TABLE = []

# The current scope (used as index to SYMBOL_TABLE)
SCOPE = 0

# Function call save points
RETURN_POINTS = []

# List of all recorded exceptions for raising and catching
EXCEPTIONS = dict()

# Global traceback object for printing tracebacks
TRACEBACK = Trace()

# Preset path of the Craft interpreter
CRAFT_PATH = [os.getcwd(), 'stdlib']

# Internal debugging flag
DEBUG = False

# List of functions that need to skip JIT compilation due to branching logic
BRANCH_FUNCTIONS = []

# Global JIT compiler object
import craft_jit; JIT_COMPILER = craft_jit.JIT()


def setup_sym_tab():
	"""
	Sets up the symbol table with all of the builtin functions, operators, and
	anything else it needs in order to be in a default state.
	"""
	# TODO(Pebaz): What else needs to be cleared?
	SYMBOL_TABLE.clear()
	RETURN_POINTS.clear()

	import craft_operators
	import craft_keywords
	import craft_exceptions
	SYMBOL_TABLE.append(dict())
	SYMBOL_TABLE[0].update(craft_operators.__craft__)
	SYMBOL_TABLE[0].update(craft_keywords.__craft__)
	SYMBOL_TABLE[0].update(craft_exceptions.__craft__)
