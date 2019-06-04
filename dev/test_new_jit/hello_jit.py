import ctypes
from pytcc import TCC

class Craft:
	def __init__(self):
		self.name = "Pebaz"
		self.asdf = lambda: [1, 2, 3]
		self.print = print

CRAFT = Craft()

comp = TCC()
comp.preprocessor_symbols["DEBUG"] = "1"
comp.add_include_path('C:/Python37/include')
comp.add_library_path('./')
comp.add_library_path('C:/Python37')
comp.add_library('python37')
comp.compile_file('hello.c')
comp.relocate()

print(":: Running JIT Compiled Code ::")
craft_main_proto = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)
craft_main = craft_main_proto(comp.get_symbol('craft_main'))

ret = craft_main(CRAFT)
print(ret)

print(":: Done running JIT Compiled Code ::")
