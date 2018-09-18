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

print(handle_expression(ast))
