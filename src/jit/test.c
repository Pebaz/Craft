#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>


#define PYO PyObject *


PyObject * query_symbol_table(PyObject * SYMBOL_TABLE, PyObject * SCOPE, char * symbol)
{
	PyGILState_STATE gstate = PyGILState_Ensure();
	long scope = PyLong_AsLong(SCOPE);
	if (scope == -1) { return Py_False; }

	for (long i = scope; i > -1; i--)
	{
		//printf("Scope index: %lu\n", scope);
		PyObject * table = PyList_GetItem(SYMBOL_TABLE, i);
		//printf("&table: 0x%lX\n", table);
		
		if (PyDict_Contains(table, Py_BuildValue("s", symbol)))
		{
			return PyDict_GetItemString(table, symbol);
		}
	}

	PyGILState_Release(gstate);
	char err_msg[128];
	snprintf(err_msg, sizeof(err_msg), "\"%s\" not found.", symbol);
	PyErr_SetString(PyExc_RuntimeError, err_msg);
	return Py_None;
}

PyObject * craft_main(
	PyObject * SYMBOL_TABLE,
	PyObject * SCOPE,
	PyObject * RETURN_POINTS,
	PyObject * EXCEPTIONS,
	PyObject * TRACEBACK,
	PyObject * CRAFT_PATH,
	PyObject * IS_DEBUG
)
{
	PyGILState_STATE gstate = PyGILState_Ensure();


	PYO scope0 = PyList_GetItem(SYMBOL_TABLE, 0);
	PYO print = PyDict_GetItemString(scope0, "print");


	// Call Print
	int CALL_print_len_args = 1;
	PYO CALL_print_args = PyTuple_New(CALL_print_len_args);
	PyTuple_SET_ITEM(CALL_print_args, 0, Py_BuildValue("s", "Hello World"));
	//PyTuple_SET_ITEM(CALL_print_args, 1, SYMBOL_TABLE);
	PyObject_Call(print, CALL_print_args, NULL);

	//Py_INCREF(SYMBOL_TABLE);
	PYO craft_print = query_symbol_table(SYMBOL_TABLE, SCOPE, "print");

	PYO CALL_craft_print_args = PyTuple_New(1);
	PyTuple_SET_ITEM(CALL_craft_print_args, 0, Py_BuildValue("s", "Used craft_print()"));
	PyObject_Call(craft_print, CALL_craft_print_args, NULL);

	PyGILState_Release(gstate);
	return Py_None;
}
