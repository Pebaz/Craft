
import sys, os, os.path, traceback, imp
from collections import deque
from pathlib import Path
import yaml
import pyparsing as pyp
from docopt import docopt


from wing_exceptions import *


# -----------------------------------------------------------------------------
#                          W I N G   I N T E R N A L S
# -----------------------------------------------------------------------------

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

		# Treat as variable if not second $
		if value.startswith('$'):
			if value[1] != '$':
				return query_symbol_table(value[1:], SCOPE)

			# Shorthand syntax for passing by value: $$var_name
			else:
				return value[1:]

	# Just return the value if there is nothing special about it
	return value


def handle_expression(dictn):
	"""
	"""
	global SCOPE, DEBUG
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
	if callable(func):

		# TODO(Pebaz): Handle Python exceptions here and translate to Wing ones
		try:
			return func(*getvalue(dictn))
		except Exception as e:
			register_pyexception(e)
			wing_raise(type(e).__name__)

	# Function is defined in Wing
	# Pass it's name to the call function
	else:

		# TODO(Pebaz): Handle Wing exceptions here
		# TODO(Pebaz): If WingException is returned, how to fix all the other
		# functions from catching it before here? Will this `try` be able to
		# capture it?

		try:
			return wing_call(getkey(dictn), *getvalue(dictn))
		except Exception as e:
			register_pyexception(e)
			wing_raise(type(e).__name__)


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


def cull_scopes(return_point):
	"""
	Removes scopes that were pushed but destroyed after a call to:
	`pop_return_point()`.
	"""
	for i in range(SCOPE - return_point):
		wing_pop_scope()


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

		# Improper usage of keywords
		except (WingLoopBreakException, WingLoopContinueException):
			raise Exception(f'BREAK or CONTINUE used outside of loop: {statement}')

		# Get return value and stop handling expressions
		except WingFunctionReturnException as wfre:
			return_value = wfre.return_value
			break

		# A real error has occurred :(
		except Exception as e:

			# TODO(Pebaz): Remove this and raise new exception for
			# handle_expression() to handle.
			# raise WingException("SOMETHING TERRIBLE HAS HAPPENED", e)
			# -----> traceback.print_exc()
			# -----> break

			# TODO(Pebaz): Exit early and raise a new WingException now.
			# It will be caught by handle_expression.
			raise e from e


	# Return the scope to where it was before the call,
	# deleting any scopes in between
	return_point = pop_return_point()

	# Delete dangling scopes
	cull_scopes(return_point)

	# Return the value returned from the function (if any)
	return return_value

def wing_set(name, value):
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

	if len(keys) > 1:
		dict_recursive_get(SYMBOL_TABLE[SCOPE], keys[:-1])[var_name] = value
	else:
		SYMBOL_TABLE[SCOPE][var_name] = value

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

	# UNDO(Pebaz):
	TRACEBACK.set_scope(SCOPE)


def wing_pop_scope():
	"""
	"""
	global SCOPE, SYMBOL_TABLE
	SCOPE -= 1
	SYMBOL_TABLE.pop()

	# UNDO(Pebaz):
	TRACEBACK.set_scope(SCOPE)


def register_exception(name, desc):
	"""
	Registers a new Exception with a new name and description of itself.
	An error code is added by default.

	 1. Register the exception as a variable with the exact name in scope level
	    zero.
	 2. The exception can be raised using the name:
	 		raise: [WingException]

		Using the error code:
			raise: [1]

		Using the lookup for the error code:
			raise: [$WingException]
	"""
	global EXCEPTIONS

	if name in EXCEPTIONS:
		return

	error_code = (len(EXCEPTIONS) / 2) + 1

	EXCEPTIONS[name] = {'name' : name, 'desc' : desc, 'meta' : None}
	EXCEPTIONS[error_code] = {'name' : name, 'desc' : desc, 'meta' : None}

	wing_set(name, error_code)


def register_pyexception(exception):
	"""
	Registers a new PyException.

	Args:
		exception(Exception): the exception object to register.
	"""
	global EXCEPTIONS

	name = type(exception).__name__

	if name in EXCEPTIONS:
		return

	desc = exception.args[0] if len(exception.args) > 0 else None
	meta = exception.args[1:] if len(exception.args) > 1 else None

	error_code = (len(EXCEPTIONS) / 2) + 1
	EXCEPTIONS[name] = {'name' : name, 'desc' : desc, 'meta' : None}
	EXCEPTIONS[error_code] = {'name' : name, 'desc' : desc, 'meta' : None}

	wing_set(name, error_code)


def wing_raise(error_code):
	"""
	Raises the given exception if it exists in the EXCEPTION list.
	"""
	global EXCEPTIONS, SCOPE
	args = get_arg_value(error_code)

	if isinstance(error_code, str):
		error_code = query_symbol_table(error_code, SCOPE)

	name = EXCEPTIONS[error_code]['name']
	desc = EXCEPTIONS[error_code]['desc']
	meta = EXCEPTIONS[error_code]['meta']

	# Dynamically create a new Exception subclass and raise it
	wing_exception = type(
		name,
		(Exception,),
		{
			'__init__' : lambda self: Exception.__init__(self, self.desc),
			'name' : name,
			'desc' : desc,
			'meta' : meta
		}
	)
	raise wing_exception



# -----------------------------------------------------------------------------
#             W I N G   I N I T I A L   S Y M B O L   T A B L E
# -----------------------------------------------------------------------------


class Trace:
	def __init__(self, history=10):
		self.traceback = list()
		self.history = history

	def banner(self, text):
		print('-' * (len(text) + 2))
		print('', text)
		print('-' * (len(text) + 2))

	def add_trace(self, func_name, args):
		self.traceback.append((func_name, args))
		if len(self.traceback) > self.history:
			self.traceback = self.traceback[1:]

	def set_scope(self, scope):
		self.traceback.append(scope)

	def show_trace(self, error):
		print()
		self.banner(f'{error.name}: {error.desc}')
		print(error.meta) if error.meta != None else print('')

		tab = 0
		for i in self.traceback[1:-1]:
			if isinstance(i, int):
				tab = i
				continue
			print(('    ' * tab)[:-1], i[0], *i[1:])

		print('\nFunction call that caused the error:')
		fcall = self.traceback[-1]
		print(('    ' * tab)[:-1], fcall[0], *fcall[1:])


# Represents a list of lists of key-value pairs (variables/names)
SYMBOL_TABLE = []
SCOPE = 0 # For now, functions have to increment and decrement scope
RETURN_POINTS = []
EXCEPTIONS = dict()
TRACEBACK = Trace()
WING_PATH = [os.getcwd(), 'X:/Wing/stdlib']
DEBUG = False
