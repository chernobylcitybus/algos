"""
Module that provides REST handlers for text based algorithms. These algorithms are found in :mod:`algos.text`.
"""
import logging
from typing import Any, Optional
from algos.text import anagrams
from fastapi import HTTPException

# Set up the logger for the module
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s [%(lineno)d] %(message)s "
)


class TextREST:
    """
    Class that contains all text based algorithms' REST implementations.

    :ivar logging.Logger logger: The logger for this class.
    """
    def __init__(self):
        """
        Initialize the logger for the class.
        """
        # Get the logger
        self.logger: logging.Logger = logging.getLogger("algosrest.text")

    def anagrams(self, json_request: dict[str, Any]) -> list[list[str]]:
        """
        REST handler for :func:`algos.text.anagrams` . The expected input is a dictionary with the key 'input',
        and a string as the value. Handles the ``/text/anagrams`` endpoint. With the REST server started, and ``curl``
        installed, you can try a command of the form

        .. code-block:: bash

           $ curl --header "Content-Type: application/json" --request POST \\
               --data '{"input": "below on the elbow is the bowel"}' http://localhost:8081/text/anagrams
           [["below","bowel","elbow"]]

        :param dict[str, Any] json_request: The loaded JSON request.
        :rtype: list[list[str]]
        :return: The anagrams found in the input sentence.
        """
        # Extract input value from response.
        input_value: Optional[Any] = json_request.get("input", None)

        # Raise error if no "input" key found.
        if input_value is None:
            self.logger.critical("anagrams - 'input' not found")
            raise HTTPException(status_code=400, detail="'input' not found")

        # If the input is not a string, raise a TypeError.
        if not isinstance(input_value, str):
            self.logger.critical("anagrams - Unsupported Type " + str(type(input_value)))
            raise HTTPException(status_code=400, detail="Unsupported Type")

        # For typing sake, be explicit that we are now working with a string.
        input_str: str = input_value

        # Turn the input string into a set of words.
        word_set: set[str] = set(input_str.split())

        # If the input is empty, just pass in the empty set.
        if len(word_set) == 0:
            word_set = {""}

        # Find the anagrams.
        result: list[list[str]] = anagrams(word_set)

        return result
