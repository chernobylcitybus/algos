"""
The following are implementations of algorithms that primarily operate on text. The list of implementations and their
purposes are

+--------------------------------------+-------------------------------------------------------------------+
| function                             | purpose                                                           |
+======================================+===================================================================+
| :func:`.anagrams`                    | Given an input word set, it returns a list of lists of words      |
|                                      | which are anagrams of each other.                                 |
+--------------------------------------+-------------------------------------------------------------------+

"""
import logging

# Set up the logger for the module
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s [%(lineno)d] %(message)s "
)

# Get the logger
logger: logging.Logger = logging.getLogger("algos.text")


def anagrams(word_set: set[str]) -> list[list[str]]:
    """
    Finds all anagrams of words contained within an input set of words.

    With an interactive Python session, you can run

    >>> from algos.text import anagrams
    >>> word_set = {'which', 'its', 'thing', 'drinking', 'can', 'car', 'that', 'cider', 'pain', 'and', 'by', 'below', \
'bowel', 'while', 'a', 'is', 'elbow', 'the', 'bending', 'in', 'during', 'an', 'arc', 'act', 'this', \
'cat', 'night', 'cried', 'rat', 'like', 'caused'}
    >>> anagrams(word_set)
    [['act', 'cat'], ['arc', 'car'], ['cider', 'cried'], ['bowel', 'elbow', 'below'], ['thing', 'night']]

    :raises TypeError: If the word_set is not a set.
    :raises TypeError: If the elements of the set are not all of type :class:`str` .
    :raises ValueError: If the word_set is empty.
    :param set[str] word_set: The set of words to find anagrams within.
    :return: A list of lists of anagrams.
    """
    # Create a dictionary that associates a word's signature to an array
    # containing all words with that signature.
    d: dict[str, list[str]] = {}

    # Declare the iterator.
    word: str

    # Raise TypeError if a set is not supplied.
    if not isinstance(word_set, set):
        logger.critical("anagrams - Incorrect Input Type")
        raise TypeError("Input Data Type Not Set")

    # Check that all element of set are of string type.
    if not all([isinstance(x, str) for x in word_set]):
        logger.critical("anagrams - Incorrect Elements Types")
        raise TypeError("Not All Elements of Type str")

    # Raise ValueError on empty set.
    if len(word_set) == 0:
        logger.critical("anagrams - Empty Input")
        raise ValueError("Empty Set")

    # For each word in the set of words.
    for word in word_set:
        # Calculate its signature. This is just each character sorted in alphabetical order as a single string.
        s: str = "".join(sorted(word))

        # If the signature has been encountered already
        if s in d:
            # Append the latest anagram to the list of anagrams with the same signature.
            d[s].append(word)
        # Otherwise this is the first occurrence of the signature.
        else:
            # Initialize the dictionary value with an array consisting of the word.
            d[s] = [word]

    # Return the lists of words for signatures that had more than one entry.
    return [d[s] for s in d if len(d[s]) > 1]

