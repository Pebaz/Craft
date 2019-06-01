#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>

#define PY_NONE Py_BuildValue("")

static void print_str(PyObject *o)
{
    PyObject_Print(o, stdout, Py_PRINT_RAW);
}

static void print_repr(PyObject *o)
{
    PyObject_Print(o, stdout, 0);
}

PyObject * craft_main()
{
    printf("Zero.\n");
    //PyGILState_STATE gstate;
    //gstate = PyGILState_Ensure();

    PyObject * name = Py_BuildValue("s", "Pebaz");
    Py_INCREF(name);
    pyprint(name);
    printf("-> %i\n", square(20));
    printf("One.\n");
    //Py_DECREF(name);

    PyObject * None = PY_NONE;
    //PyGILState_Release(gstate);
	return None;
}


int main(int argc, char** argv) { }
