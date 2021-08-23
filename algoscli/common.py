"""
Common functions and classes to support command line processing.
"""
import argparse
from typing import NamedTuple, Optional, Any


class Function(NamedTuple):
    """
    A :class:`typing.NamedTuple` that stores information for :mod:`argparse` to process command line arguments.
    Each :class:`Function` maps to a single command line argument. These make up the base command line API.

    As an example, suppose we want to create a subcommand to transpose a matrix. We could set up a subcommand
    representing this function as follows:

    >>> from algoscli.common import Function
    >>> name = "transpose"
    >>> help = "Transpose the input matrix."
    >>> args = [("MatIn", "Path to input"), ("MatOut", "Path to output")]
    >>> transpose_cli = Function(name=name, help=help, args=args)
    >>> transpose_cli
    Function(name='transpose', help='Transpose the input matrix.', args=[('MatIn', 'Path to input'), ('MatOut', 'Path \
to output')])

    This would then be added to a :class:`Component` for argparse to process. The subcommand would then require two
    positional arguments (after the name of the subcommand) called MatIn and MatOut. It will raise an error if
    they are not present on the invoked command line.
    """
    name: str
    """The name of the command line function. This is used as the second argument on the command line."""

    help: str
    """Some help text for the ``--help`` option :mod:`argparse` uses. This help described what the function does."""

    args: Optional[list[tuple[str, str]]] = None
    """An optional list of arguments and associated help text for the given command line function. The arguments
    given here will be checked by argparse and an error raised if they are note supplied."""


class Component(NamedTuple):
    """
    A :class:`typing.NamedTuple` that stores information for :mod:`argparse`. Each Component houses multiple
    command line :class:`Function` s and represents the logical grouping of algorithms.

    Each of the Components resolves into a command line function grouping e.g. algos-text/algos-text.exe.
    These contain their own titles, descriptions and help files when examining the help files generated
    by :mod:`argparse` .

    Continuing our matrix example, we create a component to service the ``algos-matrix`` command line group as follows:

    >>> from algoscli.common import Component
    >>> title = "matrix"
    >>> description = "Matrix related operations"
    >>> help = "Common matrix operations."
    >>> functions = [transpose_cli]
    >>> matrix_component = Component(title=title, description=description, help=help, functions=functions)
    >>> matrix_component
    Component(title='matrix', description='Matrix related operations', help='Common matrix operations.', \
functions=[Function(name='transpose', help='Transpose the input matrix.', args=[('MatIn', 'Path to input'), \
('MatOut', 'Path to output')])])

    :class:`Component` 's are not normally used directly, but are instead created by :func:`parse_arguments` .
    """
    title: str
    """The title of the grouping."""

    description: str
    """A description of what the grouping does."""

    help: str
    """A help file for use by :mod:`argparse` ``--help`` option."""

    functions: list[Function]
    """A list of :class:`Function` s that make up the grouping. These represent the actual command line functions
    that are called. A :class:`Component` by itself does nothing."""


def parse_arguments(
        group: str,
        description: str,
        help: str,
        component_functions: dict[str, list[Function]]
) -> argparse.Namespace:
    """
    The main function for parsing command line arguments. It takes arguments that are used to build a :class:`Component`
    for use by :mod:`argparse`.

    It serves to service argument parsing of command line scripts set up with the console_scripts parameter in
    setup.py. It can be used in general, however, to parse command line inputs.

    Continuing with the matrix example, the code could be used as follows

    >>> import argparse
    >>> from algoscli.common import parse_arguments
    >>> def matrix():
    ...     args: argparse.Namespace = parse_arguments(
    ...         "matrix",
    ...         "Matrix related operations",
    ...         "Common matrix operations.",
    ...         {"matrix": [transpose_cli]}
    ...     )
    ... )

    The result ``args`` will then be a Namespace. You can use :code:`args.MatIn` or :code:`args.MatOut` to then
    access the given command line options. This will work when matrix function is mapped to an appropriate
    console script in setup.py.

    :param str group: The title of the command line grouping.
    :param str description: What the grouping aims to do in general.
    :param str help: A help file for use with :mod:`argparse` .
    :param dict[str, list[Function]] component_functions: A dictionary mapping the group name to a list of its
                                                          constituent :class:`Function` s. For speed we pass a
                                                          dictionary that just has the component functions for the
                                                          group, though we can use a dictionary that contains all
                                                          component functions.
    :rtype: argparse.Namespace
    :return: Namespace of parsed command line arguments.
    """

    # Get the component functions for the particular group.
    functions: list[Function] = component_functions[group]

    # Create a Component to represent all the group's information for argparse.
    component: Component = Component(
        title=group,
        description=description,
        help=help,
        functions=functions
    )

    # Generate an instance of the argument parser for use with current command line.
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    # Create a subparser to handle the component functions.
    subparsers: Any = parser.add_subparsers(
        title=component.title,
        description=component.description,
        help=component.help
    )

    # For each component function
    for func in component.functions:
        # Add the function to the subparsers, with help text for argparse.
        func_parser: Any = subparsers.add_parser(
            func.name,
            help=func.help
        )

        # If the function had arguments
        if func.args is not None:
            # For each argument
            for arg in func.args:
                # Add the argument to the function parser, with help text.
                # If we are dealing with an optional argument
                if arg[0].startswith("--"):
                    # We only support optional arguments that just are True or False.
                    func_parser.add_argument(
                        arg[0],
                        action=argparse.BooleanOptionalAction,
                        help=arg[1]
                    )
                # Otherwise we have a positional argument
                else:
                    # We don't need to add an action in this case.
                    func_parser.add_argument(
                        arg[0],
                        help=arg[1]
                    )

    # Parse the arguments and return a namespace of the parsed arguments.
    return parser.parse_args()
