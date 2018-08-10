class WingFunctionReturnException(Exception):
	"""
	For returning values from functions. The `wing_call` function will catch
	these exceptions and return the value contained in this class as the return
	value.
	"""
	def __init__(self, value):
		Exception.__init__(self)
		self.return_value = value