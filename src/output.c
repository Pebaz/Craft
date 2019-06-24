#include <stdio.h>
#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "jit/craft_common.c"


PyObject * craft_main(
    PyObject * ARGS,
    PyObject * SYMBOL_TABLE,
    PyObject * BRANCHES
)
{
	// Function return values (see header.j2 and footer.j2)
	PyObject * RET_result, * ERROR_TYPE, * ERROR, * traceback;

    // Stop Python from interpreting anything else while we use this thread
    PyGILState_STATE gstate = PyGILState_Ensure();

    // Define convenience variables for lookups/etc.
    PyObject * scope0 = PyList_GetItem(SYMBOL_TABLE, 0);
    PyObject * query = PyDict_GetItemString(scope0, "query-symbol-table");
    PyObject * program = PyDict_GetItemString(scope0, "Program");
    PyObject * eval = PyDict_GetItemString(scope0, "eval");
    PyObject * scope = PyDict_GetItemString(scope0, "get-scope");
    PyObject * get_result = PyDict_GetItemString(scope0, "get-result");
    
    // Exceptions
    PyObject * CraftException 				= PyDict_GetItemString(scope0, "CraftException");
    PyObject * CraftInternalException 		= PyDict_GetItemString(scope0, "CraftInternalException");
    PyObject * CraftFunctionReturnException = PyDict_GetItemString(scope0, "CraftFunctionReturnException");
    PyObject * CraftLoopBreakException 		= PyDict_GetItemString(scope0, "CraftLoopBreakException");
    PyObject * CraftLoopContinueException 	= PyDict_GetItemString(scope0, "CraftLoopContinueException");
// LOOKUP push-scope
    PyObject * ARGS_query0 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query0, 0, Py_BuildValue("s", "push-scope"));
    PyTuple_SET_ITEM(ARGS_query0, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var1 = PyObject_Call(query, ARGS_query0, NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var1_args2 = PyTuple_New(0);
    PyObject * var3 = PyObject_Call(var1, CALL_var1_args2, NULL);
    if (PyErr_Occurred()) goto craft_error;

// ARGUMENTS
    PyObject * ARGS_query_set = Py_BuildValue("(O, O)", Py_BuildValue("s", "set"), PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * set = PyObject_Call(query, ARGS_query_set, NULL);
    PyObject * ARGS_set = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_set, 0, Py_BuildValue("s", "n"));
    PyTuple_SET_ITEM(ARGS_set, 1, PyList_GetItem(ARGS, 0));
    PyObject_Call(set, ARGS_set, NULL);

// BODY

// {'set': ['a', 0]}
    PyObject * var4 = Py_BuildValue("s", "a");
    PyObject * var5 = Py_BuildValue("i", 0);
// LOOKUP set
    PyObject * ARGS_query6 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query6, 0, Py_BuildValue("s", "set"));
    PyTuple_SET_ITEM(ARGS_query6, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var7 = PyObject_Call(query, ARGS_query6, NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var7_args8 = PyTuple_New(2);
    PyTuple_SET_ITEM(CALL_var7_args8, 0, var4);
    PyTuple_SET_ITEM(CALL_var7_args8, 1, var5);
    PyObject * var9 = PyObject_Call(var7, CALL_var7_args8, NULL);
    if (PyErr_Occurred()) goto craft_error;

// {'set': ['b', 1]}
    PyObject * var10 = Py_BuildValue("s", "b");
    PyObject * var11 = Py_BuildValue("i", 1);
// LOOKUP set
    PyObject * ARGS_query12 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query12, 0, Py_BuildValue("s", "set"));
    PyTuple_SET_ITEM(ARGS_query12, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var13 = PyObject_Call(query, ARGS_query12, NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var13_args14 = PyTuple_New(2);
    PyTuple_SET_ITEM(CALL_var13_args14, 0, var10);
    PyTuple_SET_ITEM(CALL_var13_args14, 1, var11);
    PyObject * var15 = PyObject_Call(var13, CALL_var13_args14, NULL);
    if (PyErr_Occurred()) goto craft_error;

// {'for': [['i', '$n'], {'set': ['a', '$b']}, {'set': ['b', {'+': ['$a', '$b']}]}]}
// BRANCH[0]
    PyObject_Call(eval, Py_BuildValue("(O)", PyList_GetItem(BRANCHES, 0)), NULL);
        if (PyErr_Occurred()) goto craft_error;

// {'return': ['$a']}
    PyObject * ARGS_query17 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query17, 0, Py_BuildValue("s", "a"));
    PyTuple_SET_ITEM(ARGS_query17, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var18 = PyObject_Call(query, ARGS_query17, NULL);
    if (PyErr_Occurred()) goto craft_error;
// LOOKUP return
    PyObject * ARGS_query19 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query19, 0, Py_BuildValue("s", "return"));
    PyTuple_SET_ITEM(ARGS_query19, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var20 = PyObject_Call(query, ARGS_query19, NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var20_args21 = PyTuple_New(1);
    PyTuple_SET_ITEM(CALL_var20_args21, 0, var18);
    PyObject * var22 = PyObject_Call(var20, CALL_var20_args21, NULL);
    if (PyErr_Occurred()) goto craft_error;
// LOOKUP pop-scope
    PyObject * ARGS_query23 = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_query23, 0, Py_BuildValue("s", "pop-scope"));
    PyTuple_SET_ITEM(ARGS_query23, 1, PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * var24 = PyObject_Call(query, ARGS_query23, NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var24_args25 = PyTuple_New(0);
    PyObject * var26 = PyObject_Call(var24, CALL_var24_args25, NULL);
    if (PyErr_Occurred()) goto craft_error;

    // Return Result<None> if no return function is called
	RET_result = PyObject_Call(get_result, Py_BuildValue("(O, O)", Py_None, Py_None), NULL);
    PyGILState_Release(gstate);
    //return Py_None;
    return RET_result;





	// Error Label
	craft_error:
	//PyErr_Print();
	PyErr_Fetch(&ERROR_TYPE, &ERROR, &traceback);
	PyErr_Clear();

	PyObject * RETURN_VALUE = Py_None;
	PyObject * RETURN_ERROR = Py_None;

	// Check and see if it's a return/break/etc. exception or normal error
	if (PyErr_GivenExceptionMatches(ERROR_TYPE, CraftFunctionReturnException))
	{
		printf("    CraftFunctionReturnException\n");
		RETURN_VALUE = PyObject_GetAttrString(ERROR, "return_value");
	}
	
	// Real Exception. This makes sure an Exception object is returned.
	else
	{
		PyObject * py_dict = PyDict_New();
		PyObject * py_list = PyList_New(1);
		PyList_SetItem(py_list, 0, ERROR);
		PyDict_SetItemString(py_dict, "args", py_list);
		RETURN_ERROR = PyErr_NewException("builtins.Exception", NULL, py_dict);
	}

	RET_result = PyObject_Call(get_result, Py_BuildValue("(O, O)", RETURN_VALUE, RETURN_ERROR), NULL);

	PyGILState_Release(gstate);
	return RET_result;
}