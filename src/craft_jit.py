import ctypes, pathlib, itertools, traceback, time
from pytcc import TCC
from j2do               import j2do
from craft_core 		import *
from craft_parser 		import *
from craft_exceptions 	import *
from craft_cli 			import *
from craft_interpreter 	import *

setup_sym_tab()


class Function:
	def __init__(self, func: dict, branches: list):
		self.func = func
		self.branches = branches

	def __call__(self, *args):
		global SYMBOL_TABLE
		try:
			ret = self.func(
				list(args),
				SYMBOL_TABLE,
				self.branches  # Access violation writing this value
			)

			if not ret.err:
				return ret.value
			else:
				register_pyexception(ret.err)
				craft_raise(type(ret.err).__name__)

		except SystemError as e:
			traceback.print_exc()


class JIT:
	PATH_PREFIX = pathlib.Path() / 'jit'

	def __init__(self):
		self.source = []
		self.branches = []
		self.branch_functions = [
			'if', 'then',
			'try', 'catch', 'finally',
			'for',
		]
	
	def get_source(self):
		return '\n'.join(self.source)

	def __load_template(self, filename):
		with open(str(JIT.PATH_PREFIX / filename)) as file:
			return file.read()

	def emit(self, text=''):
		#print(text)
		self.source.append(text)

	def emit_lookup(self, name, counter):
		lookup = f'var{next(counter)}'
		self.emit_template('lookup.j2', dict(lookup=lookup, name=name))
		self.emit_template('error_check.j2', {})
		return lookup

	def emit_args(self, arguments, counter):
		bound_arg_names = []
		for argument in arguments:
			aname = f'var{next(counter)}'

			# Name lookup
			if isinstance(argument, str) and argument.startswith('$'):
				#lookup = argument[1:]

				# Second lookup
				if argument.startswith('$$'):
					self.emit(f'    PyObject * {aname} = Py_BuildValue("s", "{argument[1:]}");')
				else:
					bound_arg_names.append(self.emit_lookup(argument[1:], counter))
					continue

			# Boolean Literal
			elif isinstance(argument, bool):
				self.emit(f'    PyObject * {aname} = {"Py_True" if argument else "Py_False"};')

			# String Literal
			elif isinstance(argument, str):
				self.emit(f'    PyObject * {aname} = Py_BuildValue("s", "{argument}");')

			# Integer Literal
			elif isinstance(argument, int):
				self.emit(f'    PyObject * {aname} = Py_BuildValue("i", {argument});')

			# Float Literal
			elif isinstance(argument, float):
				self.emit(f'    PyObject * {aname} = Py_BuildValue("f", {argument});')

			# List literal
			elif isinstance(argument, list):
				list_arg_names = self.emit_args(argument, counter)
				self.emit_template('list.j2', dict(
					aname = aname,
					argument = argument,
					list_arg_names = list_arg_names
				))

			# Function call
			elif isinstance(argument, dict):

				if getkey(argument) not in self.branch_functions:
					bound_arg_names.append(self.emit_func(argument, counter))
					continue
				else:
					self.emit_template('branch.j2', {'index' : len(self.branches)})
					self.branches.append(argument)

				#bound_arg_names.append(self.emit_func(argument, counter))
				#continue

			bound_arg_names.append(aname)

		return bound_arg_names

	def emit_func(self, statement, counter):
		func_name = getkey(statement)
		arguments = getvalue(statement)
		bound_arg_names = self.emit_args(arguments, counter)

		self.emit(f'// LOOKUP {func_name}')
		func_var = self.emit_lookup(func_name, counter)
		func_var_args = f'CALL_{func_var}_args{next(counter)}'
		ret_name = f'var{next(counter)}'

		data = dict(
			func_var = func_var,
			func_name = func_name,
			arguments = arguments,
			bound_arg_names = bound_arg_names,
			func_var_args = func_var_args,
			ret_name = ret_name
		)
		self.emit_template('call.j2', data)
		self.emit_template('error_check.j2', {})
		return ret_name

	def emit_template(self, template, data):
		self.emit(j2do(template, data, include=[JIT.PATH_PREFIX]))	

	def transpile(self, ast):
		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		counter = itertools.count()

		print(':: Transpiling            ::')
		print(ast, '\n\n')
		print('=-' * 20)

		self.emit('#include <stdio.h>')
		self.emit_template('header.j2', {})

		# Push Scope
		self.emit_func({'push-scope' : []}, counter)

		self.emit('')

		# Now Bind all arguments to current (function) scope
		self.emit(j2do(
			"arguments.j2",
			dict(arg_names=arg_names),
			include=[JIT.PATH_PREFIX]
		))

		self.emit('\n// BODY')

		# Function body
		is_statement = lambda x: isinstance(x, dict) and len(x) == 1
		for statement in body:
			if is_statement(statement):
				self.emit(f'\n// {statement}')
			else:
				raise CraftException('SyntaxError', {}, {})

			# Make sure to interpret branching code
			if getkey(statement) not in self.branch_functions:
				self.emit_func(statement, counter)
			else:
				self.emit_template('branch.j2', {'index' : len(self.branches)})
				self.branches.append(statement)

		# Pop Scope
		self.emit_func({'pop-scope' : []}, counter)
		self.emit_template('footer.j2', {})

		print('-=' * 20)
		return '\n'.join(self.source)

	def compile(self, code):
		comp = TCC()
		comp.add_include_path('C:/Python37/include')
		comp.add_library_path('C:/Python37')
		comp.add_library('python37')

		try:
			print('Compiling...')
			comp.compile_string(code)
			print('Relocating...')
			comp.relocate()
		except:
			traceback.print_exc()
			return lambda ARGS, x, y, z, p, d, q, s: print('<Your func here>')

		print('Prototyping...')
		func_proto = ctypes.CFUNCTYPE(
			ctypes.py_object,  # Return type
			ctypes.py_object,  # ARGS
			ctypes.py_object,  # SYMBOL_TABLE
			ctypes.py_object,  # BRANCHES
		)

		print('Getting Symbol...')
		craft_main = comp.get_symbol('craft_main')
		print('FuncProto...')
		#return func_proto(a)
		return Function(func_proto(craft_main), self.branches)

	def compile_function(self, func):
		return self.compile(self.transpile(func))


# region
hello = '''
def: [
	[hello person]
	
	print: [$person]

	if: [True then: [
		print: ['It was True!']
		print: [$person]
	]]

	print: [BackOut]

	for: [
		[i 10]
		print: [$i]
	]

	return: [neg: [45]]
]
'''
hello = '''
def: [
	[fibo n]
	print: [format: ["In fibo({})" $n]]
	set: [a 0]
	set: [b 1]
	for: [[i $n]
		set: [tmp $b]
		set: [b +: [$a $b]]
		set: [a $tmp]
	]
	return: [$a]
]
'''
# endregion

jit = JIT()
func = craft_parse(hello)

c_code = jit.transpile(func)
#with open('output.c', 'w') as file:
#	file.write(c_code)
__code__ = jit.compile(c_code)
craft_set(getvalue(func)[0][0], __code__)


print('Running...')
print('\n------------------------')
ret = __code__(10)
print('------------------------\nDone.')
print(f'Return Value: {repr(ret)}')
def fibo(x):
	if x <= 1:
		return x
	return fibo(x - 1) + fibo(x - 2)
print(f'Expected Value: {fibo(10)}')
