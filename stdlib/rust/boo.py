"""
Call with:

stringy: [1 2]
-> '3'
"""

import rust_py

__craft__ = {
	'stringy' : rust_py.sum_as_string
}
