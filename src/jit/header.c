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
    // Stop Python from interpreting anything else while we use this thread
    PyGILState_STATE gstate = PyGILState_Ensure();

    // Define convenience variables for lookups/etc.
    PyObject * scope0 = PyList_GetItem(SYMBOL_TABLE, 0);
    PyObject * query = PyDict_GetItemString(scope0, "query-symbol-table");
    PyObject * scope = PyDict_GetItemString(scope0, "get-scope");
    