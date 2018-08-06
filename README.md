# Wing Programming Language


[Click here](https://learnxinyminutes.com/docs/yaml/) for a great YAML syntax tutorial.




### Minimum Viable Product

 1. Variables
 2. Scopes
 3. Function calls
 4. Defining Functions
 5. Importing (Including) other files
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





	for i in getvalue(dictn):
		if isinstance(i, dict):
			handle_expression(i)
		else:
			handle_value(i) # Looks up names and whatnot








def handle_function(line, ast, keys):
	print(ast)
	#print(line)
	operation = getkey(line)

	if operation == 'set':

		value = getvalue(line)

		# Expressions are dictionaries
		if isinstance(value, dict):
			result = handle_op(getvalue(line))
			print(result)

		# Should
		elif isinstance(value, list):
			if len(value) == 2:
				name = value[0]

				# For right now, we are assuming that there is no expression
				# (dict) here:
				set_to_value = value[1]

				ast = [{ name : set_to_value }] + ast # <-------------- doesn't change it because ast is local copy