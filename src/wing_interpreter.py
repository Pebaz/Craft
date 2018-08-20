from wing_core import *
from wing_parser import *

def run_file(filename):
	"""
	"""
	# Handle the top-level function named "Program" recursively
	with open(filename) as file:
		extension = os.path.splitext(filename)[1]

		ast = None

		if extension.lower() == '.yaml':
			ast = yaml.load(file)

		elif extension.lower() == '.wing':
			ast = wing_parse(file.read())

		if ast != None:

			handle_expression({ 'Program' : ast['Program'] })

			# Handle "if __name__ == '__main__"
			if 'Main' in ast:
				handle_expression({ 'Program' : ast['Main'] })