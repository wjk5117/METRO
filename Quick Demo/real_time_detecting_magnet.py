import multiprocessing as mp
import pandas as pd
import numpy as np
import datetime
import binascii
import serial
import struct
import time

from scipy.signal import savgol_filter


def gaussian(x, pos, wid):
    g = np.exp(-((x - pos) / (0.60056120439323 * wid)) ** 2)
    return g


def getInterval(t1, t2):
    df_1 = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S.%f")
    df_2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S.%f")
    if (df_2 - df_1).microseconds > 0:
        return float(str(df_2 - df_1)[7:])
    else:
        return
    

# ------------Experiment Settings-------------
scenario = "Detecting_magnet_"
cnt_exp = 1
# Number of sensors (Sensor 1 and Sensor 2)
num = 2
# experiment times
times = 1
# COM port for connecting Arduino
COM = 'COM11'


# ---------Initial Parameters and Thresholds---------
# These parameters and thresholds are empirically determined for the specific sensors used
# May need to finetune to optimize results if used different sensors
wnd = 15  # Gaussian Smoother for the raw signal data
wnd_d = 5  # Gaussian Smoother for the 1st derivative data
SG_wnd = 5 # Savgol filter window size
delta_thrd_z = ([16] * num for _ in range(1))
amp_thrd_z = ([1.5] * num for _ in range(1))
# Speed info: km/h
default_speed = 10
cur_speed = 5
# Time threshold to eliminate the duplicate detection of 
# the same magnet from two adjacent sensors
delta_t = 0.0025 * 50 * default_speed / cur_speed


# Constants and Globals
raw_result = []
raw_name = ['Time Stamp'] + ['Sensor ' + str(i) for i in range(1, num + 1)]
no_z = 0  # total number of peaks
n = 0  # index for the data points

# raw z-axis data, smoothed z-axis data, 1st derivative of z-axis data, smoothed 1st derivative of z-axis data
z, sz, dz, sdz = ([[] for _ in range(num)] for _ in range(4))
# slope and raw data list of z-axis
slope_list_z, raw_list_z = ([[] for _ in range(num)] for _ in range(2))
slope_thrd_z = [10000] * num
estimate_z = [True] * num
LastRAW_z = [0] * num  # Record the index of the last peak
N_flag_z, S_flag_z = ([0] * num for _ in range(2))

SmoothVector_r = gaussian(np.arange(wnd + 1)[1:], wnd / 2, wnd / 2)
SmoothVector_r = SmoothVector_r / (np.sum(SmoothVector_r))
SmoothVector_d = gaussian(np.arange(wnd_d + 1)[1:], wnd_d / 2, wnd_d / 2)
SmoothVector_d = SmoothVector_d / (np.sum(SmoothVector_d))

sensors = np.zeros((num, 3))
data = bytearray(4 * (3 * num + 1))
cnt = 1
current = 0


