import antropy as ant
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

def Complexity(x):
    x1 = ant.perm_entropy(x, normalize=True)
    x2 = ant.spectral_entropy(x, sf=100, method='welch', normalize=True)
    x3 = ant.svd_entropy(x, normalize=True)
    x4 = ant.app_entropy(x)
    x5 = ant.sample_entropy(x)
    x6, x7 = ant.hjorth_params(x)
    x8 = ant.num_zerocross(x)
    x9 = ant.lziv_complexity('01111000011001', normalize=True)
    x10 = ant.katz_fd(x)
    x11 = ant.katz_fd(x)
    x12 = ant.higuchi_fd(x)
    x13 = ant.detrended_fluctuation(x)
    params = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13]
    return params


# Working directory
directory = os.chdir(input('Enter your path'))

# Data bins with parameter names, helped not get confused
perm_entropy_all = []
spectral_entropy_all = []
svd_entropy_all = []
approximate_entropy_all = []
sample_entropy_all = []
hjort_mobility = []
hjort_complexity = []
num_zerocross_all = []
num_lzivcomplexity_all = []
petrosian_all = []
katz_all = []
higuchi_all = []
dfa_all = []

dane = dict(perm_entropy=perm_entropy_all,
            spectral_entropy=spectral_entropy_all,
            svd_entropy=svd_entropy_all,
            approximate_entropy=approximate_entropy_all,
            sample_entropy=sample_entropy_all,
            hjort_mobility=hjort_mobility,
            hjort_complexity=hjort_complexity,
            num_zerocross_all=num_zerocross_all,
            num_lzivcomplexity_all=num_lzivcomplexity_all,
            petrosian_all=petrosian_all,
            katz_all=katz_all,
            higuchi_all=higuchi_all,
            dfa_all=dfa_all)

df = pd.DataFrame(dane)

# Dictionary with all 7 DataFrames with labels for 7 signal packets
obj = {}
for name in epoch:
    obj[name] = pd.DataFrame(dane)
print(obj)

# Iteration over all csv files in working directory
for file in os.listdir(directory):
    if file.endswith(".csv"):
        file_name = str(file)
        print(file_name)
        # Reading data file
        data = pd.read_csv(file_name, delimiter='\t', names=['1', '2', '3', '4', '5', '6', '7'], skiprows=1)
        data = data.astype(float)
        
        # Magic one-liner for populating the dictionary with calculated parameters
        for i in range(7):
            dic_key = i + 1
            obj[str(dic_key)].loc[len(obj[str(dic_key)].index)] = Complexity(data.iloc[:, i])

# Save to files
for i in obj:
    obj[i].to_csv(f"{i}.txt", index=False, sep='\t', header=df.columns.tolist())

