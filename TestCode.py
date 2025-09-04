
## NOTE: This is a test code still under development, requiring many bug fixes and alterations


import random


# Questions:
# Do we take the lower,upper or middle value of subarray to find the low and high in the interpolation formula

depth = 1

def thingy(start, end, arr, T, k, divisor):

    global depth
    print(depth)
    depth += 1

    if start == end:
        print(f"Found at arr[{start}] = {arr[start]}")
        return True

    if end - start <= k:
        k = k // divisor

    low = arr[start]
    high = arr[end]

    pos = ((T - low)*(k))/(high - low)


    subStart = int((end-start) * (pos//1)/k) + start
    subEnd = int((end-start) * (pos//1 + 1)/k) + start
    if T < arr[subStart]:
        subStart = start
    elif T > arr[subEnd]:
        subEnd = end

    if k >= 3 and subEnd - subStart > 1:
        thingy(subStart, subEnd, arr, T, k, divisor)
    else:

        print(f"start[{subStart}] = {arr[subStart]}, end[{subEnd}] = {arr[subEnd]}")
        return True



arr = []
for i in range(-678900, 1000000):
    arr.append(random.randint(i*10, (i+1)*10))

output = thingy(0, len(arr)-1, arr, 687, 10, 2)