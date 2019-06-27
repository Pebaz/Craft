#include <stdio.h>#define PY_SSIZE_T_CLEAN
#include "Python.h"
//#include "jit/craft_common.c"


PyObject * craft_main_2da57718990a11e98ee63c18a040d0f4(
    PyObject * ARGS,
    PyObject * SYMBOL_TABLE,
    PyObject * BRANCHES
)
{
    // Stop Python from interpreting anything else while we use this thread
    PyGILState_STATE gstate = PyGILState_Ensure();

	// Function return values (see header.j2 and footer.j2)
	PyObject * RET_result, * ERROR_TYPE, * ERROR, * traceback;

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
    PyObject * CraftLoopContinueException 	= PyDict_GetItemString(scope0, "CraftLoopContinueException");// LOOKUP push-scope    PyObject * var0 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "push-scope"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var0_args1 = PyTuple_New(0);
    PyObject * var2 = PyObject_Call(var0, CALL_var0_args1, NULL);
    if (PyErr_Occurred()) goto craft_error;// ARGUMENTS
    PyObject * ARGS_query_set = Py_BuildValue("(O, O)", Py_BuildValue("s", "set"), PyObject_Call(scope, PyTuple_New(0), NULL));
    PyObject * set = PyObject_Call(query, ARGS_query_set, NULL);
    PyObject * ARGS_set = PyTuple_New(2);
    PyTuple_SET_ITEM(ARGS_set, 0, Py_BuildValue("s", "n"));
    PyTuple_SET_ITEM(ARGS_set, 1, PyList_GetItem(ARGS, 0));
    PyObject_Call(set, ARGS_set, NULL);
// BODY
// {'print': [{'format': ['In fibo({})', '$n']}]}    PyObject * var4 = Py_BuildValue("s", "In fibo({})");    PyObject * var6 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "n"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// LOOKUP format    PyObject * var7 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "format"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var7_args8 = PyTuple_New(2);
    PyTuple_SET_ITEM(CALL_var7_args8, 0, var4);
    PyTuple_SET_ITEM(CALL_var7_args8, 1, var6);
    PyObject * var9 = PyObject_Call(var7, CALL_var7_args8, NULL);
    if (PyErr_Occurred()) goto craft_error;// LOOKUP print    PyObject * var10 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "print"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var10_args11 = PyTuple_New(1);
    PyTuple_SET_ITEM(CALL_var10_args11, 0, var9);
    PyObject * var12 = PyObject_Call(var10, CALL_var10_args11, NULL);
    if (PyErr_Occurred()) goto craft_error;
// {'set': ['a', 0]}    PyObject * var13 = Py_BuildValue("s", "a");    PyObject * var14 = Py_BuildValue("i", 0);// LOOKUP set    PyObject * var15 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "set"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var15_args16 = PyTuple_New(2);
    PyTuple_SET_ITEM(CALL_var15_args16, 0, var13);
    PyTuple_SET_ITEM(CALL_var15_args16, 1, var14);
    PyObject * var17 = PyObject_Call(var15, CALL_var15_args16, NULL);
    if (PyErr_Occurred()) goto craft_error;
// {'set': ['b', 1]}    PyObject * var18 = Py_BuildValue("s", "b");    PyObject * var19 = Py_BuildValue("i", 1);// LOOKUP set    PyObject * var20 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "set"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var20_args21 = PyTuple_New(2);
    PyTuple_SET_ITEM(CALL_var20_args21, 0, var18);
    PyTuple_SET_ITEM(CALL_var20_args21, 1, var19);
    PyObject * var22 = PyObject_Call(var20, CALL_var20_args21, NULL);
    if (PyErr_Occurred()) goto craft_error;
// {'for': [['i', '$n'], {'set': ['tmp', '$b']}, {'set': ['b', {'+': ['$a', '$b']}]}, {'set': ['a', '$tmp']}]}// BRANCH[0]
    PyObject_Call(eval, Py_BuildValue("(O)", PyList_GetItem(BRANCHES, 0)), NULL);
    if (PyErr_Occurred()) goto craft_error;
// {'return': ['$a']}    PyObject * var24 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "a"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// LOOKUP return    PyObject * var25 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "return"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var25_args26 = PyTuple_New(1);
    PyTuple_SET_ITEM(CALL_var25_args26, 0, var24);
    PyObject * var27 = PyObject_Call(var25, CALL_var25_args26, NULL);
    if (PyErr_Occurred()) goto craft_error;// LOOKUP pop-scope    PyObject * var28 = PyObject_Call(query, Py_BuildValue("(O, O)", Py_BuildValue("s", "pop-scope"), PyObject_Call(scope, PyTuple_New(0), NULL)), NULL);
    if (PyErr_Occurred()) goto craft_error;// CALL
    PyObject * CALL_var28_args29 = PyTuple_New(0);
    PyObject * var30 = PyObject_Call(var28, CALL_var28_args29, NULL);
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