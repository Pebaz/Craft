"""
Using library: https://github.com/frxstrem/pytcc
"""

import ctypes, pytcc

program = b"""
#include "Python.h"

PyObject * pop(PyObject * self, PyObject * args, PyObject * kwargs) {
	return PyLong_FromLong(3);
}

int foobar() { return 3; }

// Needed to appease TCC:
int main() { }
"""

# Compile the small Python extension
jit_code = pytcc.TCCState()
jit_code.add_include_path("C:/Python37/include")
jit_code.add_library_path("C:/Python37")
jit_code.add_library("python37")
jit_code.compile_string(program)
jit_code.relocate()

# int foobar()
foobar_proto = ctypes.CFUNCTYPE(ctypes.c_int)
foobar = foobar_proto(jit_code.get_symbol("foobar"))

print(f"It works: {foobar()}")

# PyObject * pop()
pop_proto = ctypes.CFUNCTYPE(ctypes.c_voidp)
pop = pop_proto(jit_code.get_symbol("pop"))

print("But this does not for some reason:")
print(pop())
print("Never gets here due to access violation :(")
