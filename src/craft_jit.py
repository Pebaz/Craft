"""
Notes:

 * Only run `craft --jit` from CMD.exe on Windows, not PowerShell due to [this]
   (https://stackoverflow.com/questions/39796424/running-python-in-powershell-crashes).
   For more on this, see [this](https://bugs.python.org/issue10920)

 * Never use `TCC.add_file()` as it somehow causes the Python interpreter to
   hang when certain functions are called in C such as PyObject_Call()... No
   idea why, just include C files as normal in the code.

 * The same code can sometimes crash or work just fine. Either way, reboot your
   terminal every once and a while during development.
"""

import ctypes, pathlib, itertools, traceback, time
#from pytcc import TCC
from pytcc import TCCState as TCC

from j2do               import j2do
from craft_core 		import *
from craft_parser 		import *
from craft_exceptions 	import *
from craft_cli 			import *
from craft_interpreter 	import *


setup_sym_tab()

# Lambda to get the system current time millis
ctm = lambda: int(round(time.time() * 1000))

if False:
	print(':: Compiling                      ::')
	compiler = TCC()
	compiler.preprocessor_symbols["DEBUG"] = "1"
	compiler.add_include_path('C:/Python37/include')
	compiler.add_library_path('C:/Python37')
	compiler.add_library('python37')
	# Don't use add_file() because it causes the Python interpreter to hang when
	# Certain functions are called in C such as PyObject_Call()... No idea why
	# just include C files as normal in the code.
	#compiler.add_file('jit/craft_common.c')
	compiler.compile_file('jit/test.c')
	compiler.relocate()
	print(':: Done                           ::')

	print(":: Running JIT Compiled Code      ::")
	craft_main_proto = ctypes.CFUNCTYPE(
		ctypes.py_object,  # Return type
		ctypes.py_object,  # SYMBOL_TABLE
		ctypes.py_object,  # SCOPE
		ctypes.py_object,  # RETURN_POINTS
		ctypes.py_object,  # EXCEPTIONS
		ctypes.py_object,  # TRACEBACK
		ctypes.py_object,  # CRAFT_PATH
		ctypes.py_object,  # DEBUG
	)

	craft_main = craft_main_proto(compiler.get_symbol('craft_main'))

	#ret = craft_main(CRAFT)
	try:
		# TODO(pebaz): Implement this using STRUCT?? import struct? (raylib)
		ret = craft_main(
			SYMBOL_TABLE,
			SCOPE,
			RETURN_POINTS,
			EXCEPTIONS,
			TRACEBACK,
			CRAFT_PATH,
			DEBUG
		)
		print(ret)
	except SystemError as e:
		print(f'!! Error                          !!')
		traceback.print_exc()
		


	print(":: Done running JIT Compiled Code ::")
	print()

if False:
	src = '''
	Program : [
		set: [name 'Pebaz']
		print : [$name]
	]
	'''
	ast = craft_parse(src)

	handle_expression({
		'Program' : [
			{
				'print': [
					'Hello World!'
				]
			}
		]
	})


# Python: Around 550 ms
# C: Around 530 ms

print('\n\n')


fibo = '''
def: [
	[fibo x]

	if: [
		<=: [$x 1]
		return: [$x]
	]

	return: [
		+: [
			fibo: [-: [$x 1]]
			fibo: [-: [$x 2]]
		]
	]
]
'''


