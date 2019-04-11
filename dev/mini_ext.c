//#define PY_SSIZE_T_CLEAN
#include <stdio.h>
#include "Python.h"

PyObject * pop()
{
	printf("Here\n");
    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();
    PyObject* obj = PyLong_FromLong(10);
    PyGILState_Release(gstate);
    return obj;
}

int foobar()
{
	printf("Here\n");
	return 3;
}
