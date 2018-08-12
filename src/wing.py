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

from docopt import docopt

from wing_core 			import *
from wing_parser 		import *
from wing_exceptions 	import *
from wing_cli 			import *
from wing_interpreter 	import *

# Needed to import __wing__ dicts for built-in symbol table entries
import wing_operators
import wing_keywords

SYMBOL_TABLE.append(dict())
SYMBOL_TABLE[0].update(wing_operators.__wing__)
SYMBOL_TABLE[0].update(wing_keywords.__wing__)

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