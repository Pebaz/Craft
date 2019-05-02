#define PY_SSIZE_T_CLEAN
#include "Python.h"

PyObject * pop(PyObject * self, PyObject * args, PyObject * kwargs) {
	int a = 3;
	return PyLong_FromUnsignedLong(25);
}

PyObject * bubbles(PyObject * self, PyObject * args, PyObject * kwargs) {
	//return Py_BuildValue("i", 65535);
	PyObject * list = PyList_New(0);
	PyList_Append(list, PyLong_FromUnsignedLong(25));
	return list;
}


PyMethodDef module_methods[] = {
	{ "pop", (PyCFunction)pop, METH_VARARGS | METH_KEYWORDS, 0 },
	{ "bubbles", (PyCFunction)bubbles, METH_VARARGS | METH_KEYWORDS, 0 },
	{ 0 },
};

PyModuleDef module_def = { PyModuleDef_HEAD_INIT, "craft_jit", 0, -1, module_methods, 0, 0, 0, 0 };

PyObject * PyInit_craft_jit() {
	PyObject * module = PyModule_Create(&module_def);
	return module;
}


int foobar(int n) {
    return n * 2;
}

// Needed to appease TCC:
int main() { }
