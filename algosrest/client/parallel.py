"""
This module supports true parallelism through multiprocessing. Since threading is still subject to the Global
Interpreter Lock (GIL), we can instead offload the requests to multiple processes which are free of this constraint.
We use the :class:`concurrent.futures.ProcessPoolExecutor` to submit our work to. Work is in the form of lists or
list of lists of :class:`RequestInfo` 's, depending on which methods are called. :meth:`RequestPool.batch_request`
accepts list of lists, whereas :meth:`RequestPool.single_request` just accepts a list.

Both methods submit the work to the ProcessPoolExecutor, with :meth:`RequestPool.batch_request` mapping all the
work simultaneously, and distributing it amongst the processes.
"""
from concurrent import futures
import time
import json
import http.client

from typing import Optional, Any, Union
from collections.abc import Iterator, Callable


class RequestInfo:
    """
    The main class to represent a request.

    :ivar str endpoint: The endpoint to make the request to.
    :ivar str method: The HTTP method to call.
    :ivar Optional[dict[str, Any]] data: Data for POST requests.

    .. automethod:: __init__
    .. automethod:: __repr__
    .. automethod:: __eq__
    """
    def __init__(self, endpoint: str, method: str, data: Optional[dict[str, Any]] = None) -> None:
        """
        Initializes the RequestInfo object. The inputs go the a variety of type and value checks.

        :raises TypeError: If endpoint is not a string.
        :raises TypeError: If method is not a string.
        :raises ValueError: If method is not one of GET or POST.
        :raises TypeError: If data is not a dictionary.
        :raises ValueError: If no data was given for POST request.
        :raises ValueError: If data was given for GET request.
        :param str endpoint: The endpoint you want to make a request to e.g. /text/anagrams
        :param str method: The method you want to use (POST if you are sending data, GET if you are not)
        :param Optional[dict[str, Any]] data: Optional data to send with POST requests.
        """
        # Check that the endpoint was given as a string.
        if not isinstance(endpoint, str):
            raise TypeError("Invalid type for endpoint - " + str(type(endpoint)))

        # Check that the method was given as a string.
        if not isinstance(method, str):
            raise TypeError("Invalid type for method - " + str(type(method)))

        # Change method to uppercase
        method_upper = method.upper()

        # Check that method is one of "GET" or "POST".
        if method_upper not in {"GET", "POST"}:
            raise ValueError("Invalid value for method. Must be 'GET' or 'POST'")

        # Check that the data, if given, is in the form of a dictionary.
        if data is not None:
            if not isinstance(data, dict):
                raise TypeError("Invalid type for data - " + str(type(method)))

        # Check that we have data for our "POST" request.
        if data is None and method_upper == "POST":
            raise ValueError("No data given for POST request")

        # Check that data is not supplied for "GET"
        if data is not None and method_upper == "GET":
            raise ValueError("Data supplied for GET request")

        self.endpoint: str = endpoint
        self.method: str = method_upper
        self.data: Optional[dict[str, Any]] = data

    def __repr__(self) -> str:
        """
        A nicer representation to read, though one cannot copy it directly into the interpreter.
        :return: String representation.
        """
        return f"RequestInfo({self.endpoint}, {self.method}, {self.data})"

    def __eq__(self, other) -> bool:
        """
        Allow tests for equality. This function checks that the endpoints, methods and data of the two objects
        being compared are all equal.
        """
        if not isinstance(other, RequestInfo):
            return False

        return (self.endpoint == other.endpoint) and (self.method == other.method) and (self.data == other.data)


