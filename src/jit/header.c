#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "jit/craft_common.c"


PyObject * craft_main(
    PyObject * ARGS,
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
	PyObject * query = PyDict_GetItemString(scope0, "query-symbol-table");
	PyObject * scope = PyDict_GetItemString(scope0, "get-scope");
    
