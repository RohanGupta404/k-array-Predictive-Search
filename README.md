# k-array Predictive Search

**k-array Predictive Search** is a distribution-aware search algorithm that improves upon traditional binary search by allowing predictive, k-way partitioning of sorted arrays. It is designed to work efficiently across arbitrary, non-uniform distributions.

---

## 📌 Key Features
- ✅ Predicts the likely subarray using domain knowledge or heuristics
- ✅ Works with skewed, clustered, exponential, or multimodal data
- ✅ Generalizes binary search (k=2 is binary search)
- ✅ Recursively narrows down the search space with customizable `k`

---

## 📄 Paper

The technical write-up is available here:  
📄 [k_array_predictive_search_rohan_gupta_2025.pdf](./k_array_predictive_search_rohan_gupta_2025.pdf)

Status: Draft / Preprint  
Author: Rohan Gupta  
Date: October 2, 2025  
License: MIT

---

## 🧠 Why This?

Binary search is great — but it assumes uniform distribution and halves the array every time. Real-world data isn’t always like that.

This algorithm:
- Uses a prediction model to identify which of the `k` subarrays is most likely to contain the target.
- Reduces the number of comparisons and recursive calls when predictions are accurate.

---

## 📚 Example Use Case

Suppose you have a sorted array of 1000 elements with values following a skewed distribution.  
Using `k = 10` and a heuristic that accounts for the skew, this algorithm can jump directly to the right subarray rather than blindly splitting the array in half.

---

## 🚀 Future Work

- Auto-tune `k` based on dataset characteristics
- Learn heuristics dynamically using ML
- Extend to multidimensional structures (e.g., KD-Trees)

---

## 🛠️ Simple Python Version (Coming Soon)

> Stay tuned — will be adding a reference Python implementation with examples soon.

---

## 📬 Feedback Welcome

This is an early-stage idea. If you're reading this:
- Let me know what makes sense and what doesn't.
- Share improvements, bugs, or use cases.
- Star the repo if you find it interesting!

