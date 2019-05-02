"""
Using library: https://github.com/frxstrem/pytcc
"""

import ctypes, pytcc
import sys
from pathlib import Path


# python_dll = ctypes.PyDLL(name)


# Compile the small Python extension
jit_code = pytcc.TCCState()
jit_code.add_include_path("C:/Python37/include")
jit_code.add_library_path("C:/Python37")
jit_code.add_library("python37")
jit_code.set_options("-shared")
jit_code.add_file("mini_ext.c")
jit_code.output_file("mini_ext.dll")
# jit_code.relocate()

pyd = ctypes.PyDLL("mini_ext.dll")
foobar_proto = ctypes.CFUNCTYPE(ctypes.c_int)
foobar = foobar_proto(("foobar", pyd))

sys.exit(0)

# while True:
# 	pass

# int foobar()
foobar_proto = ctypes.CFUNCTYPE(ctypes.c_int)
foobar = foobar_proto(jit_code.get_symbol("foobar"))

print(f"It works: {foobar()}")

# PyObject * pop()
pop_proto = ctypes.PYFUNCTYPE(ctypes.py_object)
pop = pop_proto(jit_code.get_symbol("pop"))

print("But this does not for some reason:")
print(pop())
print("Never gets here due to access violation :(")
