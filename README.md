# Wing Programming Language



## Performace

It will be necessary to port as much of the core language to Cython as possible
so that maximum performance is achieved. Some functionality may be written in C
for even more speed.







[Click here](https://learnxinyminutes.com/docs/yaml/) for a great YAML syntax tutorial.


Get Python spelling library to get suggestions for the console :D


NAMED SCOPE:
 - ACCESSED VIA: scope1.scope2.name: [arg1, arg2, arg3]
 - Each named scope is really a named dictionary in the scope in which it is
   defined.




### Minimum Viable Product

^1. Variables
^2. Scopes
^3. Function calls
^4. Defining Functions
^5. Importing (Including) other files
 6. For loops and While loops
 7. Standard library
 8. Operators


### Syntax

The syntax is thus:

An expression that contains a list of arguments (values) that can themselves be
expressions that evaluate to a value.


<function call>:
	- list
	- of
	- values
	- or
	- expressions (function calls)



Defining custom functions are just a list of statements that get re-evaluated
each time.


#### PLEASE NOTE:

The special character: '$' can be put at the start of a string to allow the
interpreter to evaluate that name as a string and not look it up in the symbol
table.


Wing Programming Language



 - Solidify data types
 	- list, hash, int, etc.
 	- Make custom types: wing_file, etc.
 	
 - How to open file
 - importing/including
 - Sublime text syntax highlighting





1.  Print
2.  Math operators: - / * + % **
3.  Bitwise operators: & | ^
4.  Equality: = is < > <= >= (<> | !=)
5.  Logical keywords: and or not
6.  def fn call
7.  Program comment
8.  if then else
9.  switch case default
10. import (imported and evaluated) | include (imported but not evaluated)
11. for (while | until) foreach
12. exit quit
13. globals
14. push-scope, pop-scope, create-named-scope
15. str, int, bool, float
16. Hash (create dictionary since YAML is not friendly)




Description:

Blah


Functional Requirements:

1. Run Software written in Wing
	WINGF1.1 Must be able to invoke the Wing interpreter via the command line.



Non-Functional Requirements:

1. Security
	WINGNF1.1 Access to the underlying interpreter infrastructure must be
		severely limited or completely denied.