# 🎻 Craft Programming Language

Craft is an interpreted, high-level scripting language.

# Features

* 100% equivalent Craft or YAML syntax
* REPL
* Import Craft/YAML/Python modules
* JIT-Compile user-defined functions to C asynchronously at runtime
* Try/Catch/Finally
* Switch/Case/Default
* For/While/Until
* And/Or/Not
* If/Unless/Then/Else
* Lambdas
* Structs
* Quoting
* String formatting
* 100% equivalent Python data types
* Python math operators

# Getting Started

### Command Line

```bash
# Launch REPL
python src/craft.py

# Run .craft script
python src/craft.py hello.craft

# Run .yaml script
python src/craft.py -y hello.yaml

# Time the execution of script
python src/craft.py -t hello.craft

# Get Craft interpreter version
python src/craft.py -v
```

### Hello World Craft Syntax

```
:: hello.craft
Program:
[
    set: [name Pebaz]  :: Single-word strings don't need to be quoted
    print: [$name]     :: Lookup variables using: `$` character

    :: For loop
    for: [
        [i 10]
        print: [$i]
    ]
]
```

### Hello World YAML Syntax

```yaml
# hello.yaml
Program:
  - set: [name, Pebaz]
  - print: [$name]

  - for:
    - [i, 10]
    - print: [$i]
```

More examples can be found in the `examples` directory.  In addition, look at the `src/test` directory for unit tests that test all the language features if you get stuck.

## Craft Roadmap

##### Milestone 1

 * Basic keywords

 * Operators

 * Standard Library Foundation

 * Functions, Lambdas

 * Data Type Interop with Python

 * Importing Craft/YAML/Python modules

 * Craft/YAML REPL

 * Create documentation page that looks like [this](https://common-lisp.net/project/parenscript/reference.html)

##### Milestone 2

 * More Comprehensive Stdlib

 * Files, Threads, Sockets, Input, Random

 * Tighter Core (all keywords in stdlib rather than core)

 * Package Manager (using Git as storage medium)

 * Python Modules can Import Python Modules

 * REPL auto-completion

 * VS Code Syntax Highliting

 * Notepad++ Syntax Highlighting

 * Atom Syntax Highlighting

# About

I originally created the Craft Programming Language on a whim.  I was sitting at the office one day and thought, "I wonder how hard it would be to write an interpreter for a given YAML syntax in Python."  I had been itching to use a popular Python [YAML parsing library](https://github.com/yaml/pyyaml) and had just found my reason.

I went through several different possible designs for interpreting the YAML syntax.  I finally found a structure that, when parsed, produced the following Python dictionary:

```python
{ 'function-name' : [argument1, 'argument2', 3, 4.0] }
```

What was very interesting to me, however, was how similar it was to how Lisp S-Expressions work: you can nest them:

```lisp
(function-name
 	argument1
 	(other-function-as-argument 123)
 	"some value"
 	(another-func))
```

This was instantly fun.  I found a way to structure how a YAML file was laid out so that when parsed, I would be left with the following Python dictionary:

```python
{
    'Program' : [
        { 'print' : ['Hello World'] }
    ]
}
```

I knew then that this was how I was going to structure the interpreter.  It would take the key of the first key-value pair in the dictionary and execute the function in the global namespace that matched that function name.  The value of the first key-value pair would always be a list that contained the arguments for the given function.

What can be done with this structure is nest them very far and instantly provide a logical and very easily understandable execution model.

In addition, my choice of using the YAML library was very fortunate because like the Python standard library's [JSON parsing module](https://docs.python.org/3.7/library/json.html), the YAML library automatically created a dictionary object with the proper data types already mapped to native Python equivalents.  Arrays would become lists and JavaScript objects would become dictionaries.

All I had to do then, was create a working symbol table.

I chose to use a regular Python list that contained a bunch of dictionaries that represented each scope currently mapped in a program.  Each function that required a new disposable scope could append a dictionary to the end of that list and then names could be mapped to values within it.

What this allowed me to do is very easily create a lookup function that looked at the current scope index and work its way upward until it either found the corresponding name or raised an error because the name did not exist.

This was the skeleton of the entire language.  Every single other function in the language was based off of the concepts detailed here.

### REPL

The read-eval-print-loop (REPL) was very fun to make because it was so very simple.  I simply created a while loop that contained a call to the `input()`  function.  The output was then piped to the YAML parser and then executed by the interpreter.  This can be illustrated in the following code example:

```python
while True:
    code = input('>>> ')
    interpret(code)
```

### Craft Syntax Parser

After creating a lot of different language features, I started feeling like the project would be better served having it's own syntax since I was already referring to it by its own name: Craft.

I built the entire parser in just a few lines of code using the [PyParsing](https://github.com/pyparsing) library.  This library is by far the best parsing library for Python in my opinion, but it did require an enormous amount of study in order to get it to work great.  In the end, I had a parser that did the equivalent of the YAML parser, but for the new Craft syntax.

### JIT Compilation

This was by far the most difficult undertaking during the course of Craft's development.  I had found [Python bindings to LibTCC](https://github.com/thgcode/pytcc) which is the accompanying library for [Tiny C Compiler](<https://bellard.org/tcc/>).  Immediately, I knew that I wanted to attempt to transpile Craft source code to C and then compile that C at runtime to increase performance.

I set out to make a proof of concept.  After many hours of tinkering, I was finally able to JIT compile a string of C source code that included the `Python.h` header to make use of Python types and functions within the JITted code.

Once I had a working example that I could consult, I began working on a JIT compiler for Craft that would:

1. Accept Craft AST
2. Transpile it at runtime to C source code containing Python API calls
3. Compile it at runtime
4. Copy the memory containing the executable code to a Python object
5. Bundle the C code buffer with a Python callable to produce a "function" that could be called from Python
6. Asynchronously JIT compile any user defined function in the background seamlessly

I accomplished all of those goals.  User defined functions seamlessly without interruption get compiled to C and then compiled using LibTCC which then get called when they are finished compiling.




