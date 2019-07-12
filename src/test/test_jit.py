try:
	import context
except ImportError:
	from . context import *
finally:
	from craft_test_utils import *


def test_jit():
	"""
	"""
	
	run_test_program(
		"""
		:: Define a new function
		def: [
			[hello person]
			prin: ["Hello "]
			print: [$person]
		]

		:: Show that the function starts as a user-defined function
		print: [$hello]

		:: Wait until it is done compiling
		sleep: [2]

		:: Show that it is now a JITFunction
		print: [$hello]

		:: Call it to make sure it works
		hello: [Pebaz]
		""",
		"""
		<Function hello:[]>
		<Function hello:[]>
		Hello Pebaz
		"""
	)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
