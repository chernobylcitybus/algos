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

    anagrams__unexpected = [
        (dict(), [TypeError, "Input not a valid list type"]),
        ([dict()], [TypeError, "Elements of input not all string type"]),
    ]
    """
    Test cases for :meth:`algosrest.client.text.TextREST.anagrams`, testing that it raises HTTPExceptions for
    unexpected input.
    """


class TestText:
    """
    Test the REST client requests for text algorithms. Care needs to be taken in cases of two or more worker processes,
    to ensure that the expected output is not subject to race conditions when patching with :class:`.MockHTTPConnection`
    In the simple case of testing the requests with a single worker process, it is permissible to use the buffer with
    a :class:`bytes` or :class:`list` value. In the case of two or more worker processes (where there is more than one
    chunk for the :class:`ProcessPool`), we must use the dictionary which stores the expected json response with the
    input json as its key. This allows workers to safely read the expected outputs and not be subject to a race
    condition, as in the case of popping from a list of expected responses in a sequential fashion.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, test_input, expected):
        """
        Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams`.

        We use the :class:`.MockHTTPConnection` to patch the outgoing requests and the incoming responses from the
        server.
        """
        # Create a RequestPool instance which will carry out our requests.
        req = RequestPool(2, "localhost", 8081)

        # Create the TextRest instance which offers our convenience interface to the text algorithms.
        text_rest = TextRest(req)

        # Create test input string.
        str_list = [" ".join(list(x)) for x in test_input]

        # Set the output of the MockHTTPConnection to be the expected response.
        # If just one process worker is used
        if len(expected) == 1:
            # #e are using using a list to store the output of successive requests.
            MockHTTPConnection.buffer = [json.dumps(x).encode() for x in expected]
        # Otherwise, we are using more than one worker
        else:
            # We need to give the buffer as a dict so that the parallel processes can find the correct input given
            # the inputs to the request.
            buffer = dict()
            # This is the data the server receives in the body of the request.
            buffers = [bytes(json.dumps({"input": x}).encode("utf-8")) for x in str_list]
            for i in range(len(buffers)):
                # We us the input data as the key and output data as the expected result. We technically
                # should use an actual result returned by anagrams, but the expected result is just
                # the sorted version of that.
                buffer.update({buffers[i]: bytes(json.dumps(expected[i]).encode("utf-8"))})

            MockHTTPConnection.buffer = buffer

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

        # Check that the result is as expected.
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

