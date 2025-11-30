# K-Array Predictive Search (KAPS)

This repository contains experimental implementations of **K-Array Predictive Search (KAPS)** and its main variants:

- **DD-KAPS** – KAPS tuned for different, known value distributions  
- **L-KAPS** – KAPS that first *learns* or approximates the data distribution, then searches  
- **Base KAPS** – a simplified “baby” version mainly used for explanation and intuition  

The core algorithms live under `src/kaps/`, and all graphs/experiments live in the `experiments/` folder.

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/RohanGupta404/k-array-Predictive-Search.git
cd k-array-Predictive-Search
```

2. **(Optional) Create and activate a virtual environment**

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Minimal `requirements.txt`:**

```txt
numpy>=1.24
matplotlib>=3.7
```

---

## Project Structure

```text
k-array-Predictive-Search/
├── README.md
├── LICENSE
├── requirements.txt
│
├── src/
│   └── kaps/
│       ├── __init__.py
│       ├── base_kaps.py              # simple teaching version of KAPS
│       ├── dd_kaps.py                # distribution-specific KAPS implementation
│       ├── l_kaps.py                 # L-KAPS (learned / inferred distribution)
│       ├── lkaps_to_gchoice.py       # helper for L-KAPS decisions
│       ├── generators.py             # data generators (uniform, zipf, exponential, etc.)
│       └── baselines/
│           ├── __init__.py
│           ├── binary_search.py      # classic binary search
│           └── interpolation_search.py  # interpolation search
│
└── experiments/
    ├── comparative_analysis.py       # performance comparisons and graphs
    └── plot_distributions.py         # LKAPS distribution prediction vs actual data
```

---

## Using the Algorithms in Code

Because this repo uses a `src/` layout, there are two easy ways to import `kaps`:

### Option A: Add `src` to `PYTHONPATH` when running

From the repo root:

```bash
# macOS / Linux
PYTHONPATH=src python experiments/comparative_analysis.py

# Windows (PowerShell)
$env:PYTHONPATH="src"; python experiments/comparative_analysis.py
```

Inside your scripts you can then do:

```python
from kaps import dd_kaps, lkaps, base_kaps
from kaps.generators import gen_uniform
from kaps.baselines import binary_search, interpolation_search
```

### Option B (optional): Install as an editable package

If you prefer:

1. Create a simple `pyproject.toml` later and run:

```bash
pip install -e .
```

2. Then you can import `kaps` from anywhere on your machine.

For now, Option A (setting `PYTHONPATH=src`) is enough.


## What Each Core File Does

`src/kaps/base_kaps.py`

* Contains the simplified, didactic version of KAPS.
* Useful for understanding the basic idea of k-way predictive search.
* Example API (your actual function names may differ):

```python
from kaps import base_kaps

idx, searchDepth = base_kaps(0, len(arr)-1, arr, target, k, divisor)
```

---

`src/kaps/dd_kaps.py` (Different-Distributions KAPS)

* Core implementation of KAPS when you know or assume a distribution type.
* Uses heuristics tuned to uniform, zipf, exponential, normal, etc.
* You might expose an interface like:

```python
from kaps import dd_kaps

idx, searchDepth = dd_kaps(
    0,
    len(arr)-1,
    arr,
    target,
    k,
    divisor,
    G_choice
)
```

---

`src/kaps/l_kaps.py` (L-KAPS)

* Implementation of KAPS that first learns/approximates the distribution of the data.
* Then uses that information to guide the search more efficiently.
* Example usage:

```python
from kaps import lkaps

dist, distScore = lkaps(arr)
```

---

`src/kaps/lkaps_to_gchoice.py`

* Helper utilities used by L-KAPS.
* Maps the learned distribution info (or curve) to actual “where should I search next?” decisions (which region / k-split to pick).

---

`src/kaps/generators.py`

* All the synthetic data generators used in experiments.
* Typical functions you might have:

```python
from kaps.generators import (
    gen_uniform,
    gen_zipf,
    gen_normal,
    gen_exponential,
    gen_lognormal,
    gen_pareto,
    gen_weibull,
    gen_logistic,
    gen_zipf_pareto,
)

arr = gen_exponential(N=100_000)
```

Each generator should return a sorted array suitable for search.

---

`src/kaps/baselines/`

* `binary_search.py`

    Classic binary search – used as a baseline against KAPS.

* `interpolation_search.py`

    Interpolation search – another baseline algorithm.

From code:

```python
from kaps.baselines import binary_search, interpolation_search

idx_bs, searchDepth_bs = binary_search(arr, 0, len(arr)-1, target)
idx_is, searchDepth_is = interpolation_search(arr, 0, len(arr)-1, target)
```

---

## Running the Experiments

All experiments assume you run them from the repo root, with `src` on the Python path.

### 1. Comparative Performance (`experiments/comparative_analysis.py`)

**Goal:**

Generate graphs that show how:

* Base KAPS
* DD-KAPS
* L-KAPS
* Binary search
* Interpolation search

compare in terms of:

* search depth
* number of steps
* and/or runtime

**Run:**

```bash
PYTHONPATH=src python experiments/comparative_analysis.py
```

**Expected behavior inside the script:**

* Import the algorithms and data generators:

```python
from kaps import base_kaps, dd_kaps, l_kaps
from kaps.baselines import binary_search, interpolation_search
from kaps.generators import (
    gen_uniform, gen_zipf, gen_normal, gen_exponential,
    gen_lognormal, gen_pareto, gen_weibull, gen_logistic, gen_zipf_pareto
)
```

* For each distribution and/or array size:

  * Generate data using `generators.py`
  * Pick random targets
  * Run each algorithm
  * Store search depth / step counts
  * Plot scatterplots / boxplots to showcase how big base KAPS is vs the others

This is the script that produces your “look how much deeper binary search is compared to KAPS” graphs.

---

### 2. Distribution Prediction (`experiments/plot_distributions.py`)

**Goal:**

Use generated data and L-KAPS to:

* Graph the actual distribution of the data
* Graph what L-KAPS predicts the underlying distribution looks like
* Overlay them (e.g., blue = input data, green = predicted distribution curve)

**Run:**

```bash
PYTHONPATH=src python experiments/plot_distributions.py
```

**Expected behavior inside the script:**

* Import generators and L-KAPS:

```python
from kaps.generators import gen_exponential  # or any other generator
from kaps import l_kaps  # and/or an L-KAPS distribution estimator function
import matplotlib.pyplot as plt
import numpy as np
```

* Generate a sorted array with one of the generators.

* Use the L-KAPS logic that estimates the distribution (whatever function you’ve written for that).

* Plot something like:

```python
plt.plot(x_indices, actual_values, label="Input Array")
plt.plot(x_indices, predicted_values, label="L-KAPS predicted distribution")
plt.legend()
plt.show()
```

This script is your visual proof that L-KAPS is correctly predicting the distribution shape.









































