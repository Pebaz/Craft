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
    PyObject * var0 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "push-scope"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var0_args1 = PyTuple_New(0);
    PyObject * var2 = PyObject_Call(var0, CALL_var0_args1, NULL);
    if (PyErr_Occurred()) goto craft_error;

// ARGUMENTS
    PyObject * ARGS_query_set = Py_BuildValue("(O, O)", Py_BuildValue("s", "set"), PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * set = PyObject_Call(query, ARGS_query_set, NULL);
    PyObject * ARGS_set = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_set, 0, Py_BuildValue("s", "person"));
    PyTuple_SET_ITEM(ARGS_set, 1, PyList_GetItem(ARGS, 0));
    PyObject_Call(set, ARGS_set, NULL);

// BODY

// {'print': ['$person']}
    PyObject * var4 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "person"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// LOOKUP print
    PyObject * var5 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "print"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var5_args6 = PyTuple_New(1);
    PyTuple_SET_ITEM(CALL_var5_args6, 0, var4);
    PyObject * var7 = PyObject_Call(var5, CALL_var5_args6, NULL);
    if (PyErr_Occurred()) goto craft_error;

// {'def': [['hi'], {'print': ['hi']}]}
// BRANCH[0]
    PyObject_Call(eval, Py_BuildValue("(O)", PyList_GetItem(BRANCHES, 0)), NULL);
    if (PyErr_Occurred()) goto craft_error;

// {'hi': []}
// LOOKUP hi
    PyObject * var8 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "hi"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var8_args9 = PyTuple_New(0);
    PyObject * var10 = PyObject_Call(var8, CALL_var8_args9, NULL);
    if (PyErr_Occurred()) goto craft_error;

// {'print': ['BackOut']}
    PyObject * var11 = Py_BuildValue("s", "BackOut");
// LOOKUP print
    PyObject * var12 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "print"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var12_args13 = PyTuple_New(1);
    PyTuple_SET_ITEM(CALL_var12_args13, 0, var11);
    PyObject * var14 = PyObject_Call(var12, CALL_var12_args13, NULL);
    if (PyErr_Occurred()) goto craft_error;
// LOOKUP pop-scope
    PyObject * var15 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "pop-scope"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// CALL
    PyObject * CALL_var15_args16 = PyTuple_New(0);
    PyObject * var17 = PyObject_Call(var15, CALL_var15_args16, NULL);
    if (PyErr_Occurred()) goto craft_error;

    // Return Result<None> if no return function is called
	RET_result = PyObject_Call(get_result, Py_BuildValue("(O, O)", Py_None, Py_None), NULL);
    PyGILState_Release(gstate);
    //return Py_None;
    return RET_result;
	
	// ------------------------------------------------------------------------
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
		//printf("    CraftFunctionReturnException\n");
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