#define PY_SSIZE_T_CLEAN
#include "Python.h"


/*PyObject * craft_main_old(PyObject *craft)
{
	PyGILState_STATE gstate = PyGILState_Ensure();

	int CALL_print_len_args = 1;
	PyObject * print = PyObject_GetAttrString(craft, "print");
	PyObject * CALL_print_args = PyTuple_New(CALL_print_len_args);
	PyTuple_SET_ITEM(CALL_print_args, 0, Py_BuildValue("s", "Hello World"));
	PyObject_Call(print, CALL_print_args, NULL);
	
	PyGILState_Release(gstate);
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

	PyGILState_Release(gstate);
	return Py_None;
}
