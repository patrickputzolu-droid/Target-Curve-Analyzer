from __future__ import annotations

import argparse

from .analyzer import (
    compare_curves,
    load_curve,
    plot_comparison,
    save_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare an audio measurement against a target curve."
    )
    parser.add_argument("--measurement", required=True, help="Measurement CSV")
    parser.add_argument("--target", required=True, help="Target curve CSV")
    parser.add_argument("--output", default="analysis.csv", help="Report CSV")
    parser.add_argument("--plot", default="analysis.png", help="Plot PNG")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1.0,
        help="Tolerance band in dB (default: 1.0)",
    )
    parser.add_argument("--min-frequency", type=float, default=None)
    parser.add_argument("--max-frequency", type=float, default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()

    measurement = load_curve(args.measurement)
    target = load_curve(args.target)

    comparison, result = compare_curves(
        measurement,
        target,
        tolerance_db=args.tolerance,
        min_frequency_hz=args.min_frequency,
        max_frequency_hz=args.max_frequency,
    )

    save_report(comparison, args.output)
    plot_comparison(
        comparison,
        args.plot,
        tolerance_db=args.tolerance,
    )

    print("Target Curve Analysis")
    print("---------------------")
    print(f"Frequency range:       {result.frequency_min_hz:.1f} - "
          f"{result.frequency_max_hz:.1f} Hz")
    print(f"Tolerance:             +/-{result.tolerance_db:.2f} dB")
    print()
    print(f"Mean absolute error:   {result.mean_absolute_error_db:.2f} dB")
    print(f"RMS error:             {result.rms_error_db:.2f} dB")
    print(f"Maximum deviation:     {result.maximum_deviation_db:.2f} dB")
    print(f"Within tolerance:      {result.within_tolerance_percent:.1f} %")
    print()
    print(f"Report: {args.output}")
    print(f"Plot:   {args.plot}")


if __name__ == "__main__":
    main()
