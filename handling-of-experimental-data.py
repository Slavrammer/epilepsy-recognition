import os
import pandas as pd

directory = input('Enter your path')

# Iteration over all csv files in working directory
for file in os.listdir(directory):
    if file.endswith(".txt"):
        file_name = str(file)
        print(file_name)
        # Reading data file
        data = pd.read_csv(file_name, delimiter='\t', names=['time', 'reference', 'signal'], skiprows=1)
        data = data.replace(',', '.', regex=True)
        data = data.astype(float)

        starting_treshold = 0.015
        counter = []

        # detection of signal rise
        for i in range(data.shape[0]):
            if data.iat[i, 2] > starting_treshold and len(counter) == 0:
                counter.append(i)
            elif data.iat[i, 2] < -starting_treshold and len(counter) == 0:
                counter.append(i)

        # cut start
        data = data[counter[0]:]

        # Time reset
        data.iloc[:, 0] = data.iloc[:, 0] - data.iloc[0, 0]

        time_single_package = 1
        delay = 0.2
        changer = 0

        # Data bins
        sig_packages = [list() for i in range(7)]

        # Populating lists with data
        for i in range(data.shape[0]):
            if data.iat[i, 0] < time_single_package:
                sig_packages[0].append(data.iat[i, 2])
            else:
                for k in range(1, 7):
                    if ((data.iat[i, 0] > (k * time_single_package + (k * time_single_package * delay))) and (
                            data.iat[i, 0] < ((1 + k) * time_single_package + (time_single_package * delay * k)))):
                        sig_packages[k].append(data.iat[i, 2])

        # Debugging
        sig_packages[0] = sig_packages[0][:-1]

        # parsing to dict
        obj = {}
        for x in range(7):
            obj[x] = sig_packages[x]

        # Saving
        df = pd.DataFrame(obj)
        df.to_csv(f'{file_name[:-8]}.csv', index=False, sep='\t')
