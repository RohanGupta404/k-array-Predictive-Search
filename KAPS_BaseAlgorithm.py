## NOTE: This is a test implementation of k-ary predictive search,
## still experimental and may need further adjustments.

# Tracks recursion depth for debugging / tracing
depth = 0

def kaps(lo, hi, arr, target, k, divisor):

    global depth
    depth += 1

    # Fast rejects: target outside current window's value range
    if target < arr[lo] or target > arr[hi]:
        d = depth
        depth = 0
        return -1, d

    # Base case: interval collapsed to one element.
    # Return its index if it matches, else -1.
    if lo == hi:
        d = depth
        depth = 0
        return lo, depth if arr[lo] == target else -1, d

    # If the interval length is smaller than k,
    # reduce k to avoid over-partitioning.
    if hi - lo <= k:
        k = k // divisor

    # Interpolation step: estimate relative position of target.
    pos = ((target - arr[lo]) * k) / (arr[hi] - arr[lo])

    # Map interpolated bucket to sub-interval [subLo, subHi].
    subLo = int((hi - lo) * (pos // 1) / k) + lo
    subHi = int((hi - lo) * (pos // 1 + 1) / k) + lo

    # Adjust sub-interval if target falls outside bucket boundaries.
    if target < arr[subLo]:
        subLo, subHi = lo, subLo
    elif target > arr[subHi]:
        subHi, subLo = hi, subHi
    else:
        # Direct hit checks for bucket boundaries.
        if arr[subLo] == target:
            d = depth
            depth = 0
            return subLo, d
        elif arr[subHi] == target:
            d = depth
            depth = 0
            return subHi, d
        # otherwise keep current [subLo, subHi]

    # Recurse if interval is still larger than 1
    # and k allows further partitioning.
    if subHi - subLo > 1 and k > 1:
        return kaps(subLo, subHi, arr, target, k, divisor)
    else:
        # Terminal step: at most two candidates left.
        # Constant-time equality checks, no loop.
        for i in range(subLo, subHi + 1):
            if arr[i] == target:
                d = depth
                depth = 0
                return i, d
        d = depth
        depth = 0
        return -1, d
