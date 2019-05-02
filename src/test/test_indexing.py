try:
    import context
except ImportError:
    from .context import *
finally:
    from craft_test_utils import *


def test_get_list():
    """
	"""

    run_test_program(
        """
		set: [a [1 2 3]]
		print: [get: [$a 0]]
		print: [get: [$a neg: [1]]]
		""",
        """
		1
		3
		""",
    )


def test_cut_list():
    """
	"""

    run_test_program(
        """
		""",
        """
		""",
    )


def test_slice_list():
    """
	"""

    run_test_program(
        """
		""",
        """
		""",
    )


def test_get_list():
    """
	"""

    run_test_program(
        """
		set: [a tuple: [[1 2 3]]]
		print: [get: [$a 0]]
		print: [get: [$a neg: [1]]]
		""",
        """
		1
		3
		""",
    )


def test_get_dict():
    """
	"""

    run_test_program(
        """
		set: [a hash: [a 1 b 2]]
		print: [get: [$a b]]
		""",
        """
		2
		""",
    )


if __name__ == "__main__":
    for test in dir():
        if test.startswith("test_"):
            globals()[test]()
