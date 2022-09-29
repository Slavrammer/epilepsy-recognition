import numpy as np
import os
import pandas as pd
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Working directory
directory = input("Enter path")

# def collecting(x, hv):
#     counter = hv
#     for i in range(x.shape[0]):
#         if (x.iat[i, 0] > hv - 0.005) and (x.iat[i, 0] < hv + 0.005):
#             peaks.append(x.iat[i, 1])
#             hv = hv + counter

sig_package_all = []
frequency_all = []
global_THD_all = []

# Iteration over all csv files in working directory
for file in os.listdir(directory):
    if file.endswith(".txt"):
        file_name = str(file)
        frequency = float(file_name[:-8])

        # Reading data file
        data = pd.read_csv(file_name, delimiter='\t', names=['time', 'reference', 'signal'], skiprows=1)
        data = data.replace(',', '.', regex=True)
        data = data.astype(float)

        starting_treshold = 0.01
        counter = []

        # detection of signal rise
        for i in range(data.shape[0]):
            if data.iat[i, 1] > starting_treshold and len(counter) == 0:
                counter.append(i)

        # cut start
        data = data[counter[0]:]

        # Normalization
        data.iloc[:, 0] = data.iloc[:, 0] - data.iloc[0, 0]
        
        # calculate lenght of the 10 signal packets
        time_single_package = (1 / frequency) * 10
        
        delay = 0.2
        changer = 0
        
        # Data bins
        sig_packages = [list() for i in range(4)]

        for i in range(data.shape[0]):
            if data.iat[i, 0] < time_single_package:
                sig_packages[0].append(data.iat[i, 2])
            else:
                # pass
                # POPRAW LICZBE
                for k in range(1, 4):
                    if ((data.iat[i, 0] > (k * time_single_package + (k * time_single_package * delay))) and (
                            data.iat[i, 0] < ((1 + k) * time_single_package + (time_single_package * delay * k)))):
                        sig_packages[k].append(data.iat[i, 2])

        # sample spacing
        T = 0.0004

        global_THD = []
        
        for i in range(len(sig_packages)):
            # Number of sample points
            N = len(sig_packages[i])

            y = np.array(sig_packages[i])
            yf = fft(y)

            xf = fftfreq(N, T)[:N // 2]
            yy = 2.0 / N * np.abs(yf[0:N // 2])
            df = pd.DataFrame(data=[xf, yy])
            df = df.transpose()
            # plt.plot(xf, yy)
            # plt.show()
            peaks = []
            counter = frequency
            # print('df shape')
            # print(df.shape[0])
            for i in range(df.shape[0]):
                if (df.iat[i, 0] > frequency - frequency*0.05) and (df.iat[i, 0] < frequency + frequency*0.05):
                    peaks.append(df.iat[i, 1])
                    # print(frequency)
                    frequency = frequency + counter
                    if len(peaks) > 10:
                        frequency = counter
                        break

            # peaks handling and THD calculations
            np_peaks = np.array(peaks)
            I_peak = np_peaks[0]
            np_peaks = np_peaks[1:]

            np_peaks_square = np_peaks * np_peaks
            sum = np.sum(np_peaks_square)
            square = np.sqrt(sum)

            thd = (square / I_peak)
            thd_r = (thd / (np.sqrt(1 + (thd * thd)))) * 100

            global_THD.append(thd_r)

            # Rysowanie wykresu po zakończeniu obliczeń THD dla wszystkich paczek
            if len(global_THD) == len(sig_packages):
                # plt.title('Częstotliwość {}'.format(frequency))
                # plt.xlabel('Numer paczki')
                # plt.ylabel('Całkowite zniekształcenie harmoniczne')
                # # PAMIĘTAJ ABY POPRAWI LICZBE PUNKTÓW
                # x_ax = [1, 2, 3, 4, 5]
                # plt.scatter(x_ax, global_THD)
                # plt.savefig('{}Hz.png'.format(frequency))
                # plt.clf()
                sig_packages_num = [1, 2, 3, 4]
                for j in range(len(sig_packages_num)):
                    sig_package_all.append(sig_packages_num[j])
                frequency_to_df = frequency * np.ones(4)
                for h in range(frequency_to_df.shape[0]):
                    frequency_all.append(frequency_to_df[h])
                for t in range(len(global_THD)):
                    global_THD_all.append(global_THD[t])
                # print('frequency_to_df.shape')
                # print(frequency_to_df.shape)
                # print('global')
                # print(len(global_THD))
                # plt.show()
                
# repeat three times for three different signal shapes (squ, sin, saw)
string = 'squ'
label = []
for i in range(88):
    label.append(string)
df = pd.DataFrame(data=[frequency_all, sig_package_all, global_THD_all, label])
df = df.transpose()
df.to_csv("data.txt", sep='\t', index=False, header=['Frequency', 'n', 'THD', 'label'])
