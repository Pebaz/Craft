import ctypes, pathlib, itertools
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
millis = lambda: int(round(time.time() * 1000))


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


print(":: Done running JIT Compiled Code ::")

print()
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

hello = '''
def: [
	[hello]
	print: ["Hello World!"]
]
'''

class JIT:
	PATH_PREFIX = pathlib.Path() / 'jit'

	def __load_template(self, filename):
		with open(str(JIT.PATH_PREFIX / filename)) as file:
			return file.read()

	def transpile(self, ast):
		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		var_num = itertools.count()

		print(':: Transpiling            ::')
		print(ast, '\n\n')
		print('=-' * 20)

		print(self.__load_template('header.c'))

		# Bind arguments to values
		for i, arg in enumerate(arg_names):
			print(f'    PyObject * {arg} = PyList_GetItem(ARGS, {i});')


		# Function body
		is_statement = lambda x: isinstance(x, dict) and len(x) == 1
		for statement in body:
			if is_statement(statement):
				print(statement)
			else:
				raise CraftException('SyntaxError', {}, {})

			# Load global "print"
			func_name = getkey(statement)
			#print(f'    PyObject * var{next(var_num)} = PyDict_GetItemString(scope0, "{func_name}");')
			print(f'    PyObject * var{next(var_num)} = craft_get(')

		# Return type?

		print(self.__load_template('footer.c'))
		print('-=' * 20)
		return '...'

	def compile(self, code):
		return lambda ARGS, x, y, z, p, d, q, s: print('<Your module here>')

	def compile_function(self, func):
		return self.compile(self.transpile(func))



jit = JIT()
func = craft_parse(hello)
__code__ = jit.compile_function(func)
__code__(
	[],
	SYMBOL_TABLE,
	SCOPE,
	RETURN_POINTS,
	EXCEPTIONS,
	TRACEBACK,
	CRAFT_PATH,
	DEBUG
)
