#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>

#define PY_NONE Py_BuildValue("")

PyObject * craft_main()
{
    printf("Here\n");
	return PY_NONE;
}


int main(int argc, char** argv) { }
