from pyparsing import *
from pprint import *

Identifier = Word(alphanums + '!#$%&()*+,./;<=>?@\\^-_`{|}~')
Value = (QuotedString('"') | Identifier)
LBRACKET, RBRACKET, COLON = map(Suppress, '[]:')

Function = Forward()
List = Forward()

Function << Dict(Group(
	Identifier +
	Literal(':') +
	Group(
		LBRACKET +
		ZeroOrMore(Function | List | Value) +
		RBRACKET
	)
))

List << Group(
	LBRACKET +
	ZeroOrMore(Value | List) +
	RBRACKET
)

results = Function.parseString(open('test/syntax_test.wing').read())

pp = PrettyPrinter(width=1)

print(results[0])

def walk(obj):
	if len(obj) > 1 and obj[1] == ':':
		return { obj[0] : [walk(i) for i in obj[2]] }
	else:
		if isinstance(obj, ParseResults):
			return obj.asList()
		return obj

pp.pprint(walk(results[0]))