# Detect the magnet in real time
def detectMag():
    print("Begin detecting at", str(datetime.datetime.now()))
    arduino = serial.Serial(port=COM, baudrate=921600, timeout=None)
    arduino.flushInput()
    t = []
    global cnt, current, no_z, n_z, n, cnt_exp, z, sz, dz, sdz
    global slope_thrd_z, slope_list_z, estimate_z, raw_result, raw_list_z
    global delta_t
    try:
        while True:
            arduino.readinto(data)
            if cnt > 1000:  # discard headers
                raw_result_tmp = [current]
                for i in range(num):
                    sensors[i, 0], = struct.unpack('f', data[(i * 12):(4 + i * 12)])
                    sensors[i, 1], = struct.unpack('f', data[(i * 12 + 4):(8 + i * 12)])
                    sensors[i, 2], = struct.unpack('f', data[(i * 12 + 8):(12 + i * 12)])
                    raw_result_tmp.append((sensors[i, 0], sensors[i, 1], sensors[i, 2]))
                raw_result.append(raw_result_tmp)
                t.append(current)
                interval, = struct.unpack('f', data[(12 * num):(4 + 12 * num)])
                current += interval / 1000 / 1000


                # buffer some x-axis data points before starting the detection
                if n <= max(wnd, SG_wnd):
                    for i in range(num):
                        sz[i].append(sensors[i, 0])
                        dz[i].append(0)
                        sdz[i].append(0)
                    n += 1
                    continue

                # Smoothing the raw data
                for i in range(num):
                    sz[i].append(np.sum(SmoothVector_r * (np.array(z[i][-wnd:]))))

                # Savitzky–Golay filter for 1st derivative
                for i in range(num):
                    filtered = savgol_filter(sz[i][-SG_wnd:], SG_wnd, 2, deriv=1)
                    dz[i].append(filtered[(SG_wnd - 1) // 2])  # avoid boundary effect

                # smooth the 1st derivative
                for i in range(num):
                    sdz[i].append(np.sum(SmoothVector_d * (np.array(dz[i][-wnd_d:]))))

                for i in range(num):
                    N_flag_z[i] = 0
                    S_flag_z[i] = 0
                    if len(slope_list_z[i]) == 50:
                        if estimate_z[i]:
                            slope_thrd_z[i] = amp_thrd_z[i] * np.abs(np.array(slope_list_z[i][1:])).max()
                            print('X axis of sensor %d: Pre-done with slope threshold equaling to %.2f' % (
                                i + 1, slope_thrd_z[i]))
                            delta_time = (t[n] - t[n - 50]) / 50
                            print('Sampling rate: %.2f Hz' % (1 / delta_time))
                            estimate_z[i] = False
                            Last_z = str(datetime.datetime.now())

                    # Detect the N polarity
                    if sdz[i][-1] > 0 and sdz[i][-2] <= 0:
                        slope_z = (sdz[i][-1] - sdz[i][-2])
                        slope_list_z[i].append(slope_z)
                        raw_z = sz[i][n - int((wnd + 1) / 2)]
                        raw_list_z[i].append(raw_z)
                        if slope_z >= slope_thrd_z[i]:
                            if LastRAW_z[i] == 0:
                                Now_z = str(datetime.datetime.now())
                                t_interval_z = getInterval(Last_z, Now_z)
                                if t_interval_z > delta_t:
                                    N_flag_z[i] = 1
                                    Last_z = Now_z
                                # no = no + 1
                                # print('Sensor %d: No. %d detect a N' % (i+1, no))

                            else:
                                if raw_z - LastRAW_z[i] <= -delta_thrd_z[i]:
                                    Now_z = str(datetime.datetime.now())
                                    t_interval_z = getInterval(Last_z, Now_z)
                                    if t_interval_z > delta_t:
                                        N_flag_z[i] = 1
                                        Last_z = Now_z
                                    # no = no + 1
                                    # print('Sensor %d: No. %d detect a N' % (i+1, no))
                        else:
                            LastRAW_z[i] = raw_z

                    # Detect the S polarity
                    if sdz[i][-1] < 0 and sdz[i][-2] >= 0:
                        slope_z = (sdz[i][-1] - sdz[i][-2])
                        slope_list_z[i].append(slope_z)
                        raw_z = sz[i][n - int((wnd + 1) / 2)]
                        raw_list_z[i].append(raw_z)
                        if slope_z <= -slope_thrd_z[i]:
                            if LastRAW_z[i] == 0:
                                Now_x = str(datetime.datetime.now())
                                t_interval_z = getInterval(Last_z, Now_z)
                                if t_interval_z > delta_t:
                                    S_flag_z[i] = 1
                                    Last_z = Now_z
                                # no = no + 1
                                # print('Sensor %d: No. %d detect a S' % (i+1, no))
                            else:
                                if raw_z - LastRAW_z[i] >= delta_thrd_z[i]:
                                    Now_z = str(datetime.datetime.now())
                                    t_interval_z = getInterval(Last_z, Now_z)
                                    if t_interval_z > delta_t:
                                        S_flag_z[i] = 1
                                        Last_z = Now_z
                                    # no = no + 1
                                    # print('Sensor %d: No. %d detect a S' % (i+1, no))
                        else:
                            LastRAW_z[i] = raw_z

                    if np.sum(np.array(N_flag_z)) > 0:
                        # record tag start
                        no_z += 1
                        print('No. %d Overall: Detect a N' % no_z)
                    
                    if np.sum(np.array(S_flag_z)) > 0:
                        no_z += 1
                        print('No. %d Overall: Detect a S' % no_z)

                n = n + 1
            cnt += 1

    except KeyboardInterrupt:
        # Record the data
        print("Output csv")
        test = pd.DataFrame(columns=raw_name, data=raw_result)
        # Raw data
        test.to_csv("RawData_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        test_z = pd.DataFrame(columns=["THR_Z"], data=slope_thrd_z)
        # Thresholds
        test_z.to_csv("THR_Z_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")

        # Slope and raw data of x-axis
        for i in range(num):
            test_z = pd.DataFrame(columns=["Slope"], data=slope_list_z[i])
            test2_z = pd.DataFrame(columns=["Raw data"], data=raw_list_z[i])
            test_z.to_csv(
                'Slope_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
            test2_z.to_csv(
                'Raw_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
        print("Exited")



if __name__ == '__main__':
    detectMag()
