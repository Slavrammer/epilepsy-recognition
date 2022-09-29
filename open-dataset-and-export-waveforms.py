import os
from scipy.io import arff
import pandas as pd
import numpy as np

def otwierac_policja(x):
    matrix = np.ones((136, 206))
    for k in range(136):
        z = df.iat[k, 0]
        labels_all.append(z[-1])
        z_bin = []
        for j in range(len(z) - 1):
            z_bin.append(float(z[j]))
        matrix[k] = matrix[k] * z_bin
    return matrix


# Working directory
os.chdir(input('Enter your path'))

data = arff.loadarff('EpilepsyDimension1_TRAIN.arff')
df = pd.DataFrame(data)
df = df.transpose()
labels_all = []
data = otwierac_policja(df)
data = data.iloc[:, 1:-1]

# Standardise so that signal does not fry the memristors
for i in range(data.shape[0]):
    data.iloc[i, :] = (data.iloc[i, :] - data.iloc[i, :].mean()) / data.iloc[i, :].std()

# Set zeros at the start and at the end (needed for Arbitrary Waveform Generator (ARB))
data['0'] = 0
data['205'] = 0

# Saving all the unpacked waveforms (ARB wanted separate files...)
for i in range(data.shape[0]):
    x = data.iloc[i, :]
    x.to_csv("{}.txt".format(i), index=False, header=False)
    
# Save labels
df_labels = pd.DataFrame(labels_all)
df_labels.to_csv('labels.csv')