class ProcessPool:
    """
    This is where the multiprocessing of the client comes from. We use a :class:`concurrent.futures.ProcessPoolExecutor`
    to execute requests concurrently.
    """
    def __init__(self, n_workers: int) -> None:
        """
        Creates the :class:`concurrent.futures.ProcessPoolExecutor` with the given number of workers.

        :param n_workers: Number of processes to spawn for this worker pool.
        """
        # Assign n_workers to instance variable for future reference.
        self.n_workers: int = n_workers

        # Create the Process Pool that will do our work.
        self.executor: futures.ProcessPoolExecutor = futures.ProcessPoolExecutor(
            max_workers=self.n_workers
        )

    def batch(
            self,
            func: Callable[[list[RequestInfo], str, int], list[tuple[str, float, str]]],
            *iterables: Union[list[list[RequestInfo]], Any]
    ) -> Iterator[list[tuple[str, float, str]]]:
        """
        Performs a batch request. The idea here is that you have a list of lists of :class:`RequestInfo` 's, each
        to the same host. Each worker will take one of the equally distributed lists, and track the responses
        for that particular list. Multiple workers will also just consume the inputs, if there are more than one
        input per worker.

        :meth:`RequestPool.chunks` assists with splitting a single list of :class:`RequestInfo` 's into a list of
        lists of :class:`RequestInfo` 's.

        :param Callable[[list[RequestInfo], str, int], list[tuple[str, float, str]]] func: :meth:`RequestPool.request`
        :param list[list[RequestInfo]] iterables: This list of requests you would like to make.
        :return: A iterator which produces a list with as many elements as workers, with the results of their
                 individual batch of requests.
        """
        results: Iterator[list[tuple[str, float, str]]] = self.executor.map(func, *iterables)

        return results

    def single(
            self,
            func: Callable[[list[RequestInfo], str, int], list[tuple[str, float, str]]],
            *arg: Union[list[RequestInfo], Any]
    ) -> futures.Future[list[tuple[str, float, str]]]:
        """
        Submit a single request to the executor pool.

        :param Callable[[list[RequestInfo], str, int], list[tuple[str, float, str]]] func: :meth:`RequestPool.request`
        :param list[RequestInfo] arg: This list of requests you would like to make.
        :return: A futures instance with the results, their timings and the requested endpoint.
        """
        future: futures.Future[list[tuple[str, float, str]]] = self.executor.submit(func, *arg)

        return future

    def shutdown(self) -> None:
        """
        Shutdown the process pool for cleanup.
        """
        self.executor.shutdown(wait=True)


