class WingException(Exception):
	"""
	super() super()
	"""

class WingInternalException(Exception):
	"""
	Raise this to communicate Python/Wing errors without exposing
	interpreter internals.
	"""

class WingFunctionReturnException(Exception):
	"""
	For returning values from functions. The `wing_call` function will catch
	these exceptions and return the value contained in this class as the return
	value.
	"""
	def __init__(self, value):
		Exception.__init__(self)
		self.return_value = value


class WingLoopBreakException(Exception):
	"""
	"""


class WingLoopContinueException(Exception):
	"""
	"""
