import ctypes, pytcc

program = b"""
#include "Python.h"

/* Cannot return 3 due to access violation */
PyObject * pop(PyObject * self, PyObject * args, PyObject * kwargs) {
    // Cannot return *any* Python object
    return PyLong_FromLong(3);
}

int foobar() { return 3; }  // Returns 3 just fine

// Needed to appease TCC:
int main() { }
"""

jit_code = pytcc.TCCState()
jit_code.add_include_path('C:/Python37/include')
jit_code.add_library_path('C:/Python37')
jit_code.add_library('python37')
jit_code.compile_string(program)
jit_code.relocate()

foobar_proto = ctypes.CFUNCTYPE(ctypes.c_int)
foobar = foobar_proto(jit_code.get_symbol('foobar'))

print(f'It works: {foobar()}')

pop_proto = ctypes.PYFUNCTYPE(ctypes.py_object)
pop = pop_proto(jit_code.get_symbol('pop'))

print('But this does not for some reason:')
print(pop())
print('Never gets here due to access violation :(')