class RequestPool:
    """
    A higher level interface to :class:`ProcessPool` that contains the HTTP functionality to make the requests.

    :ivar ProcessPool pool: The process pool that will be used to make the requests.

    .. automethod:: __init__
    """
    def __init__(self, n_workers: int, hostname: str, port: int):
        """
        Initializes the process pool with n_workers.

        :raises TypeError: If hostname is not a string.
        :raises TypeError: If port is not an int.
        :param n_workers: The number of processes to create.
        """
        # Check that n_workers is an integer.
        if not isinstance(n_workers, int):
            raise TypeError("Number of workers not given as int")

        # Check that the hostname is a string.
        if not isinstance(hostname, str):
            raise TypeError("Hostname not given as string")

        # Check that the port is an integer.
        if not isinstance(port, int):
            raise TypeError("Port not given as int")

        # Check that the hostname is not empty.
        if hostname == "":
            raise ValueError("Blank hostname given")

        # Check that we have a valid port.
        if port < 1:
            raise ValueError("Invalid port number given")
        
        self.pool: ProcessPool = ProcessPool(n_workers)
        self.hostname: str = hostname
        self.port: int = port

    @staticmethod
    def request(req_infos: list[RequestInfo], hostname: str, port: int) -> list[tuple[str, float, str]]:
        """
        The code to perform the HTTP request. Can be used directly, but used to map to :meth:`RequestPool.batch_request`
        and :meth:`RequestPool.single_request`.

        :param req_infos: The list of requests.
        :param hostname: The hostname of the machine to which to make these requests (e.g. "localhost")
        :param port: The port on the host that the :mod:`algosrest.server` is listening on.
        :return: The results with their timings and endpoints.
        """
        # Check if req_infos is indeed a list.
        if not isinstance(req_infos, list):
            raise TypeError("Unsupported Type for Input List")

        # Check if all elements in req_infos are of type RequestInfo.
        if not all([isinstance(x, RequestInfo) for x in req_infos]):
            raise TypeError("Unsupported Type for Input Elements")

        # Create an empty list to store the results.
        results: list[tuple[str, float, str]] = list()

        # Create a connection to the host with which to perform the requests.
        conn: http.client.HTTPConnection = http.client.HTTPConnection(hostname, port)

        # Force the keep-alive header to re-use the connection.
        headers: dict[str, str] = {
            "Connection": "keep-alive",
            "Host": f"{hostname}:{port}",
            "User-Agent": "algosrestclient/0.1.0",
            "Accept": "*/*"
        }

        # Declare the type of the iterator.
        req_info: RequestInfo

        # For each request in the list of requests.
        for req_info in req_infos:
            # Get a start time to calculate how long the request takes.
            start: float = time.time()

            # If there was no data supplied
            if req_info.data is None:
                # We are performing a GET request.
                conn.request(
                    req_info.method,
                    req_info.endpoint,
                    headers=headers
                )
            # Otherwise we are performing a POST request.
            else:
                # We need to encode the JSON encoded dictionary as a bytes object to send it with the body of the
                # post request.
                encoded_args: bytes = bytes(json.dumps(req_info.data).encode("utf-8"))

                # Add some required headers.
                post_headers: dict[str, str] = {
                    "Content-Length": str(len(encoded_args)),
                    "Content-type": "application/json",
                    "Host": f"{hostname}:{port}",
                    "User-Agent": "algosrestclient/0.1.0",
                    "Accept": "*/*",
                    "Connection": " keep-alive"
                }

                # Make the POST request.
                conn.request(
                    req_info.method,
                    req_info.endpoint,
                    body=encoded_args,
                    headers=post_headers
                )

            # Read the response from the connection as a string.
            response: http.client.HTTPResponse = conn.getresponse()
            response_data: str = response.read().decode("utf-8")

            # End our timer.
            end: float = time.time()

            # Append the response data, the time the request took and the endpoint and append it to the results
            # list.
            results.append((response_data, end - start, req_info.endpoint))

        # Clean up the connection.
        conn.close()

        return results

    def batch_request(self, req_infos: list[list[RequestInfo]]) -> Iterator[list[tuple[str, float, str]]]:
        """
        Performs a batch HTTP request.

        :param list[list[RequestInfo]] req_infos: The requests to make. Each list element is assigned to a parallel
                                                  process.
        :return: An iterator that yields the results of the requests.
        """
        req_len = len(req_infos)
        hostnames = [self.hostname] * req_len
        ports = [self.port] * req_len

        results: Iterator[list[tuple[str, float, str]]] = self.pool.batch(self.request, req_infos, hostnames, ports)
        return results

    def single_request(self, req_info: RequestInfo) -> futures.Future[list[tuple[str, float, str]]]:
        """
        Submits a single request to the request pool.

        :param req_info: A single request.
        :return: The result of the request with its timings and endpoint.
        """
        results: futures.Future[list[tuple[str, float, str]]] = self.pool.single(self.request, [req_info])

        return results

    @staticmethod
    def chunks(array: list[RequestInfo], n: int) -> Iterator[list[RequestInfo]]:
        """
        A function that takes all requests and splits them into multiple lists of requests for parallel processing.
        Yields an :class:`typing.Iterator` to generate sub lists.

        :param list[RequestInfo] array: A list of :class:`RequestInfo` s to be chunked.
        :param n: Number of chunks to yield.
        :rtype: typing.Iterator[list[RequestInfo]]
        :return: A list of lists of :class:`RequestInfo` s to be used with multiprocessing connections to Interactive
                 Brokers.
        """
        # Check that n is of the correct type.
        if not isinstance(n, int):
            raise TypeError("Invalid input type for n - " + str(type(n)))

        # Check that the array is of the correct type.
        if not isinstance(array, list):
            raise TypeError("Invalid input type for array - " + str(type(array)))

        # Check that the array elements are of the correct type.
        if not all([isinstance(x, RequestInfo) for x in array]):
            raise TypeError("Invalid input type for array element")

        # Declare the iterators.
        i: int

        # Yield the array slices, one by one.
        for i in range(0, len(array), n):
            yield array[i:i+n]

    def shutdown(self) -> None:
        """Shut down the request pool"""
        self.pool.shutdown()
