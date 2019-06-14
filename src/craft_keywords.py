import sys, pprint, traceback
from pathlib import Path
import yaml, os
import pyparsing as pyp
from craft_core import *
from craft_parser import *

pp = pprint.PrettyPrinter(width=1)

# -----------------------------------------------------------------------------
#            S T A N D A R D   L I B R A R Y   F U N C T I O N S
# -----------------------------------------------------------------------------


def craft_try(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    global SCOPE
    catches = [i for i in args if getkey(i) == 'catch']
    finale = [i for i in args if getkey(i) == 'finally']
    exceptors = catches + finale

    craft_push_scope()
    pushed = True
    try:
        for i in args:
            if i not in exceptors:
                get_arg_value(i)

    # If an exception occurs, Craft will have already registered it!
    except Exception as e:
        # Make sure to keep track of enclosing scope
        craft_pop_scope()
        pushed = False

        error_code = query_symbol_table(e.name, SCOPE)

        for catch in catches:
            if len(getvalue(catch)) == 0:
                continue
            exceptions = get_args(getvalue(catch)[0])
            except_matches = any(i in [error_code, e.name] for i in exceptions)

            #import ipdb; ipdb.set_trace()

            # This is the `as` functionality
            the_as = getvalue(catch)[1]
            the_exception = {
                'name' : e.name, 'desc' : e.desc, 'meta' : e.meta
            }

            if len(exceptions) == 0 or except_matches:
                # Make the second statement that the catch function interprets
                # to be binding the exception to local scope since it ignores
                # the first one in the list.
                if isinstance(the_as, list):
                    catch[getkey(catch)][1] = {
                        'set' : [the_as[0], { 'byval' : [the_exception] }]
                    }

                get_arg_value(catch)

                # Stop since the error has already been caught
                break
    finally:
        if pushed:
            craft_pop_scope()

        if len(finale) > 0:
            get_args(finale)


def craft_catch(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    # Must ignore first argument since `craft_try` reads it.
    craft_push_scope()
    get_args(args[1:])
    craft_pop_scope()


def craft_finally(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    craft_push_scope()
    get_args(args)
    craft_pop_scope()


def craft_exception(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    register_exception(*get_args(args))



def craft_switch(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    match = get_arg_value(args[0])
    cases = [i for i in args[1:] if getkey(i) == 'case']
    default = [i for i in args[1:] if getkey(i) == 'default'][0]

    # Handle malformed switch statement
    if len(default) > 1:
        ldefs = len(default)
        raise Exception(f'Only 1 default clause excepted, found: {ldefs}')

    # Create a blank program function call if there is no default
    if len(default) == 0:
        default = { 'Program' : [] }

    # Run the case block if the value matches
    for case in cases:
        # Obtain the first value in the case block and potentially match it
        statements = getvalue(case)
        if get_arg_value(statements[0]) == match:
            get_args(statements[1:])
            break

    # Matching case was not found, handle default clause
    else:
        get_arg_value(default)


def craft_case(*args):
    """
    Ignores the first argument since it is a value to use with `switch`.
    """
    get_args(args[1:])


def craft_default(*args):
    """
    Run the code therein since there is no match condition
    """
    get_args(args)


def craft_break(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    raise CraftLoopBreakException()


def craft_continue(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    raise CraftLoopContinueException()


def craft_while(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    condition = args[0]

    push_return_point()

    craft_push_scope()

    while get_arg_value(condition):
        try:
            get_args(args[1:])
        except CraftLoopContinueException:
            pass
        except CraftLoopBreakException:
            break

    cull_scopes(pop_return_point())


def craft_until(*args):
    """
<Short Description>

<Long Description>

Args:
  <Argument List>

Returns:
  <Description of Return Value>
"""
    condition = args[0]

    push_return_point()

    craft_push_scope()

    while not get_arg_value(condition):
        try:
            get_args(args[1:])
        except CraftLoopContinueException:
            pass
        except CraftLoopBreakException:
            break

    cull_scopes(pop_return_point())


def __craft_import__query_dir(filename):
    """
    Returns the YAML/CRAFT/PY file after searching the path.
    """
    global CRAFT_PATH

    for path in CRAFT_PATH:
        p = Path(path)
        mod_yaml = p / f'{filename}.yaml'
        mod_craft = p / f'{filename}.craft'
        mod_py = p / f'{filename}.py'

        if mod_yaml.exists():
            return mod_yaml

        elif mod_craft.exists():
            return mod_craft

        elif mod_py.exists():
            return mod_py

    # If none has been returned, it doesn't exist in CRAFT_PATH
    raise Exception(f'Cannot import name: {filename}. No matching .CRAFT, .YAML or .PY was found in CRAFT_PATH.')


def craft_import(*args):
    """
    1. YAML import
    2. Craft import
    3. Py import

    ```YAML
    # Import searches start from CWD and go inward:
    import: [craft.lang.builtins]
    # It would look in <CWD>/craft/lang/builtins

    # From imports:
    import: [[craft.lang.builtins, name1]]
    # from craft.lang.builtins import name1
    ```

    1. Get import name.
    2. If no dots, search CWD
    3. If not found, search CraftPath (in future)
    4. If dots, search all CraftPath dirs for it
    """
    args = get_args(args)

    for impp in args:
        to_import = impp if isinstance(impp, str) else impp[0]
        module = __craft_import__query_dir(to_import.replace('.', '/'))

        with open(str(module)) as file:
            if module.suffix == '.yaml':
                ast = yaml.load(file.read())
                if ast != None:
                    handle_expression({ 'Program' : ast['Program'] })

            elif module.suffix == '.craft':
                ast = craft_parse(file.read())
                handle_expression({ 'Program' : ast['Program'] })

            else:
                # TODO(Pebaz): Update to allow for importing PYDs
                sys.path.append(str(module.parent))

                pymod = module.name.replace(module.suffix, '')
                pymod = imp.load_source(pymod, str(module))

                if '__craft__' not in dir(pymod):
                    raise Exception('Unable to import Python module: no __craft__ variable.')

                if isinstance(impp, str):
                    for name in pymod.__craft__:
                        craft_set(name, pymod.__craft__[name])
                else:
                    for name in impp[1:]:
                        craft_set(name, pymod.__craft__[name])

def craft_and(*args):
    """
    Logical AND operator.
    """
    if len(args) > 2:
        raise Exception(f'Too many operands in logical AND: {args}')

    args = get_args(args)
    return args[0] and args[1]


def craft_or(*args):
    """
    Logical OR operator.
    """
    if len(args) > 2:
        raise Exception(f'Too many operands in logical OR: {args}')

    args = get_args(args)
    return args[0] or args[1]


def craft_not(*args):
    """
    Logical NOT operator.
    """
    if len(args) > 1:
        raise Exception(f'Too many operands in logical NOT: {args}')

    return not get_arg_value(args[0])


def craft_foreach(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    var, iterable = get_args(args[0])

    push_return_point()
    craft_push_scope()

    for i in iterable:
        try:
            craft_set(var, i)
            get_args(args[1:])
        except CraftLoopContinueException:
            continue
        except CraftLoopBreakException:
            break
        except Exception:
            traceback.print_exc()

    cull_scopes(pop_return_point())


def craft_for(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    control = args[0]

    var, start, stop, step = [None] * 4

    if len(control) == 4:
        var, start, stop, step = get_arg_value(control)

    elif len(control) == 3:
        var, start, stop, step = *get_arg_value(control), 1

    elif len(control) == 2:
        var, stop, start, step = *get_arg_value(control), 0, 1

    else:
        raise Exception(f'Malformed control value: (var, start, stop, step)')

    push_return_point()
    craft_push_scope()

    for i in range(start, stop, step):
        try:
            craft_set(var, i)
            get_args(args[1:])
        except CraftLoopContinueException:
            continue
        except CraftLoopBreakException:
            break
        except Exception as e:
            traceback.print_exc()

    pnt = pop_return_point()
    cull_scopes(pnt)


def craft_if(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    if len(args) > 3 or len(args) < 2:
        raise Exception(f'Malformed if statement at:\n{args}')

    # Testing condition
    c = args[0]

    # Run the THEN function if the condition is equal to True
    if handle_expression(c) if isinstance(c, dict) else handle_value(c):
        craft_push_scope()
        handle_expression(args[1])
        craft_pop_scope()

    # Handle ELSE clause if it was added
    elif len(args) == 3:
        craft_push_scope()
        handle_expression(args[2])
        craft_pop_scope()


def craft_unless(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    if len(args) > 3 or len(args) < 2:
        raise Exception(f'Malformed if statement at:\n{args}')

    # Testing condition
    c = args[0]

    # Run the THEN function if the condition is equal to True
    if not handle_expression(c) if isinstance(c, dict) else not handle_value(c):
        craft_push_scope()
        handle_expression(args[1])
        craft_pop_scope()

    # Handle ELSE clause if it was added
    elif len(args) == 3:
        craft_push_scope()
        handle_expression(args[2])
        craft_pop_scope()


def craft_then(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    args = get_args(args)


def craft_else(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    args = get_args(args)


def craft_globals(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    pp.pprint(SYMBOL_TABLE)
    pp.pprint(EXCEPTIONS)


def craft_locals(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    global SYMBOL_TABLE, SCOPE
    pp.pprint(SYMBOL_TABLE[SCOPE])


def craft_exit(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    sys.exit()


def craft_comment(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """


def craft_print(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    print(*get_args(args))


def craft_prin(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    print(*get_args(args), end='')


def craft_def(*args):
    """
    Bind function name to variable in current scope. This will allow it to be
    called.
    """
    declaration = get_arg_value(args[0])
    func_name = declaration[0]
    func_args = declaration[1:]
    func_definition = args[1:]
    craft_set(func_name, [func_args, func_definition])


def craft_return(*args):
    """
    The `craft_call` function will catch this exception and then return the
    value from it.
    """
    if len(args) > 1:
        ex = f'Only 1 value can be returned from function, got {len(args)}.'

        # TODO(Pebaz): Should this return a tuple rather than crash?

        raise Exception(ex)

    value = get_arg_value(args[0])
    raise CraftFunctionReturnException(value)


def craft_lambda(*args):
    """
    TODO(Pebaz): Fix `craft_call` to be able to handle lambdas.
    """
    arguments = get_arg_value(args[0])
    definition = args[1:]
    return [arguments, definition]


def craft_struct(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    args = get_args(args)
    struct_name = args[0]
    struct_members = args[1:]
    craft_set(struct_name, struct_members)


def craft_new(*args):
    """
    Must be able to be extended to build classes/types later.

    Structs: hold only vars
    Types: hold vars and functions
    Classes: hold vars, functions, and support oop
    """
    args = get_args(args)
    definition, member_values = args[0], args[1:]

    # If the values provided do not match the definition given,
    # initialize the blank members to zero.
    if len(definition) > len(member_values):
        member_values.extend([
            None for i in range(len(definition) - len(member_values))
        ])

    # Create a dictionary out of the names and values of the members
    struct = dict(zip(definition, member_values))
    return struct

"""@jit_compiled('''
while (1) {
	int x = 0;
}
''')"""
def craft_program(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    global TRACEBACK

    # NOTE(Pebaz): To show a Python internal error, simply call: get_args(args)
    # TODO(Pebaz): Make it so that a command line switch can show the traceback

    try:
        get_args(args)
    except Exception as e:
        TRACEBACK.show_trace(e)


def craft_byval(*args):
    """
    Since functions only try one round of evaluation for arguments, arguments
    can be passed "by value" instead of "by reference/name".
    """
    return args[0]


def craft_byref(*args):
    """
    Wrap the dictionary in a protective layer.
    """
    return get_args(args)


def craft_dir(value):
    global pp
    if isinstance(value, str):
        pp.pprint(get_arg_value(value))
    elif isinstance(value, dict):
        pp.pprint(dict)


# -----------------------------------------------------------------------------
# Data Types
# -----------------------------------------------------------------------------

def craft_hash(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    if len(args) % 2 != 0:
        raise Exception(f'Expected even number of arguments, got {len(args)}.')

    args = get_args(args)

    ret = {
        args[i] : args[i + 1]
        for i in range(0, len(args), 2)
    }

    return ret

def craft_get(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    if len(args) > 2:
        raise Exception(f'Too many arguments supplied, got: {len(args)}')

    args = get_args(args)
    return args[0][args[1]]


def craft_cut(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    args = get_args(args)
    raise Exception('Not implemented yet: cut')


def craft_str(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    return str(get_arg_value(args[0]))


def craft_int(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    return int(get_arg_value(args[0]))

def craft_bool(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    return bool(get_arg_value(args[0]))


def craft_float(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    return float(get_arg_value(args[0]))


def craft_tuple(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    if len(args) == 0:
        raise Exception(f'Expected a list of values, got nothing.')
    return tuple(get_arg_value(args[0]))


def craft_list(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    return list(get_arg_value(args[0]))


def craft_collected_set(*args):
    """
    <Short Description>

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    return set(get_arg_value(args[0]))


def craft_format(*args):
    """
    Formats a given string with the given arguments.

    <Long Description>

    Args:
      <Argument List>

    Returns:
      <Description of Return Value>
    """
    args = get_args(args)
    return args[0].format(*args[1:])


def jit(func):
	print(f'Need to remove {func.__name__}() from builtins!')
	return func

@jit
def getL(*args):
	args = get_args(args)
	print(args[0])
	return args[0]

__craft__ = {
    # Built-Ins
	'getL' : getL,
	'push-return-point'     : push_return_point,
	'pop-return-point'      : pop_return_point,
	'get-scope'             : craft_get_scope,
	'get-symbol-table'      : craft_get_symbol_table,
	'get-return-points'     : craft_get_return_points,
	'get-exceptions'        : craft_get_exceptions,
	'get-traceback'         : craft_get_traceback,
	'get-craft-path'        : craft_get_path,
	'get-is-debug'          : craft_get_is_debug,
	'query-symbol-table'    : query_symbol_table,
    'Program'               : craft_program,
    'push-scope'            : craft_push_scope,
    'pop-scope'             : craft_pop_scope,
    'create-named-scope'    : craft_create_named_scope,
    'globals'               : craft_globals,
    'locals'                : craft_locals,
    'quit'                  : craft_exit,
    'exit'                  : craft_exit,
    'def'                   : craft_def,
    'return'                : craft_return,
    'call'                  : craft_call,
    'fn'                    : craft_lambda,
    'struct'                : craft_struct,
    'new'                   : craft_new,
    'set'                   : craft_set,
    'get'                   : craft_get,
    'cut'                   : None,
    'slice'                 : None,
    'for'                   : craft_for,
    'foreach'               : craft_foreach,
    'if'                    : craft_if,
    'unless'                : craft_unless,
    'then'                  : craft_then,
    'else'                  : craft_else,
    'print'                 : craft_print,
    'prin'                  : craft_prin,
    'comment'               : craft_comment,
    'and'                   : craft_and,
    'or'                    : craft_or,
    'not'                   : craft_not,
    'byval'                 : craft_byval,
    'import'                : craft_import,
    'dir'                   : craft_dir,
    'break'                 : craft_break,
    'continue'              : craft_continue,
    'while'                 : craft_while,
    'until'                 : craft_until,
    'hash'                  : craft_hash,
    'str'                   : craft_str,
    'int'                   : craft_int,
    'bool'                  : craft_bool,
    'float'                 : craft_float,
    'tuple'                 : craft_tuple,
    'list'                  : craft_list,
    'collected_set'         : craft_collected_set,
    'switch'                : craft_switch,
    'case'                  : craft_case,
    'default'               : craft_default,
    'try'                   : craft_try,
    'catch'                 : craft_catch,
    'finally'               : craft_finally,
    'exception'             : craft_exception,
    'raise'                 : craft_raise,
    'format'                : craft_format,
}

__jit__ = {
	'Program'               : None
}

'''__code__ = {                : None
	
}'''
