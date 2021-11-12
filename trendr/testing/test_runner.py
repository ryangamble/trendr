import argparse
import os
import pytest
import sys

from pathlib import Path


TESTING_DIR = Path(__file__).parent.resolve()


def create_parser():
    """
    Parses arguments from the command line
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-u", action="store_true", default=False, help="Run unit tests"
    )
    parser.add_argument(
        "-i", action="store_true", default=False, help="Run integration tests"
    )
    parser.add_argument(
        "-v", action="store_true", default=False, help="Verbose output"
    
    )
    return parser


def load_env_files():
    """
    Reads all environment variables files in trend/.env/ and sets them locally
    :return:
    """
    env_path = TESTING_DIR.parent.parent.resolve() / ".env"
    env_files = [filename for filename in env_path.iterdir()]
    for env_file in env_files:
        with env_file.open() as open_file:
            for line in open_file.readlines():
                env_var_parts = line.split("=")
                os.environ[env_var_parts[0].strip()] = env_var_parts[1].strip()


def run_unit_tests(verbose=False):
    """
    Runs just the unit tests
    :return: integer result
    """
    print("RUNNING UNIT TESTS")
    args = [str(TESTING_DIR / "unit_tests")]
    if verbose:
        args.append("-s")
    return pytest.main(args)


def run_integration_tests(verbose=False):
    """
    Runs just the integration tests
    :return: integer result
    """
    print("RUNNING INTEGRATION TESTS")
    args = [str(TESTING_DIR / "integration_tests")]
    if verbose:
        args.append("-s")
    return pytest.main(args)


def run_tests():
    """
    Runs the api test suite using pytest
    :return: 0 if all tests pass, 1 otherwise
    """
    # Parse the command line to get the command line options
    parser = create_parser()
    args = parser.parse_args()

    # Load environment variables for the tests that need them (i.e. twitter connector tests)
    load_env_files()

    # Initialize result variables to 0, indicating success
    unit_result = 0
    int_result = 0

    # If -u was provided, run the unit tests
    if args.u:
        unit_result = run_unit_tests(args.v)
        print()

    # If -i was provided, run the integration tests
    elif args.i:
        int_result = run_integration_tests(args.v)

    # If neither flags were provided, run unit and integration tests
    else:
        unit_result = run_unit_tests(args.v)
        print()
        int_result = run_integration_tests(args.v)

    if unit_result or int_result:
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
