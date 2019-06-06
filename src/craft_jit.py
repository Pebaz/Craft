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


class Craft:
	def __init__(self):
		self.name = "Pebaz"
		self.asdf = lambda: [1, 2, 3]
		self.print = print

CRAFT = Craft()


print(':: Compiling                      ::')
comp = TCC()
comp.preprocessor_symbols["DEBUG"] = "1"
comp.add_include_path('C:/Python37/include')
comp.add_library_path('C:/Python37')
comp.add_library('python37')
# Don't use add_file() because it causes the Python interpreter to hang when
# Certain functions are called in C such as PyObject_Call()... No idea why
# just include C files as normal in the code.
#comp.add_file('jit/craft_common.c')
comp.compile_file('jit/test.c')
comp.relocate()
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

craft_main = craft_main_proto(comp.get_symbol('craft_main'))

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

		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		var_num = itertools.count()

		print(':: Transpiling            ::')
		print(ast, '\n\n')
		print('=-' * 20)

		emit(self.__load_template('header.c'))

		# Bind arguments to values
		for i, arg in enumerate(arg_names):
			emit(f'    PyObject * {arg} = PyList_GetItem(ARGS, {i});')


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
				emit(f'    PyObject * {aname} = Py_BuildValue("s", "{argument}");')
				bound_arg_names.append(aname)

			func_var = f'var{next(var_num)}'
			func_var_args = f'CALL_{func_var}_args{next(var_num)}'
			emit(f'    PyObject * {func_var} = query_symbol_table(SYMBOL_TABLE, SCOPE, "{func_name}");')
			emit(f'    PyObject * {func_var_args} = PyTuple_New({len(arguments)});')
			for index, aname in enumerate(bound_arg_names):
				emit(f'    PyTuple_SET_ITEM({func_var_args}, {len(arguments) - 1 - index}, {aname});')

			emit(f'    PyObject_Call({func_var}, {func_var_args}, NULL);')
			emit()

		# Return type?

		emit(self.__load_template('footer.c'))
		print('-=' * 20)
		return '\n'.join(source)

	def compile(self, code):
		comp = TCC()
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
	[hello]
	print: ["Hello World!"]
	:: This crashes sometimes...
	:: I think it has to do with the length of the string...
	print: ["Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!"]
	:: print: ["This is run from JITted Craft code :D"]
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
CALL(__code__, [])
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

