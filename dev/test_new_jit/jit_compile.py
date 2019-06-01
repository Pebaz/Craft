import ctypes
from pytcc import TCC

comp = TCC()
comp.add_include_path('C:/Python37/include')
comp.add_library_path('./')
comp.add_library_path('C:/Python37')
comp.add_library('python37')
# comp.add_file("hello.c")
# comp.compile_string('')
comp.compile_file('hello.c')
comp.relocate()

craft_main_proto = ctypes.CFUNCTYPE(ctypes.py_object)
craft_main = craft_main_proto(comp.get_symbol('craft_main'))
print(craft_main())

print(dir(comp))
