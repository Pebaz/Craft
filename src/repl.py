import yaml
from parser import WingParser

class WingREPL:

	def __init__(self, wing):
		self.wing_parser = WingParser()

	def __cli_sanitize_code(self, code):
		"""
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


	def run_cli(self):
		"""
		"""
		print('Wing Programming Language')
		print('Version: 0.1.0\n')
		print('Press <enter> twice for running single commands.')
		print('Type "quit: []" or press CTCL > C to leave the program.\n')

		if self.wing.is_yaml:
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

					if self.wing.is_yaml:
						code = self.__cli_sanitize_code(code)

					# Run the code
					try:
						ast = yaml.load(code) if self.wing.is_yaml else self.wing_parser.parse(code)
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