# Empirical Analysis of Memory-Accuracy Tradeoffs in Streaming Algorithms

## Status
**Status:** draft  
**Complete Specs:** 0%  
**Assignee:** TBD

# Template B: Full Research Project

## Description
- **Problem**: Streaming algorithms (for distinct count, frequent items,
  quantiles, clustering) trade memory for accuracy. Choosing a parameter (e.g.,
  sketch size) requires guessing at the tradeoff curve, and practitioners often
  over-provision memory or accept unnecessary accuracy loss
- **Key Angle**: Empirical Pareto frontier analysis across 10+ streaming
  algorithms and 8+ real-world data streams; quantify the exact accuracy vs
  memory curve for each
- **Novelty**: Prior work analyzes single algorithms in isolation; this project
  enables direct comparison and provides guidance for practitioners
- **Contribution**: Public benchmark, Pareto frontier recommendations, practical
  insights on when theoretical worst-case bounds are tight vs. loose

## Project Objective
Data streams are ubiquitous (log events, sensor data, stock tickers, network
traffic). Streaming algorithms compute approximate statistics on bounded memory
A practitioner must choose: "Should I use HyperLogLog with 1 KB or 10 KB memory
to count distinct users?"

Theoretical bounds say accuracy scales as $1/\sqrt{m}$ (memory), but constants
matter and real data may be kinder than worst-case. This project answers:

1. **For each streaming task (distinct count, heavy hitters, quantiles), what is
   the actual Pareto frontier of memory vs. accuracy?**
2. **Which algorithms dominate the frontier for different data characteristics
   (heavy-tailed, bursty, adversarial)?**
3. **How do theoretical worst-case bounds compare to empirical performance on
   real data?**

Deliverables: A benchmark suite, Pareto frontier plots, a decision tree for
algorithm selection, and insights for practitioners and theorists

## Core Thesis
- **Conventional view**: Streaming algorithm choice is driven by theoretical
  guarantees (worst-case complexity); practitioners apply these bounds blindly
- **Empirical motivation**: Real data is often biased (heavy-tailed, clustered,
  time-correlated); worst-case analysis is pessimistic. HyperLogLog counts
  distinct users in log streams with <1% error at 1 KB, but theory promises >10%
  error
- **Hypothesis**: Empirical accuracy depends strongly on data statistics
  (distribution of item frequencies, stream burstiness, arrival patterns);
  algorithms that are theoretically equivalent may have vastly different
  empirical performance on real data
- **Goal**: A data-aware benchmark and practical guide that helps practitioners
  choose streaming algorithms by (1) data characteristics, (2) memory budget,
  and (3) accuracy target

## Dataset Suggestions
1. **Distinct Counting: Stack Overflow Logs**
   - Source: Kaggle or Internet Archive; or simulated based on
     https://data.stackexchange.com/
   - Contains: User IDs in timestamped requests; highly skewed (few power users,
     many one-time visitors)
   - Access: Freely available simulated data; real data requires scraping
   - Why: Tests algorithms on realistic power-law distributions; representative
     of web traffic

2. **Heavy Hitters: CAIDA Internet Traffic Dataset**
   - Source: https://catalog.caida.org/dataset/passive_traffic_trace
     (registration required, but free for academic use)
   - Contains: Network flow records (source IP, dest IP, packet counts) from
     backbone routers; structured with many rare flows and few dominant flows
   - Access: Free with academic email; requires HTTP download
   - Why: Real network data with bursty temporal patterns; benchmark-standard
     for streaming algorithms

3. **Quantiles: NYC Taxi Trip Times**
   - Source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
     (public, monthly Parquet files)
   - Contains: Trip duration (seconds), distance, time of day; realistic
     distribution with outliers
   - Access: Free download
   - Why: Test quantile sketch algorithms; distribution has long right tail
     (relevant for SLA monitoring)

