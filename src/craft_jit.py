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
from pytcc import TCC

from craft_core 		import *
from craft_parser 		import *
from craft_exceptions 	import *
from craft_cli 			import *
from craft_interpreter 	import *

# Needed to import __craft__ dicts for built-in symbol table entries
import craft_operators
import craft_keywords

SYMBOL_TABLE.append(dict())
SYMBOL_TABLE[0].update(craft_operators.__craft__)
SYMBOL_TABLE[0].update(craft_keywords.__craft__)

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
		"""
		
		Plan:

		Some functions can be turned straight into their C equivalents.
		For instance, get:[] can be turned into array[index].
		Although that is slightly risky since the user could have occluded the
		get function with their own function. However, perhaps I could just check to see if they did?


		"""
		source = []
		def emit(text=''):
			print(text)
			source.append(text)

		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		var_num = itertools.count()

		print(':: Transpiling            ::')
		print(ast, '\n\n')
		print('=-' * 20)

		emit(self.__load_template('header.c'))
		emit('#include <stdio.h>')

		# Push Scope
		emit(f'    PyObject * push_scope = query_symbol_table(SYMBOL_TABLE, SCOPE, "push-scope");')
		emit(f'    PyObject_Call(push_scope, PyTuple_New(0), NULL);')

		#emit('printf("hi\\n");')

		emit('')

		# Bind arguments to values
		emit('    // Bind arguments to values')
		emit('    // Used for by-value usage.')
		emit('    // For references, lookup the value each time.')
		for i, arg in enumerate(arg_names):
			emit(f'    PyObject * {arg} = PyList_GetItem(ARGS, {i});')

		emit('')

		# Now Bind all arguments to current (function) scope
		emit('    // Now bind values to current function scope')
		emit(f'    PyObject * set = query_symbol_table(SYMBOL_TABLE, SCOPE, "set");')
		'''
		emit(f'    PyObject * ARGS_set = PyTuple_New(2);')
		for i, arg in enumerate(arg_names):
			emit(f'    PyTuple_SET_ITEM(ARGS_set, 0, Py_BuildValue("s", "{arg}"));')
			emit(f'    PyTuple_SET_ITEM(ARGS_set, 1, PyList_GetItem(ARGS, {i}));')
			emit(f'    PyObject_Call(set, ARGS_set, NULL);')
		'''
		emit('')

		# Function body
		is_statement = lambda x: isinstance(x, dict) and len(x) == 1
		for statement in body:
			if is_statement(statement):
				emit(f'    // {statement}')
			else:
				raise CraftException('SyntaxError', {}, {})

			# Load global "print"
			func_name = getkey(statement)
			arguments = getvalue(statement)

			# Emit the deepest argument first and assign it to a variable!
			bound_arg_names = []
			for argument in reversed(arguments):
				# Primitives first
				aname = f'var{next(var_num)}'

				# Argument lookup
				if isinstance(argument, str) and argument.startswith('$') and argument[1:] in arg_names:
					emit(f'    PyObject * {aname} = {argument[1:]};')
				# Name lookup
				elif isinstance(argument, str) and argument.startswith('$'):
					lookup = argument[1:]

					# Second lookup
					if lookup.startswith('$'):
						emit(f'    PyObject * {aname} = Py_BuildValue("s", "{lookup}");')
					else:
						emit(f'    PyObject * {aname} = query_symbol_table(SYMBOL_TABLE, SCOPE, "{argument[1:]}");')
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
					raise Exception('Need to recursively evaluate things in list.')

				bound_arg_names.append(aname)

			func_var = f'var{next(var_num)}'
			func_var_args = f'CALL_{func_var}_args{next(var_num)}'
			emit(f'    PyObject * {func_var} = query_symbol_table(SYMBOL_TABLE, SCOPE, "{func_name}");')
			emit(f'    PyObject * {func_var_args} = PyTuple_New({len(arguments)});')
			for index, aname in enumerate(bound_arg_names):
				emit(f'    PyTuple_SET_ITEM({func_var_args}, {len(arguments) - 1 - index}, {aname});')

			emit(f'    PyObject_Call({func_var}, {func_var_args}, NULL);')
			emit()

		# Pop Scope
		# This Crashes....
		emit(f'    PyObject * pop_scope = query_symbol_table(SYMBOL_TABLE, SCOPE, "pop-scope");')
		emit(f'    PyObject_Call(pop_scope, PyTuple_New(0), NULL);')

		# Return type?

		emit(self.__load_template('footer.c'))
		print('-=' * 20)
		return '\n'.join(source)

	def compile(self, code):
		import pytcc
		comp = pytcc.TCC()
		comp.preprocessor_symbols["DEBUG"] = "1"
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


hello = '''
def: [
	[hello person]
	print: ["Hello World!"]
	:: This crashes sometimes...
	:: I think it has to do with the length of the string...

	:: UPDATE: For some reason, it works in PowerShell as well as never fails here...
	:: print: ["Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!"]
	
	print: [$person]
]
'''
hello = '''
def: [
	[hello person]
	print: ["Hello World!"]
	print: [$person]
	print: [314]
	print: [3.14]
	print: [True]
	print: [False]
	print: [1 2 3 4 5]
	::print: [$$person]
]
'''
jit = JIT()
func = craft_parse(hello)
__code__ = jit.compile_function(func)


def CALL(func, args):
	global SYMBOL_TABLE, SCOPE, RETURN_POINTS, EXCEPTIONS, TRACEBACK, CRAFT_PATH, DEBUG
	return func(
		args,
		SYMBOL_TABLE,
		SCOPE,
		RETURN_POINTS,
		EXCEPTIONS,
		TRACEBACK,
		CRAFT_PATH,
		DEBUG
	)

print('Running...\n')

print('\n\n\n------------------------\n\n\n')
name = 'Pebaz123'
CALL(__code__, ['asdf'])
print('\nDone.')



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

