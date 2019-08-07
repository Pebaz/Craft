from craft_core import expose

print('Imported module: mod3')

@expose()
def foo(x):
	print(f'Hello {x}')