4. **Stream Clustering: Sensor Data Streams**
   - Source: UCI ML Repository: Sensor datasets (e.g., Intel Berkeley Research
     Lab sensor data,
     https://archive.ics.uci.edu/ml/datasets/Sensor+Stream+Data)
   - Contains: Timestamped sensor readings (temperature, humidity) from 54
     sensors over 2 months; temporal correlation and drift
   - Access: Free download
   - Why: Tests clustering algorithms under concept drift; realistic streaming
     scenario

5. **Frequency Moments: Synthetic Log-Normal Streams**
   - Source: Generate synthetic data with known $F_k$ (frequency moments) for
     ground truth
   - Contains: Synthetic item frequencies drawn from log-normal, Zipfian, and
     uniform distributions; parametrizable burstiness
   - Access: Generate with Python (scipy.stats)
   - Why: Enables controlled experiments; can match real data statistics while
     adding adversarial cases

6. **Word Frequency in Text Streams: Common Crawl / Wikipedia**
   - Source: Hugging Face datasets library (wikimedia or oscar)
   - Contains: Raw text; run tokenizer to get word streams; power-law word
     frequency (Zipf's law)
   - Access: Free via `datasets.load_dataset('wikipedia')`
   - Why: Tests on structured, real-world text; Zipf distribution is
     well-studied

## Tasks
1. **Implement 10+ Streaming Algorithms**:
   - **Distinct Counting**: HyperLogLog, HyperLogLog++, Linear Counting,
     Min-Hash, KMV (K Minimum Values)
   - **Frequent Items (Heavy Hitters)**: Count-Min Sketch, Count-Sketch,
     Frequent, Space-Saving, Top-K PowerSketch
   - **Quantiles**: t-Digest, KLL Sketch, GK Algorithm (Greenwald-Khanna)
   - **Stream Clustering**: D-Stream, CluStream, DenStream (density-based)

   Use reference implementations (Datasketches library, Redis modules, or
   reimplements for reproducibility)

2. **Benchmark Suite Setup**:
   - For each algorithm, create a parameterized version where memory (sketch
     size, buffer size, etc.) is a knob
   - Implement ground truth computation (e.g., exact distinct count via HashSet)
     for validation
   - Create a runner that varies memory from 256 bytes to 10 MB and measures
     accuracy (relative error, rank error for quantiles, purity for clustering)

3. **Data Preparation & Streaming Simulation**:
   - Download or generate 8 datasets (from Dataset Suggestions)
   - Normalize datasets to a common format: stream of (timestamp, item_id,
     value)
   - Create adversarial streams: random permutation, sorted (worst-case for some
     sketches), bursty (clustered in time), with concept drift
   - Generate 10 random substreams from each dataset to measure variance

4. **Execute Experiments**:
   - For each (algorithm, dataset, memory level), run the algorithm on the
     stream and measure ground-truth accuracy
   - Measure wall-clock time and actual memory usage (not just theoretical)
   - Run 3 trials with different random seeds; record mean, median, and
     percentiles (10th, 90th)
   - Total runs: 10 algorithms × 8 datasets × 10 memory levels × 3 trials × 3
     stream variants ≈ 7,200 trials (parallelizable)

5. **Pareto Frontier Analysis**:
   - For each (algorithm, dataset), plot accuracy vs. memory; fit curves (e.g.,
     $\text{error} \propto 1/\sqrt{m}$) and extract parameters
   - Identify algorithms on the Pareto frontier: no algorithm dominates on both
     memory and accuracy
   - Compute "Pareto distance" for each algorithm (how much extra memory for
     same accuracy as frontier)
   - Analyze which algorithms are frontier-dominant for which data distributions

6. **Statistical Analysis & Decision Rules**:
   - Fit logistic regression or decision tree: features = data characteristics
     (Gini coefficient, burstiness, item count), targets = recommended algorithm
   - Cross-validate recommendations on held-out datasets
   - Summarize in a decision guide: "If data is Zipfian and bursty, use
     Space-Saving over Count-Sketch; save ~30% memory at 0.1% error"
   - Analyze how often empirical performance matches theoretical bounds

## Expected Findings
1. **HyperLogLog dominates distinct counting for large $n$**: Across all
   datasets, HyperLogLog is Pareto-optimal for distinct count; alternatives
   never cheaper or more accurate
2. **Count-Min Sketch is robust but suboptimal on power-law data**: On Zipfian
   data, Frequent or Space-Saving beat Count-Min at same memory; but Count-Min
   is safer if data characteristics unknown
3. **Theoretical bounds are loose by 5–50x**: HyperLogLog theory predicts ~2%
   error at 1 KB memory; empirically achieves 0.1% on real data (50x tighter)
4. **Quantile sketches are sensitive to outliers**: t-Digest is more accurate
   for tail quantiles; KLL is better for median; GK is worst on heavy-tailed
   distributions
5. **Bursty streams require larger sketches**: Count-Sketch needs 30% more
   memory on bursty streams (temporal correlation) than uniform random streams;
   streaming algorithms assume independence

## Bonus Ideas
- **Streaming Joins**: Compare algorithms for approximate equijoin on streams
  (e.g., sampling vs. hash-based)
- **Adversarial Robustness**: Design adversarial streams that maximize error for
  each algorithm; measure how practitioners' parameters compare to adversarial
  worst-case
- **Time-Aware Sketches**: Adapt sketches to weight recent data more heavily
  (with decay); compare accuracy vs. fixed-memory sketches
- **Hardware Effects**: Measure how CPU cache, SIMD, and memory bandwidth affect
  algorithm runtime; theoretical analysis ignores these

## Extensions
- **Multi-Stream Merging**: Merge sketches from distributed streams; how does
  merging error compound?
- **Adaptive Algorithms**: Dynamically adjust sketch size based on observed
  error rate; can we tune faster than offline tuning?
- **Sketch Composition**: Chain sketches (e.g., Count-Min Sketch → Top-K → Count
  Sketch) for combined workloads; what is the overhead?

## Policy / Practical Implications
- **Industry Best Practices**: Benchmark should be incorporated into data
  engineering documentation; current guidance (e.g., Spark, Flink docs) is
  outdated
- **Parameter Tuning**: Frameworks should expose algorithm selection via
  high-level APIs: `select_distinct_counter(data_sample, memory_budget)` instead
  of low-level parameters
- **Theoretical Gaps**: Current bounds are over-conservative for real data;
  tighter analysis or adaptive algorithms could reduce memory use by 10–50%

## Useful Resources
- [Datasketches Java Library](https://datasketches.apache.org/): Reference
  implementations of HyperLogLog, KLL, etc
- [Flajolet, P., & Martin, G. N. (1985). "Probabilistic Counting Algorithms for Data Base Applications." _Journal of Computer and System Sciences_, 31(2), 182–209.](https://www.sciencedirect.com/science/article/pii/0022000085900417)
  — HyperLogLog precursor
- [Cormode, G., & Muthukrishnan, S. (2005). "An improved data stream summary: the count-min sketch and its applications." _Journal of Algorithms_, 55(1), 58–75.](https://www.sciencedirect.com/science/article/pii/S0196677404001499)
  — Count-Min Sketch foundational paper
- [Karnin, Z., Lang, K., & Liberty, E. (2016). "Optimal quantile approximation in streams." _FOCS_, 2016.](https://arxiv.org/abs/1603.05346)
  — KLL Sketch theory
- [Dunning, T. (2019). "t-Digest: Accurate quantile sketches on data streams."](https://github.com/tdunning/t-digest)
  — t-Digest implementation and docs
