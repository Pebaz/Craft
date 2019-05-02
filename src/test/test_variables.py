try:
    import context
except ImportError:
    from .context import *
finally:
    from craft_test_utils import *


def test_set_int():
    """
	Test to see if setting a int variable has the correct value.
	"""

    run_test_program(
        """
		set: [age 24]
		""",
        """
		""",
    )
    assert query_symbol_table("age", SCOPE) == 24


def test_set_float():
    """
	Test to see if setting a float variable has the correct value.
	"""

    run_test_program(
        """
		set: [age 25.0]
		""",
        """
		""",
    )
    assert query_symbol_table("age", SCOPE) == 25.0


def test_set_str_no_quotes():
    """
	Test to see if setting a str_no_quotes variable has the correct value.
	"""

    run_test_program(
        """
		set: [name Pebaz]
		""",
        """
		""",
    )
    assert query_symbol_table("name", SCOPE) == "Pebaz"


def test_set_str_double_quotes():
    """
	Test to see if setting a str_double_quotes variable has the correct value.
	"""

    run_test_program(
        """
		set: [name "Pebaz"]
		""",
        """
		""",
    )
    assert query_symbol_table("name", SCOPE) == "Pebaz"


def test_set_str_single_quotes():
    """
	Test to see if setting a str_single_quotes variable has the correct value.
	"""

    run_test_program(
        """
		set: [name 'Pebaz']
		""",
        """
		""",
    )
    assert query_symbol_table("name", SCOPE) == "Pebaz"


def test_set_bool():
    """
	Test to see if setting a bool variable has the correct value.
	"""

    run_test_program(
        """
		set: [alive True]
		""",
        """
		""",
    )
    assert query_symbol_table("alive", SCOPE) == True


def test_set_list():
    """
	Test to see if setting a list variable has the correct value.
	"""

    run_test_program(
        """
		set: [nums list: [[1 2 3]]]
		""",
        """
		""",
    )
    assert query_symbol_table("nums", SCOPE) == [1, 2, 3]


def test_set_dict():
    """
	Test to see if setting a dict variable has the correct value.
	"""

    run_test_program(
        """
		set: [ages hash: [Pebaz 24 Protodip 27 Yelbu 22]]
		""",
        """
		""",
    )
    assert query_symbol_table("ages", SCOPE) == dict(Pebaz=24, Protodip=27, Yelbu=22)


def test_set_tuple():
    """
	Test to see if setting a tuple variable has the correct value.
	"""

    run_test_program(
        """
		set: [nums tuple: [[1 2 3]]]
		""",
        """
		""",
    )
    assert query_symbol_table("nums", SCOPE) == (1, 2, 3)


def test_set_variable():
    """
	Test to make sure that setting a variable to the value of a variable
	contains the correct value.
	"""

    run_test_program(
        """
		set: [age 24]
		set: [my-age $age]
		""",
        """
		""",
    )
    assert query_symbol_table("my-age", SCOPE) == 24


if __name__ == "__main__":
    for test in dir():
        if test.startswith("test_"):
            globals()[test]()
