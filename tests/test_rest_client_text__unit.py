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
    Test cases for :meth:`algosrest.client.text.TextREST.anagrams` ., testing that it functions correctly for 
    expected inputs.
    """

    anagrams__unexpected = [
        (dict(), [TypeError, "Input not a valid list type"]),
        ([dict()], [TypeError, "Elements of input not all string type"]),
    ]
    """
    Test cases for :meth:`algosrest.client.text.TextREST.anagrams` ., testing that it raises HTTPExceptions for
    unexpected input.
    """


class TestText:
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, test_input, expected):
        """
        Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams` .
        """
        # Create a RequestPool instance which will carry out our requests.
        req = RequestPool(2, "localhost", 8081)

        # Create the TextRest instance which offers our convenience interface to the text algorithms.
        text_rest = TextRest(req)

        # Create test input string.
        str_list = [" ".join(list(x)) for x in test_input]

        # Set the output of the MockHTTPConnection to be the expected response. In this case, we are using using a list
        # to store the output of successive requests.
        MockHTTPConnection.buffer = [json.dumps(x).encode() for x in expected]

        # Patch the connection to before we perform the request so it received our mock data.
        with patch.object(http.client, "HTTPConnection", MockHTTPConnection):
            # Perform the request
            anagrams_found = text_rest.anagrams(str_list)

        # Sort the result to compare to expected value.
        anagrams_found = [[sorted(y) for y in x] for x in anagrams_found]
        anagrams_found = [sorted(x) for x in anagrams_found]
        anagrams_found.sort()

        # Clean up the RequestPool workers.
        req.shutdown()

        assert anagrams_found == expected


    @pytest.mark.parametrize(
        "test_input,error",
        DataText.anagrams__unexpected,
        ids=[repr(v) for v in DataText.anagrams__unexpected]
    )
    def test_anagrams__unexpected(self, test_input, error):
        """
        Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams` .
        """
        # Create a RequestPool instance which will carry out our requests.
        req = RequestPool(2, "localhost", 8081)

        # Create the TextRest instance which offers our convenience interface to the text algorithms.
        text_rest = TextRest(req)

        with pytest.raises(error[0]) as excinfo:
            anagrams_found = text_rest.anagrams(test_input)

        # Clean up the RequestPool workers.
        req.shutdown()

        assert excinfo.match(error[1])

