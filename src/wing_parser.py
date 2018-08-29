import sys
import pyparsing as pyp

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


def _type_cast_value(x, y, value):
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


class SourceValidator:
	def __init__(self):
		self.line = 1

	def validate(self, _ignore, value):
		"""
		This method is designed to be used from Pyparsing:

		<parser>.setParseAction(<validator>.validate)
		"""

		print('----->', value.count('\n') if '\n' in value else '')
		self.line += 1

		return value

	def validate_with_type_cast(self, _ignore, value):
		return _type_cast_value(None, None, value)

	def panic(self):
		print(f"Panic at line: {self.line}")



def wing_parse(text):
	"""
	"""
	LineComment = pyp.Combine(pyp.Literal('::') + pyp.restOfLine).suppress()
	BlockComment = pyp.Combine(
		pyp.Literal(':>') +
		pyp.SkipTo(pyp.Literal('<:')) +
		pyp.Literal('<:')
	).suppress()
	Comment = BlockComment | LineComment

	BlockComment = pyp.Combine(
		pyp.Literal(':<') +
		pyp.Combine(pyp.NotAny(pyp.Literal(':>')) + pyp.Word(pyp.printables + ' ')) +
		pyp.Literal('>:')
	)

	Identifier = pyp.Word(pyp.alphanums + '!#$%&()*+,./;<=>?@\\^-_`{|}~')
	Value = (
		Comment
		| pyp.QuotedString('"')
		| pyp.QuotedString("'")
		| Identifier.setParseAction(_type_cast_value)
	)
	LBRACKET, RBRACKET, COLON = map(pyp.Suppress, '[]:')

	Function = pyp.Forward()
	List = pyp.Forward()

	Function << pyp.Dict(pyp.Group(
		Identifier +
		pyp.Literal(':') +
		pyp.Group(
			LBRACKET +
			pyp.ZeroOrMore(Comment | Function | List | Value) +
			RBRACKET
		)
	))

	List << pyp.Group(
		LBRACKET +
		pyp.ZeroOrMore(Comment | Value | List) +
		RBRACKET
	)

	Program = pyp.OneOrMore(Comment | Function)

	# Validate for syntax error messages:
	validator = SourceValidator()
	Value.setParseAction(validator.validate)
	List.setParseAction(validator.validate)
	Identifier.setParseAction(validator.validate_with_type_cast)
	Comment.setParseAction(validator.validate)
	Function.setParseAction(validator.validate)
	Program.setParseAction(validator.validate)

	try:
		return __walk(Program.parseString(text)[0])
	except Exception as e:
		print(e)
		validator.panic()
		sys.exit()
