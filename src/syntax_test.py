from pyparsing import *

Identifier = Word(alphanums + '!#$%&()*+,./;<=>?@\\^_`{|}~')

Value = (
	QuotedString('"')
	| Identifier
)

List = (
	Literal('[') +
	Forward() +
	Literal(']')
)

Function = (
	Identifier.setParseAction(lambda x, y, z: print(z, y)) +
	Literal(':') +
	List
)

List[0][1] << ZeroOrMore(Function | List | Value)

Program = OneOrMore(Function)

print('Starting test...')
print(Program.parseString(open('test/syntax_test.txt').read()))
print('Done!')

