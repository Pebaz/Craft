import ctypes
from pytcc import TCC

def myprint():
    #print(arg)
	return ['Hello World!']

def square(n):
    return n ** 2

class Craft:
	def __init__(self):
		self.name = "Pebaz"
		self.asdf = lambda: [1, 2, 3]

CRAFT = Craft()

comp = TCC()
comp.preprocessor_symbols["DEBUG"] = "1"
comp.add_include_path('C:/Python37/include')
comp.add_library_path('./')
comp.add_library_path('C:/Python37')
comp.add_library('python37')


squaresignature = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
func = squaresignature(square)
pyprint = ctypes.CFUNCTYPE(ctypes.py_object)

comp.add_symbol("pyprint", pyprint(myprint))
comp.add_symbol("square", func)

comp.compile_file('hello.c')
comp.relocate()

print(":: Running JIT Compiled Code ::")
craft_main_proto = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)
craft_main = craft_main_proto(comp.get_symbol('craft_main'))

print(craft_main(CRAFT, print))

print(":: Done running JIT Compiled Code ::")
