import math

import GenerateData
import L_Kaps as lkaps

import numpy as np



# Generate 1,000,000-sample array from exponential distribution
arr = GenerateData.generate_array(10**6, dist="exponential", seed=122654)
#arr = np.array(arr)

# Get best-fit distribution and total depth
best_name, best_score = lkaps.lkaps(arr)
print("Best fit:", best_name)


dists = lkaps.distributionList()
gen = dists[best_name]   # gen is your random sample generator



#------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

lam = 1
size = 10**6

N=size
mu, sigma = 3, 0.1
arr1 = np.sort(np.random.uniform(-1,0,100000))

print(lkaps.lkaps(arr1))

ind = [i for i in range(size)]


arr = GenerateData.generate_array(10**6, dist="exponential", seed=122654)

print(arr[0:50])
print(arr1[0:50])




#plt.plot(ind, arr)
plt.plot(arr1)
plt.show()
