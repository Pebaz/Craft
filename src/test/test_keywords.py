try:
	import context
except ImportError:
	from . context import *
finally:
	from craft_test_utils import *


def test_try_catch_finally():
	""""""
	
	run_test_program(
		"""
		:: Catch all
		try: [
			print: [Try]
			/: [0 0]
			catch: [[] print: [Catch]]
			finally: [print: [Finally]]
		]

		:: Catch explicitly
		try: [
			print: [Try]
			/: [0 0]
			catch: [[ZeroDivisionError] print: [Catch]]
			finally: [print: [Finally]]
		]

		:: Catch with exception `as`
		try: [
			print: [Try]
			/: [0 0]
			catch: [
				[ZeroDivisionError][ex]
				print: [$ex.name]
				print: [$ex.desc]
				print: [$ex.meta]
			]
			finally: [print: [Finally]]
		]

		:: Skip Catch
		try: [
			print: [Try]
			/: [0 0]
			catch: []
			finally: [print: [Finally]]
		]

		:: Verify Push & Pop Scope 1
		print: [len: [get-symbol-table: []]]
		try: [
			print: [len: [get-symbol-table: []]]
			/: [0 0]
			catch: []
			finally: [
				print: [len: [get-symbol-table: []]]
			]
		]
		print: [len: [get-symbol-table: []]]

		:: Verify Push & Pop Scope 2
		print: [len: [get-symbol-table: []]]
		try: [
			print: [len: [get-symbol-table: []]]
			finally: [
				print: [len: [get-symbol-table: []]]
			]
		]
		print: [len: [get-symbol-table: []]]

		:: Verify that try will work without `catch` or `finally` 1
		try: [
			print: ["No soap doc"]
		]

		:: Verify that try will not crash
		try: [
			/: [0 0]
		]
		""",
		"""
		Try
		Catch
		Finally
		Try
		Catch
		Finally
		Try
		ZeroDivisionError
		division by zero
		None
		Finally
		Try
		Finally
		1
		2
		2
		1
		1
		2
		2
		1
		No soap doc
		"""
	)


def test_register_exception():
	""""""
	
	run_test_program(
		"""
		print: [len: [get-exceptions: []]]
		exception: [SomeOtherException "Something went wrong"]
		print: [len: [get-exceptions: []]]
		print: [len: [
			get: [get-exceptions: [] SomeOtherException]
		]]
		""",
		"""
		0
		2
		3
		"""
	)


if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()