// Py_BuildValue
// https://docs.python.org/2.0/ext/buildValue.html
// https://docs.python.org/3/c-api/arg.html#c.Py_BuildValue


#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>

#define PY_NONE Py_BuildValue("")

static void print_str(PyObject *o)
{
    PyObject_Print(o, stdout, Py_PRINT_RAW);
}

static void print_repr(PyObject *o)
{
    PyObject_Print(o, stdout, 0);
}


/*
What implications does this test signify?

 1. Python can pass Python objects to C.
 2. C can call Python callables.
 3. C can access Python object attributes.
 4. C can obtain values returned from Python callable.
 5. Python can obtain values return from C functions.
*/
PyObject * craft_main(PyObject *craft, PyObject *print)
{
	printf("Negative One.\n");
	PyGILState_STATE gstate = PyGILState_Ensure();
	PyObject * s1 = PyObject_Call(print, Py_BuildValue("(s)", "THIS IS LONG!"), NULL);
	PyObject * s2 = PyObject_Call(print, Py_BuildValue("(s)", "THIS IS LONG2"), NULL);

	PyObject * craft_name = PyObject_GetAttrString(craft, "name");
	PyObject * asdf = PyObject_GetAttrString(craft, "asdf");
	PyObject * s3 = PyObject_Call(asdf, PyTuple_New(0), NULL);


	PyObject *the_tuple = PyTuple_New(4);
	PyTuple_SET_ITEM(the_tuple, 0, craft_name);
	PyTuple_SET_ITEM(the_tuple, 1, s1);
	PyTuple_SET_ITEM(the_tuple, 2, s2);
	PyTuple_SET_ITEM(the_tuple, 3, s3);
	PyObject_Call(print, the_tuple, NULL);
	PyGILState_Release(gstate);

    printf("Zero.\n");
    PyObject * name = Py_BuildValue("s", "Pebaz");
	
    printf("-> %i\n", square(20));
	return the_tuple;
}


int main(int argc, char** argv) { }
