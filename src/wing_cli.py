from wing_core import *
from wing_parser import *


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

def __cli_sanitize_wing_code(code):
	"""
	Ensure that the code is wrapped in a Program function.
	"""
	return f'Program: [ {code} ]'


def run_cli(yaml_lang):
	"""
	"""
	print('Wing Programming Language')
	print('Version: 0.1.0\n')
	print('Press <enter> twice for running single commands.')
	print('Type "quit: []" or press CTCL > C to leave the program.\n')

	if yaml_lang:
		print('NOTE: Interpreting YAML code as Wing syntax.')

	try:
		code = ''
		while True:
			line = input('>>> ') if code == '' else input('... ')

			if line.strip() != '':
				code += line + '\n'

			else:
				if code.strip() == '':
					continue

				code = __cli_sanitize_yaml_code(code) if yaml_lang \
					else __cli_sanitize_wing_code(code)

				# Run the code
				try:
					ast = yaml.load(code) if yaml_lang else wing_parse(code)
					output = handle_expression(ast)

					if output != None:
						print(f' -> {output}')

				except Exception as e:
					print('WING ERROR:')
					traceback.print_exc()
					code = ''
					continue

				if code.strip().replace('\n', '') == 'quit':
					break

				code = ''

	except KeyboardInterrupt:
		pass
