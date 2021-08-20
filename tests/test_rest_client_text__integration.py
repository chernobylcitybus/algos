"""
Test the REST client with the algorithms in :mod:`algos.text` .
"""
import json
import pytest
import http.client
from unittest.mock import patch
from algosrest.client.parallel import RequestPool
from algosrest.client.text import TextRest
from .conftest import MockHTTPConnection


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
            [{'the', 'car', 'can', 'caused', 'a', 'and', 'during', 'cried', 'by', 'its', 'rat', 'bowel', 'drinking',
             'elbow', 'bending', 'that', 'while', 'an', 'thing', 'cider', 'like', 'pain', 'cat', 'which', 'in', 'this',
             'act', 'below', 'is', 'night', 'arc'}],
            [[['act', 'cat'], ['arc', 'car'], ['below', 'bowel', 'elbow'], ['cider', 'cried'], ['night', 'thing']]]
        ),
        (
            [{"elbow", "below", "bowel"}],
            [[['below', 'bowel', 'elbow']]]
        ),
        (
            [{""}],
            [[]]
        ),
        (
            [
                {'the', 'car', 'can', 'caused', 'a', 'and', 'during', 'cried', 'by', 'its', 'rat', 'bowel', 'drinking',
                 'elbow', 'bending', 'that', 'while', 'an', 'thing', 'cider', 'like', 'pain', 'cat', 'which', 'in',
                 'this', 'act', 'below', 'is', 'night', 'arc'},
                {"elbow", "below", "bowel", "arc", "car"}
             ],
            [
                [['act', 'cat'], ['arc', 'car'], ['below', 'bowel', 'elbow'], ['cider', 'cried'], ['night', 'thing']],
                [['arc', 'car'], ['below', 'bowel', 'elbow']]
            ]
        ),
    ]
    """
    Test cases for :meth:`algosrest.client.text.TextRest.anagrams`, testing that it functions correctly for 
    expected inputs. The test cases are as follows
    
    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | 1 worker, many anagrams              | Check if multiple anagrams are identified in the results.            |
    +--------------------------------------+----------------------------------------------------------------------+
    | 1 worker, 1 set of anagrams          | Check if a single result is returned correctly.                      |
    +--------------------------------------+----------------------------------------------------------------------+
    | 1 worker, empty set                  | Check that we get back an empty result set.                          |
    +--------------------------------------+----------------------------------------------------------------------+
    | 2 workers, many sets of anagrams     | Check if batch requests work.                                        |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """


class TestText:
    """
    This class is needed in order to use the :func:`rest_server_fixture` to conduct integration tests against the
    current :mod:`algosrest.server` version. The tests herein are for the text based algorithms found in
    :mod:`algos.text` .
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, rest_server_fixture, test_input, expected):
        """
        Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams`.
        We make use of the :func:`rest_server_fixture` to spawn an actual instance of the server to test the client
        against.
        """
        # Create a RequestPool instance which will carry out our requests.
        req = RequestPool(2, "localhost", 8081)

        # Create the TextRest instance which offers our convenience interface to the text algorithms.
        text_rest = TextRest(req)

        # Create test input string.
        str_list = [" ".join(list(x)) for x in test_input]

        anagrams_found = text_rest.anagrams(str_list)

        # Sort the result to compare to expected value.
        anagrams_found = [[sorted(y) for y in x] for x in anagrams_found]
        anagrams_found = [sorted(x) for x in anagrams_found]
        anagrams_found.sort()

        # Clean up the RequestPool workers.
        req.shutdown()

        assert anagrams_found == expected

