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


def test_switch_case_default():
	""""""
	
	run_test_program(
		"""
		foreach: [
			[number [2 5 10]]

			:: Test default switch-case-default syntax
			switch: [$number
				case: [2
					print: [222]
				]

				case: [5
					print: [555]
				]

				default: [
					print: [$number]
				]
			]
		]

		:: Make sure malformed syntax errors out
		try: [
			switch: [5
				default: [print: [Uh oh]]
				default: [print: [Uh oh]]
			]

			catch: [[]
				print: [MalformedSwitchStatement]
			]
		]

		:: Make sure empty switch statements are supported
		switch: [5
			case: [2 print: ["Won't get here"]]
			:: Empty default block is inserted here
		]
		print: [EmptyDefaultBlock]
		""",
		"""
		222
		555
		10
		MalformedSwitchStatement
		EmptyDefaultBlock
		"""
	)


def test_case():
	run_test_program(
		"""
		case: [
			comment: ["Skip Me"]
			print: [Hello]
			print: [World]
		]
		""",
		"""
		Hello
		World
		"""
	)



def test_break():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		for: [[i 10]
			if: [=: [%: [$i 2] 0] then: [
				continue: []
			]]

			if: [=: [$i 7] then: [
				break: []
			]]

			print: [$i]
		]
		""",
		"""
		1
		3
		5
		"""
	)


def test_continue():
	"""
	Description of test.
	Func name must start with `test_`.
	"""
	
	run_test_program(
		"""
		for: [[i 10]
			if: [=: [%: [$i 2] 0] then: [
				continue: []
			]]

			print: [$i]
		]
		""",
		"""
		1
		3
		5
		7
		9
		"""
	)


def test_while():
	""""""
	
	run_test_program(
		"""
		set: [count 0]
		while: [
			<: [$count 10]
			print: [Go]
			+=: [$count 1]
			if: [=: [%: [$count 2] 0] then: [
				continue: []
			]]

			if: [=: [$count 7] then: [
				break: []
			]]
		]
		""",
		"""
		Go
		Go
		Go
		Go
		Go
		Go
		Go
		"""
	)


def test_until():
	""""""
	
	run_test_program(
		"""
		set: [count 0]
		until: [
			>: [$count 10]
			print: [Go]
			+=: [$count 1]
			if: [=: [%: [$count 2] 0] then: [
				continue: []
			]]

			if: [=: [$count 7] then: [
				break: []
			]]
		]
		""",
		"""
		Go
		Go
		Go
		Go
		Go
		Go
		Go
		"""
	)



def test_import():
	""""""

	global CRAFT_PATH
	CRAFT_PATH.append('src/test')

	run_test_program(
		"""
		import: [mods.mod1]
		foo: [Craft]
		import: [mods.mod2]
		foo: [YAML]
		import: [mods.mod3]
		foo: [Python]

		:: Test Module Existence
		try: [
			import: [does-not-exist]
			catch: [[]
				print: ["Module doesn't exist :("]
			]
		]

		:: Test import Python without __craft__
		try: [
			import: [mods.mod4]
			catch: [[]
				print: ["Module doesn't define __craft__"]
				print: ["So we can't import Python funcs"]
			]
		]

		:: Test import multiple mods
		import: [
			mods.mod5
			mods.mod6
			mods.mod7
		]

		:: Test "from import" functionality
		import: [[mods.mod8 foo]]
		foo: [Python]
		""",
		"""
		Imported module: mod1
		Hello Craft
		Imported module: mod2
		Hello YAML
		Imported module: mod3
		Hello Python
		Module doesn't exist :(
		Imported module: mod4
		Module doesn't define __craft__
		So we can't import Python funcs
		mod5
		mod6
		mod7
		Imported module: mod8
		Hello Python
		"""
	)

	CRAFT_PATH.pop()






















def test_byval():
	""""""
	
	run_test_program(
		"""
		set: [name Pebaz]
		print: [name]
		print: [$name]
		print: [$$name]
		print: [byval: [name]]
		print: [byval: [$name]]
		""",
		"""
		name
		Pebaz
		$name
		name
		$name
		"""
	)


def test_byref():
	""""""
	
	run_test_program(
		"""
		struct: [point x y]
		def: [
			[show-point the-point]
			print: [$the-point.x $the-point.y]
		]
		def: [
			[move-point the-point]
			+=: [$the-point.x 4]
		]
		set: [a new: [$point 0 0]]
		move-point: [byref: [$a]]
		show-point: [byref: [$a]]
		""",
		"""
		4 0
		"""
	)






def test_struct():
	""""""
	
	run_test_program(
		"""
		struct: [point x y]
		def: [
			[show-point the-point]
			print: [$the-point.x $the-point.y]
		]
		def: [
			[move-point the-point]
			+=: [$the-point.x 4]
		]
		set: [a new: [$point 0 0]]
		show-point: [$a]
		move-point: [$a]
		show-point: [$a]
		""",
		"""
		0 0
		4 0
		"""
	)





if __name__ == '__main__':
	for test in dir():
		if test.startswith('test_'):
			globals()[test]()
