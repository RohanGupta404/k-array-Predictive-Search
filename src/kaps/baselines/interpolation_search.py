# Python3 program to implement
# interpolation search with recursion

depth = 0

def interpolation_search(arr, lo, hi, x):

    global depth
    depth += 1

    # Safety stop — prevents recursion overflow
    if depth > 998:
        d = depth
        depth = 0
        return -1, d

    # Valid bounds
    if lo <= hi and arr[lo] <= x <= arr[hi]:

        # Prevent divide-by-zero infinite recursion
        if arr[hi] == arr[lo]:
            if arr[lo] == x:
                return lo, depth
            d = depth
            depth = 0
            return -1, d

        # Probing the position
        pos = int(lo + ((hi - lo) // (arr[hi] - arr[lo])) * (x - arr[lo]))

        # Found
        if arr[pos] == x:
            d = depth
            depth = 0
            return pos, d

        # Right side
        if arr[pos] < x:
            return interpolation_search(arr, pos + 1, hi, x)

        # Left side
        if arr[pos] > x:
            return interpolation_search(arr, lo, pos - 1, x)

    d = depth
    depth = 0
    return -1, d