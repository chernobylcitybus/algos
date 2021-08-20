"""
This module yields the REST entry points to the algorithms in :mod:`algosrest.server.text` . The :class:`TextRest` class
corresponds to the ``/text`` REST endpoint. The list of methods and their purposes are described below.

+--------------------------------+-------------------------------------------------------------------------------+
| Name                           | purpose                                                                       |
+================================+===============================================================================+
| :meth:`.TextRest.anagrams`     | Finds all the anagrams in the given input.                                    |
+--------------------------------+-------------------------------------------------------------------------------+

"""
import json
import math
from algosrest.client.parallel import RequestPool, RequestInfo


class TextRest:
    """
    Text class for REST client.

    :ivar RequestPool req: A :class:`.RequestPool` object to use for the requests.
    """
    def __init__(self, req: RequestPool):
        """
        Initializes the class with the RequestPool with which to make the requests.

        :param RequestPool req: A :class:`.RequestPool` object to use for the requests.
        """
        self.req = req

    def anagrams(self, str_list: list[str]) -> list[list[str]]:
        """
        Make a request to the :meth:`algosrest.server.text.TextRest.anagrams` handler. This uses the endpoint
        ``/text/anagrams`` .

        :param str_list: A list of strings to make a batch request.
        :return: The anagrams found in the inputs.
        """
        # Check that we have a valid list instance.
        if not isinstance(str_list, list):
            raise TypeError("Input not a valid list type")

        # Check that all the elements of the list are of string type.
        if not all([isinstance(x, str) for x in str_list]):
            raise TypeError("Elements of input not all string type")

        # Return the number of workers in the pool.
        n_workers: int = self.req.pool.n_workers

        # Create a list of RequestInfo with the list of strings.
        req_data = [RequestInfo(endpoint="/text/anagrams", method="POST", data={"input": x}) for x in str_list]

        # Chunk the list of RequestInfo using the length of the ceiling of the length of the list divided by
        # the number of workers in the pool. This should evenly distribute the work with some remainder in an
        # additional list in the worst case.
        req_infos = list(self.req.chunks(
            req_data,
            int(math.ceil(len(req_data) / n_workers))
        ))

        # Perform the request and read the results.
        results: list[list[tuple[str, float, str]]] = list(self.req.batch_request(req_infos))

        # Create a variable to linearly store the results of the requests in the same order as the original
        # input list.
        results_clean: list[list[str]] = list()

        # Iterate through the results, which are in the form of a list of lists, and load the extracted JSON
        # strings. We append it to the linear result set.
        for result in results:
            for sub_result in result:
                results_clean.append(json.loads(sub_result[0]))

        return results_clean
