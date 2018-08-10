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

results = Function.parseString(open('test/syntax_test.txt').read())

pp = PrettyPrinter(width=1)
#pp.pprint(results.asDict())

print(results[0])


{
	'Program':
	{
		'print': [],
		'struct': ['point', 'x', 'y'],
		'def': {'set': {'+': ['$the-point.x', '4']}},
		'set': {'new': ['$point', '0', '0']},
		'move-point': {'byval': ['$a']},
		'show-point': {'byval': ['$a']}
	}
}

['Program', ':',
	[
		['print', ':', []],
		['struct', ':', ['point', 'x', 'y']],
		['def', ':',
			[
				['show-point', 'the-point'],
				['print', ':', ['$the-point.x', '$the-point.y']]
			]
		],
		['def', ':',
			[
				['move-point', 'the-point'],
				['set', ':', ['$the-point.x', ['+', ':', ['$the-point.x', '4']]]]
			]
		],
		['set', ':', ['a', ['new', ':', ['$point', '0', '0']]]],
		['move-point', ':', [['byval', ':', ['$a']]]],
		['move-point', ':', [['byval', ':', ['$a']]]],
		['show-point', ':', [['byval', ':', ['$a']]]]
	]
]