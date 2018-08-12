"""Wing Programming Language

Usage:
  {0}
  {0} (-v | --version)
  {0} [-y | --yaml]
  {0} [-y | --yaml] FILENAME
  {0} [-d | --debug] FILENAME

Options:
  FILE            Run a Wing Program From Source
  -v --version    Display Wing Version and Exit
  -d --debug      Debug a Wing Program
  -y --yaml       Interpret YAML as a Wing program

To run the Wing REPL, supply no arguments:
  {0}
"""


import sys, os, os.path, pprint, traceback, imp
from pathlib import Path
import yaml
import pyparsing as pyp
from docopt import docopt

from wing_core import *
from wing_parser import *
from wing_exceptions import *
from wing_operators import *
from wing_keywords import *
from wing_cli import *
from wing_interpreter import *

# -----------------------------------------------------------------------------
#                       W I N G   I N T E R P R E T E R
# -----------------------------------------------------------------------------

# Print debugging for now


SYMBOL_TABLE.append({
	# Operators
	'+' : wing_add,
	'+=' : wing_add_equal,
	'-' : wing_sub,
	'*' : wing_mul,
	'/' : wing_div,
	'%' : wing_mod,
	'**' : wing_exp,
	'=' : wing_equals,
	'<>' : wing_not_equals,
	'!=' : wing_not_equals,
	'>' : wing_greater_than,
	'<' : wing_less_than,
	'>=' : wing_greater_than_or_equal_to,
	'<=' : wing_less_than_or_equal_to,
	'&' : wing_bitwise_and,
	'|' : wing_bitwise_or,
	'^' : wing_bitwise_xor,
	'~' : wing_bitwise_complement,
	'<<' : wing_bitwise_left_shift,
	'>>' : wing_bitwise_right_shift,

	# Built-Ins
	'Program' : wing_program,
	'push-scope' : wing_push_scope,
	'pop-scope' : wing_pop_scope,
	'create-named-scope': wing_create_named_scope,
	'globals' : wing_globals,
	'locals' : wing_locals,
	'quit' : wing_exit,
	'exit' : wing_exit,
	'def' : wing_def,
	'return' : wing_return,
	'call' : wing_call,
	'fn' : wing_lambda,
	'struct' : wing_struct,
	'new' : wing_new,
	'set' : wing_set,
	'for' : wing_for,
	'if' : wing_if,
	'then' : wing_then,
	'else' : wing_else,
	'print' : wing_print,
	'comment' : wing_comment,
	'and' : wing_and,
	'or' : wing_or,
	'not' : wing_not,
	'byval' : wing_byval,
	'import' : wing_import,
	'dir' : wing_dir,
})


def main(args):
	"""
	"""
	global DEBUG

	# Make the docstring .EXE friendly
	usage = __doc__.format(args[0])
	arguments = docopt(usage, argv=args[1:], version='Wing 0.1.0')

	if arguments['FILENAME'] != None:
		DEBUG = arguments['--debug']
		run_file(arguments['FILENAME'])	
	else:
		run_cli(arguments['--yaml'])


if __name__ == '__main__':
	sys.exit(main(sys.argv))

	'''
	import cProfile
	def profile():
		main(sys.argv)
	cProfile.run('profile()', sort='ncalls')
	'''