import ctypes
from pytcc import TCC

comp = TCC()
comp.preprocessor_symbols["DEBUG"] = "1"
comp.add_include_path('C:/Python37/include')
comp.add_library_path('./')
comp.add_library_path('C:/Python37')
comp.add_library('python37')
comp.add_file("test.c")
comp.compile_string('''
#define PY_SSIZE_T_CLEAN
#include "Python.h"

PyObject * pop(PyObject * self, PyObject * args, PyObject * kwargs) {
	// Cannot return *any* Python object
	return PyLong_FromLong(3);
}

int main(int argc, char **argv)
{
	printf("%s %d\n", argv[0], sum(2, 2));
	return 0;
}
''')

comp.relocate()

pop_proto = ctypes.CFUNCTYPE(ctypes.py_object)
pop = pop_proto(comp.get_symbol('pop'))
print(pop())

#comp.run(["test"])

print(dir(comp))
