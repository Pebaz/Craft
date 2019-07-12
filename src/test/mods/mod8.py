"""
Used to test when there is no __craft__ variable defined.
"""

from craft_core import expose

print('Imported module: mod8')

@expose()
def foo(x):
	print(f'Hello {x}')
