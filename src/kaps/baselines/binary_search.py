# Python3 program to implement
# binary search with recursion

depth = 0

def binarySearch(arr, lo, hi, x):
    global depth
    depth += 1

    # Prevent excessive recursion (max depth safety)
    if depth > 998:              # adjust if needed
        return -1, depth

    # Valid range check
    if lo <= hi:

        mid = (lo + hi) // 2

        # Found
        if arr[mid] == x:
            d = depth
            depth = 0
            return mid, d

        # If x is larger → right half
        if arr[mid] < x:
            return binarySearch(arr, mid + 1, hi, x)

        # If x is smaller → left half
        if arr[mid] > x:
            return binarySearch(arr, lo, mid - 1, x)

    d = depth
    depth = 0
    return -1, d

