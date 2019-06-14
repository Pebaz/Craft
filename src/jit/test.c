
// #define PY_SSIZE_T_CLEAN
// #include "Python.h"
// #include <stdio.h>
// #include "jit/craft_common.c"


// #define PYO PyObject *


#include <stdio.h>
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
// LOOKUP push-scope
    PyObject * ARGS_query0 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query0, 0, Py_BuildValue("s", "push-scope"));
    PyTuple_SET_ITEM(ARGS_query0, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var1 = PyObject_Call(query, ARGS_query0, NULL);
// CALL
    PyObject * CALL_var1_args2 = PyTuple_New(0);
    PyObject * var3 = PyObject_Call(var1, CALL_var1_args2, NULL);

// ARGUMENTS
    PyObject * set = query_symbol_table(SYMBOL_TABLE, SCOPE, "set");
    PyObject * ARGS_set = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_set, 0, Py_BuildValue("s", "person"));
    PyTuple_SET_ITEM(ARGS_set, 1, PyList_GetItem(ARGS, 0));
    PyObject_Call(set, ARGS_set, NULL);

// BODY

// {'print': ['hi']}
    PyObject * var4 = Py_BuildValue("s", "hi");
// LOOKUP print
    PyObject * ARGS_query5 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query5, 0, Py_BuildValue("s", "print"));
    PyTuple_SET_ITEM(ARGS_query5, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var6 = PyObject_Call(query, ARGS_query5, NULL);
// CALL
    PyObject * CALL_var6_args7 = PyTuple_New(1);
    PyTuple_SET_ITEM(CALL_var6_args7, 0, var4);
    PyObject * var8 = PyObject_Call(var6, CALL_var6_args7, NULL);



    PyGILState_Release(gstate);
    //return Py_None;
    return NULL;
}


/*

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

*/



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
