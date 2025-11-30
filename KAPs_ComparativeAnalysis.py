import GenData

import L_Kaps
import KAPS_DifferentDistributions
import LKAPs_to_GChoice
import KAPS_BaseAlgorithm

import InterpolationSearch
import BinarySearch

import random
import matplotlib.pyplot as plt


bk_arr = []
dd_arr = []
is_arr = []
bs_arr = []


gen_functions = [
    GenData.gen_uniform,
    GenData.gen_zipf,
    GenData.gen_normal,
    GenData.gen_exponential,
    GenData.gen_lognormal,
    GenData.gen_pareto,
    GenData.gen_weibull,
    GenData.gen_logistic,
    GenData.gen_zipf_pareto
]
arr_length = 10**6


for i in range(1000):

    # Generating an array
    arr = sorted(random.choice(gen_functions)(arr_length))

    # Finding a random value to look for in the array
    target = arr[random.randint(0, len(arr))]

    dist = L_Kaps.lkaps(arr)


    baseKaps_result = KAPS_BaseAlgorithm.kaps(0, len(arr)-1, arr, target, 10, 2)
    DDKaps_result = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, target, 20, 2, LKAPs_to_GChoice.make_G_from_lkaps(arr, dist[0]))
    interpolation_result = InterpolationSearch.interpolationSearch(arr, 0, len(arr)-1, target)
    binary_result = BinarySearch.binarySearch(arr, 0, len(arr)-1, target)

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