class JIT:
	PATH_PREFIX = pathlib.Path() / 'jit'
	
	def get_source(self):
		return '\n'.join(self.source)

	def __load_template(self, filename):
		with open(str(JIT.PATH_PREFIX / filename)) as file:
			return file.read()

	def transpile(self, ast):
		source = []

		def emit(text=''):
			print(text)
			source.append(text)

		'''
		def emit_call(func, args, counter):
			"""
			This will be recursively called if an argument is a function call.
			It will also do all processing for scalar values.

			NOTE: `args` must be a list of C variable names.
			"""
			emit('')
			emit(f'    // Lookup Function: {func}')
			func_var = emit_lookup(func, counter)
			emit('    // Now Call Function')
			func_var_args = f'ARGS_{func_var}{next(counter)}'
			return_value = f'RET_{func_var}{next(counter)}'
			emit(f'    PyObject * {func_var_args} = PyTuple_New({len(args)});')
			for i, arg in enumerate(args):
				emit(f'    PyTuple_SET_ITEM({func_var_args}, {i}, {arg});')
			emit(f'    PyObject * {return_value} = PyObject_Call({func_var}, {func_var_args}, NULL);')
			return return_value
		'''

		def emit_lookup(name, counter):
			ARGS_query = f'ARGS_query{next(counter)}'
			lookup = f'var{next(counter)}'
			emit(f'    PyObject * {ARGS_query} = PyTuple_New(2);')
			emit(f'    PyTuple_SET_ITEM({ARGS_query}, 0, Py_BuildValue("s", "{name}"));')
			emit(f'    PyTuple_SET_ITEM({ARGS_query}, 1, PyObject_Call(scope, PyTuple_New(0), NULL));')
			emit(f'    PyObject * {lookup} = PyObject_Call(query, {ARGS_query}, NULL);')
			return lookup

		def emit_args(arguments, counter):
			bound_arg_names = []
			#for argument in reversed(arguments):
			for argument in arguments:
				aname = f'var{next(counter)}'

				# Argument lookup
				#if isinstance(argument, str) and argument.startswith('$') and argument[1:] in arg_names:
				#	emit(f'    PyObject * {aname} = {argument[1:]};')
				# vvv = emit_lookup(...)
				# bound_arg_names.append(vvv)
				# continue

				# Name lookup
				if isinstance(argument, str) and argument.startswith('$'):
					#lookup = argument[1:]

					# Second lookup
					if argument.startswith('$$'):
						emit(f'    PyObject * {aname} = Py_BuildValue("s", "{argument[1:]}");')
					else:
						#emit(f'    PyObject * {aname} = query_symbol_table(SYMBOL_TABLE, SCOPE, "{lookup}");')
						bound_arg_names.append(emit_lookup(argument[1:], counter))
						continue

				# Boolean Literal
				elif isinstance(argument, bool):
					emit(f'    PyObject * {aname} = {"Py_True" if argument else "Py_False"};')

				# String Literal
				elif isinstance(argument, str):
					emit(f'    PyObject * {aname} = Py_BuildValue("s", "{argument}");')

				# Integer Literal
				elif isinstance(argument, int):
					emit(f'    PyObject * {aname} = Py_BuildValue("i", {argument});')

				# Float Literal
				elif isinstance(argument, float):
					emit(f'    PyObject * {aname} = Py_BuildValue("f", {argument});')

				# List literal
				elif isinstance(argument, list):
					list_arg_names = emit_args(argument, counter)
					'''
					emit(f'    PyObject * {aname} = PyList_New({len(argument)});')
					for i, list_arg_name in enumerate(list_arg_names):
						#emit(f'    PyList_SetItem({aname}, {len(list_arg_names) - 1 - i}, {list_arg_name});')
						emit(f'    PyList_SetItem({aname}, {i}, {list_arg_name});')
					'''
					emit_template('list.j2', dict(
						aname = aname,
						argument = argument,
						list_arg_names = list_arg_names
					))

				# Function call
				elif isinstance(argument, dict):
					bound_arg_names.append(emit_func(argument, counter))
					continue

				bound_arg_names.append(aname)

			return bound_arg_names

		def emit_func(statement, counter):
			func_name = getkey(statement)
			arguments = getvalue(statement)
			bound_arg_names = emit_args(arguments, counter)

			#func_var = f'var{next(counter)}'
			emit(f'// LOOKUP {func_name}')
			func_var = emit_lookup(func_name, counter)
			func_var_args = f'CALL_{func_var}_args{next(counter)}'
			ret_name = f'var{next(counter)}'

			'''
			emit(f'    PyObject * {func_var} = query_symbol_table(SYMBOL_TABLE, SCOPE, "{func_name}");')
			emit(f'    PyObject * {func_var_args} = PyTuple_New({len(arguments)});')
			for index, aname in enumerate(bound_arg_names):
				emit(f'    PyTuple_SET_ITEM({func_var_args}, {len(arguments) - 1 - index}, {aname});')

			emit(f'    PyObject_Call({func_var}, {func_var_args}, NULL);')
			emit()
			'''

			data = dict(
				func_var = func_var,
				func_name = func_name,
				arguments = arguments,
				bound_arg_names = bound_arg_names,
				func_var_args = func_var_args,
				ret_name = ret_name
			)
			emit_template('call.j2', data)
			emit_template('error_check.j2', {})
			return ret_name

		def emit_template(template, data):
			emit(j2do(template, data, include=[JIT.PATH_PREFIX]))	

		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		counter = itertools.count()

		print(':: Transpiling            ::')
		print(ast, '\n\n')
		print('=-' * 20)

		emit('#include <stdio.h>')
		#emit(self.__load_template('header.c'))
		emit_template('header.j2', {})

		# Push Scope
		#emit(f'    PyObject * push_scope = query_symbol_table(SYMBOL_TABLE, SCOPE, "push-scope");')
		#emit_call('push-scope', [], counter)
		emit_func({'push-scope' : []}, counter)

		emit('')

		# Now Bind all arguments to current (function) scope
		'''
		emit('    // Now bind values to current function scope')
		emit(f'    PyObject * set = query_symbol_table(SYMBOL_TABLE, SCOPE, "set");')
		emit(f'    PyObject * ARGS_set = PyTuple_New(2);')
		for i, arg in enumerate(arg_names):
			emit(f'    PyTuple_SET_ITEM(ARGS_set, 0, Py_BuildValue("s", "{arg}"));')
			emit(f'    PyTuple_SET_ITEM(ARGS_set, 1, PyList_GetItem(ARGS, {i}));')
			emit(f'    PyObject_Call(set, ARGS_set, NULL);')
		'''
		emit(j2do(
			"arguments.j2",
			dict(arg_names=arg_names),
			include=[JIT.PATH_PREFIX]
		))

		emit('\n// BODY')

		sym_tab = emit_lookup('get-symbol-table', counter)
		#r = emit_call('print', [sym_tab], counter)
		r = emit_func({'print':[sym_tab]}, counter)

		# Function body
		is_statement = lambda x: isinstance(x, dict) and len(x) == 1
		for statement in body:
			if is_statement(statement):
				emit(f'\n// {statement}')
			else:
				raise CraftException('SyntaxError', {}, {})

			emit_func(statement, counter)

		# Pop Scope
		#emit(f'    PyObject * pop_scope = query_symbol_table(SYMBOL_TABLE, SCOPE, "pop-scope");')
		#emit(f'    PyObject_Call(pop_scope, PyTuple_New(0), NULL);')
		#emit_call('pop-scope', [], counter)
		emit_func({'pop-scope' : []}, counter)

		# Return type?
		# Catch FunctionReturnException... :(
		#emit(self.__load_template('footer.c'))

		emit_template('footer.j2', {})

		print('-=' * 20)
		return '\n'.join(source)

	def compile(self, code):
		#import pytcc
		from pytcc import TCCState as TCC
		comp = TCC()
		#comp.preprocessor_symbols["DEBUG"] = "1"
		comp.add_include_path('C:/Python37/include')
		comp.add_library_path('C:/Python37')
		comp.add_library('python37')

		# IMPORTANT(pebaz): Don't use add_file() because it causes the Python
		# interpreter to hang when certain functions are called in C such as
		# PyObject_Call()... No idea why just include C files as usual in code.
		#comp.add_file('jit/craft_common.c')

		try:
			print('Compiling...')
			comp.compile_string(code)
			print('Relocating...')
			comp.relocate()
		except:
			traceback.print_exc()
			return lambda ARGS, x, y, z, p, d, q, s: print('<Your func here>')

		print('Prototyping...')
		func_proto = ctypes.CFUNCTYPE(
			ctypes.py_object,  # Return type
			ctypes.py_object,  # ARGS
			ctypes.py_object,  # SYMBOL_TABLE
			ctypes.py_object,  # SCOPE
			ctypes.py_object,  # RETURN_POINTS
			ctypes.py_object,  # EXCEPTIONS
			ctypes.py_object,  # TRACEBACK
			ctypes.py_object,  # CRAFT_PATH
			ctypes.py_object,  # DEBUG
		)

		print('Getting Symbol...')
		a = comp.get_symbol('craft_main')
		print('FuncProto...')
		return func_proto(a)

	def compile_function(self, func):
		return self.compile(self.transpile(func))

