"""
JIT compilation capability for Craft.

Can JIT compile any user-defined Craft function. For debugging or curiosity,
can 
"""

import ctypes, pathlib, itertools, traceback, multiprocessing  # Utilities
from concurrent.futures import ThreadPoolExecutor, as_completed
from pytcc import TCC  # C compiler as library
from j2do import j2do  # C code snippets
from craft_core import *  # craft_raise, BRANCH_FUNCTIONS, SYMBOL_TABLE


class JITFunction:
	""""""

	def __init__(self, func, branches: list):
		""""""
		self.name = 'NAME'
		self.func = func
		self.branches = branches

	def __repr__(self):
		return f'<JITFunction {self.name}>'

	def __call__(self, *args):
		""""""
		global SYMBOL_TABLE
		try:
			ret = self.func(
				list(args),
				SYMBOL_TABLE,
				self.branches
			)

			if not ret.err:
				return ret.value
			else:
				global TRACEBACK
				try:
					register_pyexception(ret.err)
					craft_raise(type(ret.err).__name__)
				except Exception as e:
					TRACEBACK.show_trace(e)
					raise e

		except SystemError as e:
			traceback.print_exc()


class JITCompiler:
	""""""
	PATH_PREFIX = pathlib.Path() / 'jit'

	def __init__(self, emit_stdout=False, emit_file=None):
		""""""
		global BRANCH_FUNCTIONS
		self.source = []
		self.branches = []
		self.branch_functions = [] + BRANCH_FUNCTIONS
		self.emit_stdout = emit_stdout
		self.emit_file = emit_file
	
	def get_source(self):
		""""""
		return '\n'.join(self.source)

	def __load_template(self, filename):
		""""""
		with open(str(JITCompiler.PATH_PREFIX / filename)) as file:
			return file.read()

	def emit(self, text=''):
		""""""
		# Output to stdout if desired
		if self.emit_stdout:
			print(text)

		# `self.transpile()` already opened the output file (if any)
		if self.emit_file:
			self.emit_file.write(text)

		self.source.append(text)

	def emit_lookup(self, name, counter):
		""""""
		lookup = f'var{next(counter)}'
		self.emit_template('lookup.j2', dict(lookup=lookup, name=name))
		return lookup

	def emit_args(self, arguments, counter):
		""""""
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
		""""""
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
		#self.emit_template('error_check.j2', {})
		return ret_name

	def emit_template(self, template, data):
		""""""
		self.emit(j2do(template, data, include=[JITCompiler.PATH_PREFIX]))	

	def transpile(self, ast):
		""""""
		# Open output file if set
		self.emit_file = open(self.emit_file, 'w') if self.emit_file else None

		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		counter = itertools.count()

		#print(':: Transpiling            ::')
		#print(ast, '\n\n')
		print(f':: Transpiling {getvalue(ast)[0][0]}')
		#print('=-' * 20)

		self.emit('#include <stdio.h>')
		self.emit_template('header.j2', {})

		# Push Scope
		self.emit_func({'push-scope' : []}, counter)

		self.emit('')

		# Now Bind all arguments to current (function) scope
		self.emit(j2do(
			"arguments.j2",
			dict(arg_names=arg_names),
			include=[JITCompiler.PATH_PREFIX]
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

		# Close output file if set
		self.emit_file = self.emit_file.close() if self.emit_file else None

		#print('-=' * 20)
		return '\n'.join(self.source), self.branches

	def compile(self, code):
		""""""
		comp = TCC()
		comp.add_include_path('C:/Python36/include')
		comp.add_library_path('C:/Python36')
		comp.add_library('python3')

		try:
			#print('Compiling...')
			comp.compile_string(code)
			#print('Relocating...')
			comp.relocate()
		except:
			traceback.print_exc()
			return lambda args, symtab, branches: print('<Your func here>')

		#print('Prototyping...')
		func_proto = ctypes.CFUNCTYPE(
			ctypes.py_object,  # Return type
			ctypes.py_object,  # ARGS
			ctypes.py_object,  # SYMBOL_TABLE
			ctypes.py_object,  # BRANCHES
		)

		#print('Getting Symbol...', end='')
		craft_main = comp.get_symbol('craft_main')
		#print(craft_main)
		#print('FuncProto...', end='')
		proto = func_proto(craft_main)
		#print(proto)
		return JITFunction(proto, self.branches)

	def compile_function(self, func):
		""""""
		#return self.compile(self.transpile(func))
		source = self.transpile(func)
		jitted = self.compile(source)
		print(f'JIT Compilation Finished: {jitted}')
		return jitted



class JIT:
	"""
	Allows many compilation jobs to run at the same time concurrently.
	"""

	def __init__(self):
		""""""
		self.pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
		self.comp = self.setup_compiler()

	def setup_compiler(self):
		comp = TCC()
		comp.add_include_path('C:/Python36/include')
		comp.add_library_path('C:/Python36')
		comp.add_library('python3')
		return comp

	def compile(self, function):
		""""""
		transpiler = JITCompiler()
		source, branches = transpiler.transpile(function)
		return self.pool.submit(self.compile_source, source, branches)

	def compile_source(self, source, branches):
		""""""
		comp = self.setup_compiler()
		ret = None
		try:
			comp.compile_string(source)
			comp.relocate()
			func_proto = ctypes.CFUNCTYPE(
				ctypes.py_object,  # Return type
				ctypes.py_object,  # ARGS
				ctypes.py_object,  # SYMBOL_TABLE
				ctypes.py_object,  # BRANCHES
			)
			craft_main = comp.get_symbol('craft_main')
			ret = JITFunction(func_proto(craft_main), branches)
		except:
			traceback.print_exc()
		finally:
			del comp
			return ret




if __name__ == '__main__':
	
	from craft_parser 		import *
	#from craft_exceptions 	import *
	#from craft_cli 			import *
	#from craft_interpreter 	import *
	# region
	fibo = '''
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
	hello = '''
	def: [
		[hello person]
		prin: ["Hello "]
		print: [$person]

		def: [[hi] print: [hi]]
		hi: []

		print: [BackOut]
	]
	'''
	# endregion


	# a = JITCompiler(emit_stdout=True)
	# a.compile_function(craft_parse(hello))
	# print('Done.')
	# exit()


	from random import choice
	jitter = JIT()
	status = [
		jitter.compile(craft_parse(choice([fibo, hello])))
		for i in range(10)
	]
	print('All tasks submitted')
	for future in as_completed(status):
		res = future.result()
		print(res)
		res(10)
	'''
	for future in status:
		print(future.result())
	'''
	exit()





	jit = JITCompiler()
	func = craft_parse(hello)
	#c_code = jit.transpile(func)
	#__code__ = jit.compile(c_code)
	__code__ = jit.compile_function(func)
	setup_sym_tab()
	craft_set(getvalue(func)[0][0], __code__)

	print(__code__(10))

	__code__ = jit.compile_function(func)

	print(__code__(11))

	exit()


	print('Running...')
	print('\n------------------------')
	ret = __code__(10)
	print('------------------------\nDone.')
	print(f'Return Value: {repr(ret)}')
	# def fibo(x):
	# 	if x <= 1:
	# 		return x
	# 	return fibo(x - 1) + fibo(x - 2)
	# print(f'Expected Value: {fibo(10)}')