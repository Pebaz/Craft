from craft_core import *
from craft_parser import *


def __cli_sanitize_yaml_code(code):
	"""
	Ensure that the code is wrapped in a Program function.
	"""
	new_code = 'Program:\n'

	for the_line in code.split('\n'):
		if the_line.strip() == '':
			continue

		if '  ' not in the_line:
			new_code += '  - ' + the_line + '\n'
		else:
			new_code += '  ' + the_line + '\n'

	return new_code

def __cli_sanitize_craft_code(code):
	"""
	Ensure that the code is wrapped in a Program function.
	"""
	return f'Program: [ {code} ]'


def run_cli(yaml_lang):
	"""
	"""
	global TRACEBACK
	print('Craft Programming Language')
	print('Version: 0.1.0\n')
	print('Press <enter> twice for running single commands.')
	print('Type "quit: []" or press CTCL > C to leave the program.\n')

	if yaml_lang:
		print('NOTE: Interpreting YAML code as Craft syntax.')

	try:
		code = ''
		while True:
			TRACEBACK.reset()
			line = input('>>> ') if code == '' else input('... ')

			if line.strip() != '':
				code += line + '\n'

			else:
				if code.strip() == '':
					continue

				code = __cli_sanitize_yaml_code(code) if yaml_lang \
					else __cli_sanitize_craft_code(code)

				# Run the code
				try:
					ast = yaml.load(code) if yaml_lang else craft_parse(code)
					output = handle_expression(ast)

					if output != None:
						print(f' -> {output}')

				except Exception as e:
					print('CRAFT ERROR:')
					traceback.print_exc()
					code = ''
					continue

				if code.strip().replace('\n', '') == 'quit':
					break

				code = ''

	except KeyboardInterrupt:
		pass