# https://stackoverflow.com/questions/20232965/how-do-i-properly-use-pythons-c-api-and-exceptions
# https://www.programiz.com/python-programming/exception-handling
# https://docs.python.org/3/c-api/exceptions.html
hello = '''
def: [
	[hello person]
	print:[hi]
	::raise:[Exception]
	::/: [0 0]
	return: ["Hello World!"]
]
'''
hello = '''
def: [
	[fibo x]
	print: ["Within fibo() now"]

	if: [
		<=: [$x 1] then: [
			return: [$x]
		]
	]

	return: [
		+: [
			fibo: [-: [$x 1]]
			fibo: [-: [$x 2]]
		]
	]
]
'''
jit = JIT()
func = craft_parse(hello)

#jit.transpile(func)

#sys.exit(0)

__code__ = jit.compile_function(func)
craft_set(getvalue(func)[0][0], __code__)


def CALL(func, args):
	global SYMBOL_TABLE, SCOPE, RETURN_POINTS, EXCEPTIONS, TRACEBACK, CRAFT_PATH, DEBUG
	try:
		ret = func(
			args,
			SYMBOL_TABLE,
			SCOPE,
			RETURN_POINTS,
			EXCEPTIONS,
			TRACEBACK,
			CRAFT_PATH,
			DEBUG
		)

		if not ret.err:
			return ret.value
		else:
			register_pyexception(ret.err)
			craft_raise(type(ret.err).__name__)

	except SystemError as e:
		traceback.print_exc()

		

print('Running...')
print('\n------------------------')
ret = CALL(__code__, [10])
print('------------------------\nDone.')
print(f'Return Value: {repr(ret)}')


if False:
	hello2 = craft_parse('''
	Program: [
	def: [
		[hello]
		print: ["Hello World!" "1" "2"]
	]
	hello: []
	]
	''')
	times = 10
	start = ctm()
	for i in range(times):
		CALL(__code__, [])
	print('Time:', ctm() - start)
	start = ctm()
	for i in range(times):
		handle_expression(hello2)
	print('Time:', ctm() - start)

	# CONFUSED(pebaz): If you double click the craft_jit.py it works.
	# If you run it from the command line, it doesn't.




# Make sure to use craft_jit.py like craft_keywords
__craft__ = {
	
}
