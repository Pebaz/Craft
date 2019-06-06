
#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>
#include "jit/craft_common.c"


#define PYO PyObject *


/*PyObject * query_symbol_table(PyObject * SYMBOL_TABLE, PyObject * SCOPE, char * symbol)
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
}*/


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





/*
#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>
#include "jit/craft_common.c"

PyObject * craft_main(
    //PyObject * ARGS,
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
    PyObject * scope0 = PyList_GetItem(SYMBOL_TABLE, 0);
    PyObject * craft_get = PyDict_GetItemString(scope0, "get");

    // {'print': ['Hello World!', '1', '2']}
    PyObject * var0 = Py_BuildValue("s", "2");
    PyObject * var1 = Py_BuildValue("s", "1");
    PyObject * var2 = Py_BuildValue("s", "Hello World!");
    PyObject * var3 = query_symbol_table(SYMBOL_TABLE, SCOPE, "print");
    PyObject * CALL_var3_args4 = PyTuple_New(3);
    PyTuple_SET_ITEM(CALL_var3_args4, 2, var0);
    PyTuple_SET_ITEM(CALL_var3_args4, 1, var1);
    PyTuple_SET_ITEM(CALL_var3_args4, 0, var2);
    PyObject_Call(var3, CALL_var3_args4, NULL);

    PyGILState_Release(gstate);
    return Py_None;
}

*/
