# Target Curve Analyzer

A practical Python tool for objective evaluation of measured audio frequency-response curves against a defined target curve.

The project is designed around a simple engineering principle:

> Turn subjective discussions about sound direction into a reproducible measurement and evaluation process.

It calculates deviation between a measured response and a target curve, including mean absolute error, RMS error, maximum deviation, and the percentage of frequency points within a configurable tolerance band.

## Features

- CSV import for measured and target frequency-response data
- Automatic interpolation onto a common frequency grid
- Configurable frequency range
- Configurable tolerance band
- Mean Absolute Error (MAE)
- RMS Error
- Maximum absolute deviation
- Percentage of points within tolerance
- Frequency-by-frequency deviation analysis
- Publication-ready response plot
- CSV export of the analysis
- Command-line interface
- Unit tests

## Data format

CSV files require two columns:

```text
frequency_hz,level_db
20,-2.1
25,-1.8
31.5,-1.2
...
```

Frequency values should be positive and monotonically increasing.

## Installation

Requires Python 3.10 or newer.

```bash
git clone https://github.com/YOUR-USERNAME/target-curve-analyzer.git
cd target-curve-analyzer
python -m venv .venv
```

Activate the environment:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Analyze the included example data:

```bash
python -m target_curve_analyzer.cli \
  --measurement examples/measurement.csv \
  --target examples/target.csv \
  --output report.csv \
  --plot response.png \
  --tolerance 1.0
```

If using the source checkout directly, set the Python path:

```bash
PYTHONPATH=src python -m target_curve_analyzer.cli \
  --measurement examples/measurement.csv \
  --target examples/target.csv \
  --output report.csv \
  --plot response.png \
  --tolerance 1.0
```

## Example output

```text
Target Curve Analysis
---------------------
Frequency range:       20.0 - 20000.0 Hz
Tolerance:             +/-1.00 dB

Mean absolute error:   0.72 dB
RMS error:             0.91 dB
Maximum deviation:     2.43 dB
Within tolerance:      82.4 %
```

## Engineering interpretation

The tool deliberately separates numerical evaluation from subjective listening.

A low numerical error does not automatically mean that a system sounds better. Conversely, a technically larger deviation can sometimes be intentional if it supports the desired perceptual result.

The purpose is to provide a common, reproducible reference for engineering discussion and iteration.

## Example workflow

1. Define the desired target curve.
2. Measure the system under controlled conditions.
3. Import the measurement and target.
4. Calculate objective deviations.
5. Identify frequency regions requiring attention.
6. Apply DSP or acoustic changes.
7. Re-measure.
8. Compare the new result against the target.

This makes the target curve a shared engineering reference rather than a purely subjective preference.

## Project structure

```text
target-curve-analyzer/
├── examples/
│   ├── measurement.csv
│   └── target.csv
├── src/
│   └── target_curve_analyzer/
│       ├── __init__.py
│       ├── analyzer.py
│       └── cli.py
├── tests/
│   └── test_analyzer.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Scope

This project is intentionally lightweight. It is not intended to replace professional acoustic measurement software. It demonstrates a reproducible evaluation layer that can sit on top of measurement systems and DSP workflows.

## Author

**Patrick Putzolu**

Audio Engineering · DSP · Acoustic Evaluation · Music Production

The project is based on general audio-engineering methodology and uses synthetic example data.
