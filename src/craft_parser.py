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
			return [__walk(i) for i in obj.asList()]
		return obj


def _type_cast_value(x, y, value):
	"""
	Convert the follocraft strings to Python objects:

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
		try:
			return float(value)
		except:
			return value
	else:
		return value


class SourceValidator:
	def __init__(self):
		self.pairs = list()
		self.source = ''

	def validate(self, string, line_number, value):
		"""
		This method is designed to be used from Pyparsing:

		<parser>.setParseAction(<validator>.validate)
		"""
		self.source = string
		#print(line_number, value[0], '->', string[line_number])
		self.pairs.append([line_number, value[0]])
		return value

	def panic(self):
		msg = '\nSyntaxError:\n'
		lines = iter(self.source.split('\n'))
		pair = self.pairs[-1]
		count = 0
		while count < pair[0]:
			line = next(lines)
			msg += f'{line}\n'
			count += len(line) + 1  # Account for '\n'

		indent = ' ' * len(line)
		msg += f'{indent}^\n'
		msg += f'{indent}|\n'
		msg += f'{indent}|\n'
		return SyntaxError(msg)



def craft_parse(text):
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
		| Identifier.addParseAction(_type_cast_value)
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
		pyp.ZeroOrMore(Comment | Function | List | Value) +
		RBRACKET
	)

	Program = pyp.OneOrMore(Comment | Function)

	# Validate for syntax error messages:
	validator = SourceValidator()
	Value.setParseAction(validator.validate)
	List.setParseAction(validator.validate)
	Identifier.addParseAction(validator.validate)
	#Comment.setParseAction(validator.validate)
	Function.setParseAction(validator.validate)
	Program.setParseAction(validator.validate)

	syntax_error = None
	try:
		return __walk(Program.parseString(text)[0])
	except Exception as e:
		syntax_error = validator.panic()

	# Now raise the exception with a clean stack trace
	raise syntax_error


if __name__ == '__main__':
	craft_parse('''
        Program:[
            print: [hi]
            [
        ]
	''')
