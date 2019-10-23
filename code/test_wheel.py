"""
Building Skills in Object-Oriented Design V4

Wheel Examples
"""
from unittest.mock import MagicMock, Mock
import pytest
from wheel_examples import Wheel, Wheel_RNG


def test_wheel_rng():
    mock_rng = Mock(
        choice=Mock(return_value="bin1")
    )

    bins = ["bin1", "bin2"]
    wheel = Wheel_RNG(bins, mock_rng)
    value = wheel.choose()

    assert value == "bin1"
    mock_rng.choice.assert_called_with(bins)


def test_wheel_isolation():
    mock_rng = Mock(
        choice=Mock(return_value="bin1")
    )

    bins = ["bin1", "bin2"]
    wheel = Wheel(bins)
    wheel.rng = mock_rng  # Replaces random.Random
    value = wheel.choose()

    assert value == "bin1"
    mock_rng.choice.assert_called_with(bins)


def test_wheel_integration():
    bins = ["bin1", "bin2"]
    wheel = Wheel(bins)
    wheel.rng.seed(42)
    value = wheel.choose()

    assert value == "bin1"
