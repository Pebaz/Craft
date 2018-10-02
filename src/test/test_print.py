import sys
sys.path.append('..')
from wing_core import *
from wing_parser import *

setup_sym_tab()

source = \
"""
Program:
[
	print: ["Hello World!"]
]
"""

ast = wing_parse(source)

class STDOutWrapper:
	def __init__(self):
		pass

sys.stdout = STDOutWrapper()

handle_expression(ast)
