import argparse
import pytest
import sys


def create_parser():
    """
    Parses arguments from the command line
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-u', action='store_true', default=False,
                        help='Run unit tests')
    parser.add_argument('-i', action='store_true', default=False,
                        help='Run integration tests')
    return parser


def run_unit_tests():
    """
    Runs just the unit tests
    :return: integer result
    """
    print("RUNNING UNIT TESTS")
    return pytest.main(["unit_tests"])


def run_integration_tests():
    """
    Runs just the integration tests
    :return: integer result
    """
    print("RUNNING INTEGRATION TESTS")
    return pytest.main(["integration_tests"])


def run_tests():
    """
    Runs the api test suite using pytest
    :return: 0 if all tests pass, 1 otherwise
    """
    # Parse the command line to get the command line options
    parser = create_parser()
    args = parser.parse_args()

    # Initialize result variables to 0, indicating success
    unit_result = 0
    int_result = 0

    # If -u was provided, run the unit tests
    if args.u:
        unit_result = run_unit_tests()
        print()

    # If -i was provided, run the integration tests
    elif args.i:
        int_result = run_integration_tests()

    # If neither flags were provided, run unit and integration tests
    else:
        unit_result = run_unit_tests()
        print()
        int_result = run_integration_tests()

    if unit_result or int_result:
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
