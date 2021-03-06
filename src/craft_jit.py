"""
JIT compilation capability for Craft.

Can JIT compile any user-defined Craft function. For debugging or curiosity,
can 
"""

import ctypes, pathlib, itertools, traceback, sys  # Utilities
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor, as_completed
from j2do import j2do  # C code snippets
from craft_core import *  # craft_raise, BRANCH_FUNCTIONS, SYMBOL_TABLE
from craft_parser import *

class JITFunction:
	""""""

	def __init__(self, func: dict, branches: list, buffer):
		""""""
		self.func = func
		self.branches = branches
		self.code_buffer = buffer

	def __repr__(self):
		return f'<{self.__class__.__name__}>'

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
	"""
	"""
	def __init__(self):
		self.code_buffer = None

	def compile(self, code):
		""""""
		from pytcc import TCCState as TCC
		python_dir = pathlib.Path(sys.exec_prefix)
		comp = TCC()
		comp.add_include_path(str(python_dir / 'include'))
		comp.add_library_path(str(python_dir))
		comp.add_library('python3')
		ret = None
		try:
			#print('Compiling...', id(self))
			comp.compile_string(code)
			#print('Relocating...')
			#comp.relocate()
			self.code_buffer = comp.get_bytes()
			#print('Prototyping...')
			func_proto = ctypes.CFUNCTYPE(
				ctypes.py_object,  # Return type
				ctypes.py_object,  # ARGS
				ctypes.py_object,  # SYMBOL_TABLE
				ctypes.py_object,  # BRANCHES
			)
			#print('Getting Symbol...')
			craft_main = comp.get_symbol('craft_main')
			ret = func_proto(craft_main)
		except:
			traceback.print_exc()
		finally:
			del comp
			return ret, self.code_buffer


class JITTranspiler:
	""""""
	PATH_PREFIX = pathlib.Path() / 'src/jit'

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

	def get_branches(self):
		""""""
		return self.branches

	def __load_template(self, filename):
		""""""
		with open(str(JITTranspiler.PATH_PREFIX / filename)) as file:
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
		self.emit(j2do(template, data, include=[JITTranspiler.PATH_PREFIX]))	

	def transpile(self, ast):
		""""""
		# Open output file if set
		self.emit_file = open(self.emit_file, 'w') if self.emit_file else None

		arg_names = getvalue(ast)[0][1:]
		body = getvalue(ast)[1:]
		counter = itertools.count()

		#print(':: Transpiling            ::')
		#print(ast, '\n\n')
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
			include=[JITTranspiler.PATH_PREFIX]
		))

		self.emit('\n// BODY')

		# Function body
		is_statement = lambda x: isinstance(x, dict) and len(x) == 1
		for statement in body:
			if is_statement(statement):
				self.emit(f'\n// {statement}')
			else:
				raise CraftException(f'SyntaxError: {statement}', {}, {})

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
		return '\n'.join(self.source)


class ApplyResultGhost:
	"""
	When running `JIT` in single threaded mode, it still needs to return an
	object that resembles a `multiprocessing.pool.ApplyResult`.
	"""
	def __init__(self, function):
		"""
		The JIT function to store until the caller needs it.
		"""
		self.function = function

	def ready(self):
		"""
		It's always ready since `JIT` is assumed to not be running in another
		thread if this class is ever instantiated.
		"""
		return True

	def get(self):
		"""
		Returns the JIT-compiled function, just not in an asynchronous way.
		"""
		return self.function


class JIT:
	"""
	Allows many compilation jobs to run at the same time concurrently.
	"""

	ENABLED = False
	USE_SINGLE_THREAD = False

	def __init__(self):
		""""""
		try:
			from pytcc import TCCState as TCC
		except:
			JIT.ENABLED = False
		self.pool = ThreadPool(processes=1)

	def compile(self, function):
		"""
		The `function` is a Dictionary containing a valid Craft function.
		"""
		if not JIT.ENABLED:
			raise Exception('JIT Compilation is disabled since LibTCC cannot be found on Path.')

		if JIT.USE_SINGLE_THREAD:
			jit_func = self.__compile(function)
			return ApplyResultGhost(jit_func)
		else:
			return self.pool.apply_async(self.__compile, (function,))

	def __compile(self, ast):
		""""""
		from craft_core import getvalue
		transpiler = JITTranspiler()
		source = transpiler.transpile(ast)
		branches = transpiler.branches.copy()
		compiler = JITCompiler()
		proto, buffer = compiler.compile(source)
		del compiler
		return JITFunction(proto, branches, buffer)
		





if __name__ == '__main__':
	JITTranspiler.PATH_PREFIX = pathlib.Path() / 'jit'

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

	# Test Setup
	def tmp_func(ast):
		jit = JIT()
		b = jit.compile_function(ast)
		del jit
		return b

	setup_sym_tab()
	jit = JIT()
	func = craft_parse(fibo)
	print(func)

	a = jit.compile(func)
	b = jit.compile(func)
	print(a.get()(10))
	print(b.get()(10))

	exit()

	for i in range(4):
		
		#c_code = jit.transpile(func)
		#__code__ = jit.compile(c_code)
		__code__ = jit.compile_function(func)
		craft_set(getvalue(func)[0][0], __code__)
		print('Running...')
		print('\n------------------------')
		ret = __code__(10)
		print('------------------------\nDone.')
		print(f'Return Value: {repr(ret)}')
		assert(ret == 55)

	print('\n\n\n\n\n\n\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	exit()

	pool = ThreadPool(processes=1)

	results = [pool.apply_async(tmp_func, (func,)) for i in range(2)]
	values = []
	# for i in results:
	# 	ret = i.get()
	# 	print(ret)
	# 	res = ret(10)
	# 	values.append(res)
	# 	print(res)

	import time
	while results:
		for i in range(len(results)):
			thread = results[i]
			if thread.ready():
				values.append(thread.get())
				results.pop(i)
				break
		print('.', end='')
		time.sleep(0.1)
	print()


	print('DONE!!!')
	print(values)
	#values = [i(10) for i in values]
	tmp = []
	for i in values:
		try:
			tmp.append(i(10))
		except OSError:
			tmp.append(-1)
	values = tmp
	print(values)
	print(f'All values == 55: {all([i == 55 for i in values])}')


