from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AnalysisResult:
    """Summary metrics for a target-curve comparison."""

    mean_absolute_error_db: float
    rms_error_db: float
    maximum_deviation_db: float
    within_tolerance_percent: float
    frequency_min_hz: float
    frequency_max_hz: float
    tolerance_db: float


def load_curve(path: str | Path) -> pd.DataFrame:
    """Load a two-column frequency-response CSV.

    Expected columns:
        frequency_hz, level_db
    """
    df = pd.read_csv(path)

    required = {"frequency_hz", "level_db"}
    if not required.issubset(df.columns):
        raise ValueError(
            f"{path} must contain columns: frequency_hz, level_db"
        )

    df = df[["frequency_hz", "level_db"]].copy()
    df = df.dropna()

    if (df["frequency_hz"] <= 0).any():
        raise ValueError("Frequency values must be greater than zero.")

    df = df.sort_values("frequency_hz")
    df = df.drop_duplicates("frequency_hz")

    if len(df) < 2:
        raise ValueError("A curve must contain at least two valid points.")

    return df


def compare_curves(
    measurement: pd.DataFrame,
    target: pd.DataFrame,
    tolerance_db: float = 1.0,
    min_frequency_hz: float | None = None,
    max_frequency_hz: float | None = None,
) -> tuple[pd.DataFrame, AnalysisResult]:
    """Interpolate both curves onto a common frequency grid and compare them."""
    lower = max(
        measurement["frequency_hz"].min(),
        target["frequency_hz"].min(),
    )
    upper = min(
        measurement["frequency_hz"].max(),
        target["frequency_hz"].max(),
    )

    if min_frequency_hz is not None:
        lower = max(lower, min_frequency_hz)
    if max_frequency_hz is not None:
        upper = min(upper, max_frequency_hz)

    if lower >= upper:
        raise ValueError("No overlapping frequency range is available.")

    common_frequency = np.unique(
        np.concatenate(
            [
                measurement["frequency_hz"].to_numpy(),
                target["frequency_hz"].to_numpy(),
            ]
        )
    )
    common_frequency = common_frequency[
        (common_frequency >= lower) & (common_frequency <= upper)
    ]

    measurement_level = np.interp(
        common_frequency,
        measurement["frequency_hz"],
        measurement["level_db"],
    )
    target_level = np.interp(
        common_frequency,
        target["frequency_hz"],
        target["level_db"],
    )

    deviation = measurement_level - target_level
    absolute_deviation = np.abs(deviation)

    comparison = pd.DataFrame(
        {
            "frequency_hz": common_frequency,
            "measurement_db": measurement_level,
            "target_db": target_level,
            "deviation_db": deviation,
            "absolute_deviation_db": absolute_deviation,
            "within_tolerance": absolute_deviation <= tolerance_db,
        }
    )

    result = AnalysisResult(
        mean_absolute_error_db=float(np.mean(absolute_deviation)),
        rms_error_db=float(np.sqrt(np.mean(deviation**2))),
        maximum_deviation_db=float(np.max(absolute_deviation)),
        within_tolerance_percent=float(
            np.mean(absolute_deviation <= tolerance_db) * 100
        ),
        frequency_min_hz=float(lower),
        frequency_max_hz=float(upper),
        tolerance_db=float(tolerance_db),
    )

    return comparison, result


def save_report(comparison: pd.DataFrame, path: str | Path) -> None:
    """Save the frequency-by-frequency comparison as CSV."""
    comparison.to_csv(path, index=False)


def plot_comparison(
    comparison: pd.DataFrame,
    path: str | Path,
    title: str = "Target Curve Analysis",
    tolerance_db: float = 1.0,
) -> None:
    """Create a logarithmic frequency-response comparison plot."""
    import matplotlib.pyplot as plt

    frequency = comparison["frequency_hz"]
    measurement = comparison["measurement_db"]
    target = comparison["target_db"]

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    axes[0].semilogx(frequency, measurement, label="Measurement")
    axes[0].semilogx(frequency, target, label="Target")
    axes[0].set_ylabel("Level (dB)")
    axes[0].set_title(title)
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend()

    deviation = comparison["deviation_db"]
    axes[1].semilogx(frequency, deviation, label="Deviation")
    axes[1].axhline(0, linewidth=0.8)
    axes[1].axhline(tolerance_db, linestyle="--", linewidth=0.8)
    axes[1].axhline(-tolerance_db, linestyle="--", linewidth=0.8)
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Deviation (dB)")
    axes[1].grid(True, which="both", alpha=0.25)

    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
