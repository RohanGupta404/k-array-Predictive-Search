import random
import matplotlib.pyplot as plt

import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from kaps import base_kaps, dd_kaps, lkaps, lkaps_to_G
from kaps.generators import *
from kaps.baselines import binary_search, interpolation_search


bk_arr = []
dd_arr = []
is_arr = []
bs_arr = []


gen_functions = [
    gen_uniform,
    gen_zipf,
    gen_normal,
    gen_exponential,
    gen_lognormal,
    gen_pareto,
    gen_weibull,
    gen_logistic,
    gen_zipf_pareto
]
arr_length = 10**6


for i in range(5):

    # Generating an array
    arr = sorted(random.choice(gen_functions)(arr_length))

    # Finding a random value to look for in the array
    target = arr[random.randint(0, len(arr))]

    dist = lkaps(arr)


    baseKaps_result = base_kaps(0, len(arr)-1, arr, target, 10, 2)
    DDKaps_result = dd_kaps(0, len(arr)-1, arr, target, 20, 2, lkaps_to_G(arr, dist[0]))
    interpolation_result = interpolation_search(arr, 0, len(arr)-1, target)
    binary_result = binary_search(arr, 0, len(arr)-1, target)

    bk_arr.append(baseKaps_result[1])
    dd_arr.append(DDKaps_result[1])
    is_arr.append(interpolation_result[1])
    bs_arr.append(binary_result[1])
    print(i)




# Graph 1 ------------------------------

plt.figure(figsize=(10,6))
plt.scatter(range(len(bk_arr)), bk_arr, label="Base KAPs", s=25, color="#1f77b4")
plt.scatter(range(len(dd_arr)), dd_arr, label="L-KAPs optimised KAPs", s=25, color="#9467bd")
plt.scatter(range(len(is_arr)), is_arr, label="Interpolation Search", s=25, color="#2ca02c")
plt.scatter(range(len(bs_arr)), bs_arr, label="Binary Search", s=25, color="#d62728")

plt.title("Search Depth taken by each Distribution")
plt.xlabel("Iteration")
plt.ylabel("Search Depth")

plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()


# Graph 2 ------------------------------

plt.figure(figsize=(10,6))
plt.scatter(range(len(bk_arr)), bk_arr, label="Base KAPs", s=25, color="#1f77b4")
plt.scatter(range(len(dd_arr)), dd_arr, label="L-KAPs optimised KAPs", s=25, color="#9467bd")
plt.scatter(range(len(bs_arr)), bs_arr, label="Binary Search", s=25, color="#d62728")

plt.title("Search Depth taken by each Distribution")
plt.xlabel("Iteration")
plt.ylabel("Search Depth")

plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()


# Graph 3 ------------------------------


plt.figure(figsize=(9,6))

# Data in same order as your scatter labels
data = [bk_arr, dd_arr, is_arr, bs_arr]
labels = ["Base KAPs", "L-KAPs optimised KAPs", "Interpolation Search", "Binary Search"]

plt.boxplot(data, labels=labels, patch_artist=True)

plt.title("Search Depth Distribution Comparison (Boxplot)")
plt.ylabel("Search Depth")
plt.xticks(rotation=15)

plt.tight_layout()
plt.show()


# Graph 4 ------------------------------


plt.figure(figsize=(9,6))

# Data in same order as your scatter labels
data = [bk_arr, dd_arr, bs_arr]
labels = ["Base KAPs", "L-KAPs optimised KAPs", "Binary Search"]

plt.boxplot(data, labels=labels, patch_artist=True)

plt.title("Search Depth Distribution Comparison (Boxplot)")
plt.ylabel("Search Depth")
plt.xticks(rotation=15)

plt.tight_layout()
plt.show()