#ifndef CRAFT_COMMON
#define CRAFT_COMMON

#define PY_SSIZE_T_CLEAN
#include "Python.h"

PyObject * query_symbol_table(PyObject * SYMBOL_TABLE, PyObject * SCOPE, char * symbol)
{
	PyGILState_STATE gstate = PyGILState_Ensure();
	long scope = PyLong_AsLong(SCOPE);
	if (scope == -1) { return Py_False; }

	for (long i = scope; i > -1; i--)
	{
		PyObject * table = PyList_GetItem(SYMBOL_TABLE, i);
		
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
