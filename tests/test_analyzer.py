import pandas as pd
import pytest

from target_curve_analyzer.analyzer import compare_curves


def curve(levels):
    return pd.DataFrame(
        {
            "frequency_hz": [100, 1000, 10000],
            "level_db": levels,
        }
    )


def test_identical_curves_have_zero_error():
    comparison, result = compare_curves(
        curve([0, 0, 0]),
        curve([0, 0, 0]),
    )

    assert result.mean_absolute_error_db == pytest.approx(0)
    assert result.rms_error_db == pytest.approx(0)
    assert result.maximum_deviation_db == pytest.approx(0)
    assert result.within_tolerance_percent == pytest.approx(100)
    assert len(comparison) == 3


def test_constant_offset_is_detected():
    _, result = compare_curves(
        curve([2, 2, 2]),
        curve([0, 0, 0]),
        tolerance_db=1.0,
    )

    assert result.mean_absolute_error_db == pytest.approx(2)
    assert result.rms_error_db == pytest.approx(2)
    assert result.maximum_deviation_db == pytest.approx(2)
    assert result.within_tolerance_percent == pytest.approx(0)


def test_frequency_limits_are_applied():
    _, result = compare_curves(
        curve([0, 1, 2]),
        curve([0, 0, 0]),
        min_frequency_hz=1000,
        max_frequency_hz=10000,
    )

    assert result.frequency_min_hz == pytest.approx(1000)
    assert result.frequency_max_hz == pytest.approx(10000)
