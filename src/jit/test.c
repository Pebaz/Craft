#define PY_SSIZE_T_CLEAN
#include "Python.h"


PyObject * query_symbol_table(PyObject * SYMBOLE_TABLE, PyObject * SCOPE, char * symbol)
{
	long scope = PyLong_AsLong(SCOPE);
	if (scope == -1) { return Py_False; }

	for (long i = scope; i > -1; i--)
	{
		PyObject * table = PyList_GetItem(SYMBOLE_TABLE, PyLong_FromLong(i));

		// If symbol in table, return table[symbol]
		if (PyDict_Contains(table, PyUnicode_FromString(symbol)))
		{
			return PyDict_GetItemString(table, symbol);
		}
	}

	return Py_False;
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


	PyObject * scope0 = PyList_GetItem(SYMBOL_TABLE, 0);
	PyObject * print = PyDict_GetItemString(scope0, "print");


	// Call Print
	int CALL_print_len_args = 1;
	PyObject * CALL_print_args = PyTuple_New(CALL_print_len_args);
	PyTuple_SET_ITEM(CALL_print_args, 0, Py_BuildValue("s", "Hello World"));
	PyObject_Call(print, CALL_print_args, NULL);

	query_symbol_table(SYMBOL_TABLE, SCOPE, "print");


	PyGILState_Release(gstate);
	return Py_None;
}
