"""
Test the REST server's responses for the text algorithms in :mod:`algos.text` . This module depends on the use of
the pytest fixture rest_server_fixture which does the set-up/teardown for an actual instance of the rest server.
"""
import textwrap
import subprocess
import json
import pytest


class DataText:
    """
    Test data for text based algorithms. Contains lists of tuples of the form (inputs, expected). The data for the
    following functions is contained within

    +--------------------------------------+
    | anagrams                             |
    +--------------------------------------+

    """
    anagrams__expected = [
        (
            {'the', 'car', 'can', 'caused', 'a', 'and', 'during', 'cried', 'by', 'its', 'rat', 'bowel', 'drinking',
             'elbow', 'bending', 'that', 'while', 'an', 'thing', 'cider', 'like', 'pain', 'cat', 'which', 'in', 'this',
             'act', 'below', 'is', 'night', 'arc'},
            [['act', 'cat'], ['arc', 'car'], ['below', 'bowel', 'elbow'], ['cider', 'cried'], ['night', 'thing']]
        ),
        (
            {"elbow", "below", "bowel"},
            [['below', 'bowel', 'elbow']]
        ),
        (
            {""},
            []
        )
    ]
    """
    Test cases for :meth:`algosrest.server.text.TextREST.anagrams`, testing that it functions correctly for 
    expected inputs. The test cases are as follows
    
    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | many anagrams                        | Check if multiple anagrams are identified in the results.            |
    +--------------------------------------+----------------------------------------------------------------------+
    | 1 set of anagrams                    | Check if a single result is returned correctly.                      |
    +--------------------------------------+----------------------------------------------------------------------+
    | empty set                            | Check that we get back an empty result set.                          |
    +--------------------------------------+----------------------------------------------------------------------+
    """

    anagrams__unexpected = [
        ({"noinput": "elbow below bowel"}, (400, {"detail": "'input' not found"})),
        ({"input": 1}, (400, {"detail": "Unsupported Type"}))
    ]
    """
    Test cases for :meth:`algosrest.server.text.TextREST.anagrams`, testing that it raises HTTPExceptions for
    unexpected input.The test cases are as follows
    
    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | no input key found                   | Check that we send a 400 response if the "input" key was not found.  |
    +--------------------------------------+----------------------------------------------------------------------+
    | incorrect input type                 | Check that we send a 400 response when we receive incorrect input.   |
    +--------------------------------------+----------------------------------------------------------------------+
    """


class TestText:
    """
    We use the pytest fixture rest_server_fixture which has class scope, so we need to group all our code together into one
    class, to prevent repeatedly starting up and shutting down the fastapi server, which can greatly increase
    the runtime of the tests.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, test_input, expected, rest_server_fixture):
        """
        Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams`
        """
        # Make the request and get the response.
        post_request = textwrap.dedent(
            f"""
            curl -s --header "Content-Type: application/json"   --request POST   
            --data '{json.dumps({"input": " ".join(list(test_input))})}'   http://localhost:8081/text/anagrams
            """
        ).replace("\n", " ")
        post_output: bytes = subprocess.check_output(post_request, shell=True)

        # Sort the output into the order the expected response expects.
        anagrams_found = json.loads(post_output.decode())
        anagrams_found = [sorted(x) for x in anagrams_found]
        anagrams_found.sort()

        assert anagrams_found == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__unexpected,
        ids=[repr(v) for v in DataText.anagrams__unexpected]
    )
    def test_anagrams__unexpected(self, test_input, expected, rest_server_fixture):
        """
        Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams`
        """
        # Make the request with the invalid input data
        post_request = textwrap.dedent(
            f"""
            curl -s --header "Content-Type: application/json"   --request POST   
            --data '{json.dumps(test_input)}'   http://localhost:8081/text/anagrams
            """
        ).replace("\n", " ")
        post_output: bytes = subprocess.check_output(post_request, shell=True)

        # Read back the error from the shell output
        error = json.loads(post_output.decode())

        # Check if the reason for the error is as expected.
        assert error == expected[1]