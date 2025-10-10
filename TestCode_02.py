
## NOTE: This is a test code still under development, requiring many bug fixes and alterations

# Counter for the recursion depth of the algorithm
depth = 1

def kaps(lo, hi, arr, target, k, divisor):

    global depth
    print(depth)
    depth += 1


    # Base case: single element interval (lo == hi).
    # If reached, we "declare" it found at this index and succeed.
    if lo == hi:
        return True


    # If the interval is too small (length <= k), reduce k to avoid over-partitioning.
    if hi - lo <= k:
        k = k // divisor


    # Boundary values of the current interval for interpolation.
    pos = ((target - arr[lo]) * k) / (arr[hi] - arr[lo])


    # Map the bucket index floor(pos) to concrete sub-interval [subLo, subHi].
    # Each bucket corresponds to a 1/k slice of the current [lo, hi] span.
    subLo = int((hi-lo) * (pos//1)/k) + lo
    subHi = int((hi-lo) * (pos//1 + 1)/k) + lo


    print(arr[lo:hi+1])

    # Clamp the sub-interval if T falls outside its boundary values.
    # If T < arr[subLo], search from the left boundary of the current window.
    if target < arr[subLo]:
        subLo, subHi = lo, subLo
    # If T > arr[subHi], search to the right boundary of the current window.
    elif target > arr[subHi]:
        subHi, subLo = hi, subHi


    # Recurse if we still have at least a ternary (k >= 3) split
    # and the chosen sub-interval has length > 1.
    if subHi - subLo > 1 and k>1:
        print(f"lo[{subLo}] = {arr[subLo]}, hi[{subHi}] = {arr[subHi]}, k={k}")
        return kaps(subLo, subHi, arr, target, k, divisor)
    else:
        # Fallback/terminal: print current hipoints and succeed.
        # TODO : Make it so this does verifies equality with T; and not only report the bounds examined.
        return f"lo[{subLo}] = {arr[subLo]}, hi[{subHi}] = {arr[subHi]}, k={k}"


#kaps(lo=344, hi=349, arr, 35085313, k=2, divisor)