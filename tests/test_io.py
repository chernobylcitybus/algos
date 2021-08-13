import io
from algos.io import ReadStdIn


class TestReadStdIn:
    def test_integer__expected_input(self, monkeypatch):
        """
        Test that the integer method works properly for expected inputs.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO("1"))

        # Create the instance
        reader = ReadStdIn()

        # Check that the value is the same as the monkeypatched value
        assert reader.integer() == 1
