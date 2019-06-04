import ctypes
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
comp.add_library_path('./')
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
