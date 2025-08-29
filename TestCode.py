
## NOTE: This is a test code still under development, requiring many bug fixes and alterations


import random


# Questions:
# Do we take the lower,upper or middle value of subarray to find the low and high in the interpolation formula


def thingy(start, end, arr, T, k, divisor):

    if end - start < k:
        k = k // divisor

    low = arr[start]
    high = arr[end-1]

    pos = ((T - low)*(k))/(high - low)


    subStart = int((end-start) * (pos//1)/k) + start
    subEnd = int((end-start) * (pos//1 + 1)/k) + start

    if T < arr[subStart]:
        subStart = start
    elif T > arr[subEnd]:
        subEnd = end

    if k >= 3:
        thingy(subStart, subEnd, arr, T, k, divisor)
    else:
        print(f"start[{subStart}] = {arr[subStart]}, end[{subEnd}] = {arr[subEnd]}")



arr = []
for i in range(-10000,10000):
    arr.append(random.randint(i*10, (i+1)*10))

thingy(0, len(arr), arr, 687, 10, 2)