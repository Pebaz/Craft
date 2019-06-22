# Craft JIT Compilation

 * Convert arbitrary Craft code (function) to C and JIT compile.
 * Any Craft data type will be able to be JITted.
 * Could use j2do as a library to have each Craft builtin have a `__jit__`
   variable that contains templated C code. (e.g.):
	```c
	// Convert Python Integer
	Py_BuildValue("L", {{ num }})

	// <= Function
	PyObject_RichCompareBool({{ o1 }}, {{ o2 }}, Py_LE)

	// If statement

	if ({{ obj }} == Py_True) {
	{{ render(statements) }}
	}
	```
   This could be easily used like so:
	```python
	statements = [...]
	render(jit(4))
	```


## Docs

 * https://docs.python.org/3/c-api/object.html#c.PyObject_CallObject
 * https://docs.python.org/3/c-api/arg.html#c.Py_BuildValue
