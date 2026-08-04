# Kolmogorov Complexity Over Time

**Status:** draft | **Specs:** 10% | **Assignee:** —

## Core Idea

Use Kolmogorov complexity to measure the compressibility of a data stream over
time. Changes in compression rate can serve as a signal for regime shifts,
concept drift, or fundamental changes in the underlying process.

## Formalization

Measure compressibility of an entire data stream:

\[
K(x_{1:T})
\]

Or its incremental description length:

\[
L = \sum_{t=1}^{T} K(x_{t} \mid x_{<t})
\]

A sudden increase in \(K(x_{t} \mid x_{<t})\) indicates that past patterns no
longer predict the present—a regime shift has occurred.

## Key Examples

- **Financial time series**: A market that suddenly becomes less compressible
  (higher conditional Kolmogorov complexity) may indicate a regime change—the
  2008 financial crisis or COVID-19 market turbulence are canonical examples
  where past patterns stopped predicting future behavior.
- **Industrial sensor data**: Predictive maintenance systems where machinery
  degradation causes the signal to become progressively less compressible
  before failure.
- **Network intrusion detection**: Normal traffic patterns have regular
  structure (low \(K\)); attacks introduce novel patterns, increasing
  \(K(x_{t} \mid x_{<t})\).

## Provocative Question

Is there a fundamental limit to predictability based on Kolmogorov complexity?
If \(K(x_{t} \mid x_{<t})\) approaches \(|x_{t}|\) (data is incompressible
given past), does this imply the system has become random, or that our model
class is too weak?

## Research Topics

- Using compression rate changes to detect regime shifts in real time
- Understanding the gap between Kolmogorov complexity (uncomputable) and
  practical compression-based approximations
- Bounding predictability from above using conditional Kolmogorov complexity
- Connecting compression-based change detection to PAC-style learning bounds

## References

- Derived from *Research_plan/paper.tex* (Section: Quasi-Stationary Learning /
  Kolmogorov Complexity Over Time)