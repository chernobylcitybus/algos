"""
Test the REST server's responses for the text algorithms in :mod:`algos.text` .
"""
import pytest
from algosrest.server.main import app, anagrams

from fastapi import Response
from fastapi.testclient import TestClient

client: TestClient = TestClient(app)


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
    Test cases for :meth:`algosrest.server.text.TextREST.anagrams` ., testing that it functions correctly for 
    expected inputs.
    """

    anagrams__unexpected = [
        ({"noinput": "elbow below bowel"}, (400, {"detail": "'input' not found"})),
        ({"input": 1}, (400, {"detail": "Unsupported Type"}))
    ]


@pytest.mark.parametrize(
    "test_input,expected",
    DataText.anagrams__expected,
    ids=[str(v) for v in range(len(DataText.anagrams__expected))]
)
def test_anagrams__expected(test_input, expected):
    """
    Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams` .

    :param test_input:
    :param expected:
    :return:
    """
    # Make the request and get the response.
    response: Response = client.post("/text/anagrams", json={"input": " ".join(list(test_input))})

    # Assign json response to anagrams_found.
    anagrams_found = response.json()

    # Sort the result to compare to expected value.
    anagrams_found = [sorted(x) for x in anagrams_found]
    anagrams_found.sort()

    assert anagrams_found == expected


@pytest.mark.parametrize(
    "test_input,expected",
    DataText.anagrams__unexpected,
    ids=[repr(v) for v in DataText.anagrams__unexpected]
)
def test_anagrams__unexpected(test_input, expected):
    """
    Test the ``/text/anagrams`` endpoint with expected inputs. Uses :meth:`algosrest.server.text.TextREST.anagrams` .

    :param test_input:
    :param expected:
    :return:
    """
    response: Response = client.post("/text/anagrams", json=test_input)
    anagrams_found = response.json()
    print(response.status_code)
    print(anagrams_found)

    assert response.status_code == expected[0]
    assert anagrams_found == expected[1]

