import time, ctypes, sys
import pytcc as pcc

program = b"""
#define PY_SSIZE_T_CLEAN
#include "Python.h"

PyObject * pop(PyObject * self, PyObject * args, PyObject * kwargs) {
	int a = 3;
	return PyLong_FromLong(25);

	// WORKS
	//return NULL;

	//return Py_RETURN_TRUE;
}

PyObject * bubbles(PyObject * self, PyObject * args, PyObject * kwargs) {
	//return Py_BuildValue("i", 65535);
	PyObject * list = PyList_New(0);
	PyList_Append(list, PyLong_FromLong(25));
	return list;
}


int foobar(int n) {
	int i = 0;
	for (int r = 0; r < n; r++)
	{
		i += r;
	}
    return i;
}

// Needed to appease TCC:
int main() { }
"""


def jit_compile(source):
    pass


jit_code = pcc.TCCState()
jit_code.add_include_path("C:/Python37/include")
jit_code.add_library_path("C:/Python37")
jit_code.add_library("python37")
# jit_code.set_options('-m64')
jit_code.compile_string(program)
jit_code.relocate()


rettype = ctypes.c_int
foobar_proto = ctypes.CFUNCTYPE(rettype, ctypes.c_int)
foobar = foobar_proto(jit_code.get_symbol("foobar"))

# bubbles_proto = ctypes.CFUNCTYPE(ctypes.py_object)
# bubbles = bubbles_proto(jit_code.get_symbol('bubbles'))
# print(bubbles())


pop_proto = ctypes.CFUNCTYPE(ctypes.py_object)
pop = pop_proto(jit_code.get_symbol("pop"))

print("Try Call...")
print(pop(133))
print("DONE")
# sys.exit(0)


def py_foobar(n):
    i = 0
    for r in range(n):
        i += r
    return i


times = 3000

start = time.time_ns()
for i in range(times):
    py_foobar(times)
print(py_foobar(times))
py_end = (time.time_ns() - start) / 1000000000
print(f"Took {py_end}s to complete.")

start = time.time_ns()
for i in range(times):
    foobar(times)
print(foobar(times))
c_end = (time.time_ns() - start) / 1000000000
print(f"Took {c_end}s to complete.")

print(f"The C version is around {int(py_end / c_end)} times faster.")
