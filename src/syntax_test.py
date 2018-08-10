from pyparsing import *

Identifier = Word(alphanums + '!#$%&()*+,./;<=>?@\\^-_`{|}~')
Value = (QuotedString('"') | Identifier)
LBRACKET, RBRACKET, COLON = map(Suppress, '[]:')

Function = Forward()
List = Forward()

Function << Dict(Group(
	(Identifier + Literal(':')) +
	LBRACKET +
	ZeroOrMore(Function | List | Value) +
	RBRACKET
))

List << Group(
	LBRACKET +
	ZeroOrMore(Value) +
	RBRACKET
)

print(Function.parseString(open('test/syntax_test.txt').read()))



