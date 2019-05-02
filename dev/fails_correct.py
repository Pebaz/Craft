"""
Using library: https://github.com/frxstrem/pytcc
"""

import ctypes, pytcc

import sys
from pathlib import Path

# name = str(Path(sys.executable).parent / f'python{sys.version_info.major}{sys.version_info.minor}.dll')
# python_dll = ctypes.PyDLL(name)


program = b"""
#define PY_SSIZE_T_CLEAN
#include <stdlib.h>
#include "Python.h"

PyObject * pop()
{
	Py_Initialize();
    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();
    PyObject* obj = PyLong_FromLong(10);
    PyGILState_Release(gstate);
    return obj;
}

struct car
{
	int num_wheels;
};

struct car * do_this()
{
	sleep(3);
	struct car * Car = malloc(sizeof(struct car));
	Car->num_wheels = 4;
	return Car;
	//return NULL;
}

int foobar() { return 3; }

// Needed to appease TCC:
//int main() { }
"""

# Compile the small Python extension
jit_code = pytcc.TCCState()
jit_code.add_include_path("C:/Python37/include")
jit_code.add_library_path("C:/Python37")
jit_code.add_library("python37")
jit_code.set_options("-shared")
jit_code.compile_string(program)
jit_code.relocate()
# b = jit_code.get_bytes()
# print(b)

do_this_proto = ctypes.CFUNCTYPE(ctypes.c_voidp)
do_this = do_this_proto(jit_code.get_symbol("do_this"))
print(dir(do_this))
a = do_this()
print(a)

sys.exit()


foobar_proto = ctypes.CFUNCTYPE(ctypes.c_int)
foobar = foobar_proto(jit_code.get_symbol("foobar"))

print(f"It works: {foobar()}")

# PyObject * pop()
pop_proto = ctypes.PYFUNCTYPE(ctypes.py_object)
pop = pop_proto(jit_code.get_symbol("pop"))

print("But this does not for some reason:")
print(pop())
print("Never gets here due to access violation :(")
