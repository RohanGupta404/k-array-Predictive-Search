
## NOTE: This is a test code still under development, requiring many bug fixes and alterations

# Counter for the recursion depth of the algorithm
depth = 1

def kaps(start, end, arr, T, k, divisor):
    # --------------------------------------------------------------------
    # K-Array Predictive Search, interpolation-guided search (work-in-progress).
    #
    # Parameters
    # ----------
    # start, end : int
    #     Current (inclusive) search window over the sorted array `arr`.
    # arr : Sequence[int]
    #     Sorted array of unique (assumed) integers to search in.
    # T : int
    #     Target value to locate.
    # k : int
    #     Intended "fan-out" (number of buckets/segments) for partitioning.
    # divisor : int
    #     When the interval gets too small (<= k), k is reduced via k // divisor.
    #
    # Behavior
    # --------
    # - Uses an interpolation estimate (`pos`) to choose which of k buckets to zoom into.
    # - Recurses while k >= 3 and the chosen sub-interval still has > 1 element.
    # - Falls back to a bounded check printing the current start/end values.
    #
    # Notes / Caveats
    # ---------------
    # - Uses a global `depth` counter for debugging the recursion depth.
    # - No explicit "not found" path: function prints and returns True on certain bases,
    #   but never returns False—callers can’t distinguish failure.
    # - Potential division-by-zero if `high == low` (flat segment).
    # - `subStart` / `subEnd` clamping attempts to keep indices in range w.r.t T,
    #   but edge cases may remain (e.g., off-by-one at array borders).
    # - Integer arithmetic via `//` makes bucket selection discrete.
    # - Assumes `arr` is sorted ascending and indexable at `start..end`.
    # --------------------------------------------------------------------


    global depth
    print(depth)  # Debug: print current recursion depth (1-based)
    depth += 1    # Increment depth counter


    # Base case: single element interval (start == end).
    # If reached, we "declare" it found at this index and succeed.
    if start == end:
        return True


    # If the interval is too small (length <= k), reduce k to avoid over-partitioning.
    if end - start <= k:
        k = k // divisor


    # Boundary values of the current interval for interpolation.
    low = arr[start]
    high = arr[end]


    # Interpolation position estimate (as a real number in [0, k)).
    # TODO : fix risk of ZeroDivisionError if high == low.
    pos = ((T - low) * k) / (high - low)


    # Map the bucket index floor(pos) to concrete sub-interval [subStart, subEnd].
    # Each bucket corresponds to a 1/k slice of the current [start, end] span.
    subStart = int((end-start) * (pos//1)/k) + start
    subEnd = int((end-start) * (pos//1 + 1)/k) + start


    # Clamp the sub-interval if T falls outside its boundary values.
    # If T < arr[subStart], search from the left boundary of the current window.
    if T < arr[subStart]:
        subStart = start
    # If T > arr[subEnd], search to the right boundary of the current window.
    elif T > arr[subEnd]:
        subEnd = end


    # Recurse if we still have at least a ternary (k >= 3) split
    # and the chosen sub-interval has length > 1.
    if k >= 3 and subEnd - subStart > 1:
        kaps(subStart, subEnd, arr, T, k, divisor)
    else:
        # Fallback/terminal: print current endpoints and succeed.
        # TODO : Make it so this does verifies equality with T; and not only report the bounds examined.
        print(f"start[{subStart}] = {arr[subStart]}, end[{subEnd}] = {arr[subEnd]}")
        return True


