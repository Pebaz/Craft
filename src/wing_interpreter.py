import os.path
import yaml
from wing_parser import WingParser


class WingInterpreter:
	def __init__(self, wing):
		self.wing = wing
		self.wing_parser = WingParser()

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
				ast = self.wing_parser.parse(file.read())

			self.wing.handle_expression({ 'Program' : ast['Program'] })

			# Handle "if __name__ == '__main__"
			if 'Main' in ast:
				self.wing.handle_expression({ 'Program' : ast['Main'] })