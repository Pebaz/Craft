#ifndef CRAFT_COMMON
#define CRAFT_COMMON

#define PY_SSIZE_T_CLEAN
#include "Python.h"


/*struct Result
{
	bool found;
	PyObject * value;
}*/


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



/*
def craft_push_scope():
	"""
	"""
	global SCOPE, SYMBOL_TABLE
	SCOPE += 1
	SYMBOL_TABLE.append(dict())

	# UNDO(Pebaz):
	TRACEBACK.set_scope(SCOPE)


def craft_pop_scope():
	"""
	"""
	global SCOPE, SYMBOL_TABLE, TRACEBACK
	SCOPE -= 1
	SYMBOL_TABLE.pop()

	# UNDO(Pebaz):
	TRACEBACK.set_scope(SCOPE)

*/

#endif  // CRAFT_COMMON
