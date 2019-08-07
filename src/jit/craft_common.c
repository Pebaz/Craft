/*
This file is no longer concretely useful.
However, during development, when serious segfaults and access violations were
common as I learned the Python C API, I could simply #include "craft_common.c"
and the build would work. Absolutely no idea why this would happen. After a
while, the opposite would work: commenting out the include. Since I am not a C
programming adept, this was quite frustrating and also a windfall since errors
could take hours to debug while working on Craft JIT Compilation.

So I'm keeping it!
*/

#ifndef CRAFT_COMMON
#define CRAFT_COMMON

#define PY_SSIZE_T_CLEAN
#include "Python.h"


PyObject * query_symbol_table(PyObject * SYMBOL_TABLE, PyObject * SCOPE, char * symbol)
{
	PyGILState_STATE gstate = PyGILState_Ensure();
	long scope = PyLong_AsLong(SCOPE);
	if (scope == -1) { return Py_False; }

			//PyObject * scope0 = PyList_GetItem(SYMBOL_TABLE, 0);
			//PyObject * print = PyDict_GetItemString(scope0, "print");

	for (long i = scope; i > -1; i--)
	{
		PyObject * table = PyList_GetItem(SYMBOL_TABLE, i);
		Py_INCREF(table);

			// {'print': [False]}		
			//PyObject * CALL_var16_args17 = PyTuple_New(1);
			//PyTuple_SET_ITEM(CALL_var16_args17, 0, table);
			//PyObject_Call(print, CALL_var16_args17, NULL);
		
		if (PyDict_Contains(table, Py_BuildValue("s", symbol)))
		{
			Py_INCREF(table);
			return PyDict_GetItemString(table, symbol);
		}
	}

	PyGILState_Release(gstate);
	char err_msg[128];
	snprintf(err_msg, sizeof(err_msg), "\"%s\" not found.", symbol);
	printf("%s\n", err_msg);
	//PyErr_SetString(PyExc_NameError, err_msg);
	return Py_None;
}

#endif  // CRAFT_COMMON
