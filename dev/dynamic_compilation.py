import ctypes, sys
import pytcc as pcc


program =b"""

int foobar(int n) {
    return n * 2;
}

// Main is needed for compilation but is unnecessary since it won't be used.
int main(int argc, char** argv)
{
	return foobar(23);
}
"""

a = pcc.TCCState()
a.compile_string(program)
a.relocate()
#a.run()
#sys.exit(0)

rettype = ctypes.c_int
foobar_proto = ctypes.CFUNCTYPE(rettype, ctypes.c_int)
foobar = foobar_proto(a.get_symbol('foobar'))


def py_foobar(n):
	return n * 2

import time

start = time.time_ns()
print(foobar(123))
print(f'Took {time.time_ns() - start} to complete.')

start = time.time_ns()
print(py_foobar(123))
print(f'Took {time.time_ns() - start} to complete.')
