import pyparsing as pyp

class WingParser:
	def __walk(obj):
		"""
		"""
		# If it's iterable, and is a "dictionary"
		if hasattr(obj, '__len__') and len(obj) > 1 and obj[1] == ':':
			# Return a mapping of it and process it's arguments also
			return { obj[0] : [__walk(i) for i in obj[2]] }
		# It's a normal value
		else:
			# Make it be a Python object, not ParseResults
			if isinstance(obj, pyp.ParseResults):
				return obj.asList()
			return obj


	def __type_cast_value(x, y, value):
		"""
		Convert the following strings to Python objects:

		 * Boolean
		 * Integer (hex, bin, oct, int)
		 * None
		"""
		value = value[0]

		if value == 'True':
			return True

		elif value == 'False':
			return False

		elif value == 'null' or value == 'None':
			return None

		elif value[0].isnumeric():
			for base in [10, 2, 8, 16]:
				try:
					return int(value, base=base)
				except:
					pass
			return value
		else:
			return value


	def parse(text):
		"""
		"""
		Identifier = pyp.Word(pyp.alphanums + '!#$%&()*+,./;<=>?@\\^-_`{|}~')
		Value = (
			pyp.QuotedString('"')
			| pyp.QuotedString("'")
			| Identifier.setParseAction(__type_cast_value)
		)
		LBRACKET, RBRACKET, COLON = map(pyp.Suppress, '[]:')

		Function = pyp.Forward()
		List = pyp.Forward()

		Function << pyp.Dict(pyp.Group(
			Identifier +
			pyp.Literal(':') +
			pyp.Group(
				LBRACKET +
				pyp.ZeroOrMore(Function | List | Value) +
				RBRACKET
			)
		))

		List << pyp.Group(
			LBRACKET +
			pyp.ZeroOrMore(Value | List) +
			RBRACKET
		)

		return __walk(Function.parseString(text)[0])