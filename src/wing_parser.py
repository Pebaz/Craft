import pyparsing as pp

def __walk(obj):
	"""
	"""
	# If it's iterable, and is a "dictionary"
	if len(obj) > 1 and obj[1] == ':':
		# Return a mapping of it and process it's arguments also
		return { obj[0] : [__walk(i) for i in obj[2]] }
	# It's a normal value
	else:
		# Make it be a Python object, not ParseResults
		if isinstance(obj, ParseResults):
			return obj.asList()
		return obj


def wing_parse(text):
	Identifier = pp.Word(pp.alphanums + '!#$%&()*+,./;<=>?@\\^-_`{|}~')
	Value = (pp.QuotedString('"') | pp.Identifier)
	LBRACKET, RBRACKET, COLON = map(pp.Suppress, '[]:')

	Function = pp.Forward()
	List = pp.Forward()

	Function << pp.Dict(pp.Group(
		Identifier +
		pp.Literal(':') +
		pp.Group(
			LBRACKET +
			pp.ZeroOrMore(Function | List | Value) +
			RBRACKET
		)
	))

	List << pp.Group(
		LBRACKET +
		pp.ZeroOrMore(Value | List) +
		RBRACKET
	)

	return __walk(Function.parseString(text)[0])
