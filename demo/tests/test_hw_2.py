"""
Mastering Object Oriented Design, 4ed.

Example tests using :class:`pytest`
"""
from io import StringIO
from unittest.mock import Mock
import pytest
import hw


def test_greeting():
    g = hw.Greeting("x", "y")
    assert str(g) == "x y"


@pytest.fixture
def mock_greeting(monkeypatch):
    greeting = Mock(
        name="Greeting",
        return_value=Mock(
            name="Greeting instance", __str__=Mock(return_value="mock str output")
        ),
    )
    monkeypatch.setattr(hw, "Greeting", greeting)
    return greeting


def test_main(mock_greeting, capsys):
    hw.main()

    mock_greeting.assert_called_with("hello", "world")
    mock_greeting.return_value.__str__.assert_called_with()

    out, err = capsys.readouterr()
    assert out == "mock str output\n"
