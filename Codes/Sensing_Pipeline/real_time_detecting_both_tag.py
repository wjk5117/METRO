'''
Detect both information and line tags
X-axis: used for detecting information tags (0-degree)
Z-axis: used for detecting line tags (90-degree)
'''
import multiprocessing as mp
import pandas as pd
import numpy as np
import datetime
import binascii
import serial
import struct
import time
import can

from can.bus import BusState
from can.interfaces.pcan.basic import *
from scipy.signal import savgol_filter
from AMN_denoise import *
from utils import *


# ------------Experiment Settings-------------
scenario = "Detecting_both_tag_"
cnt_exp = 1
# Number of sensors
num = 14
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
delta_thrd_x, delta_thrd_z = ([16] * num for _ in range(2))
amp_thrd_x, amp_thrd_z = ([1.5] * num for _ in range(2))
# Speed info: km/h
default_speed = 10
cur_speed = 20
# Time threshold to eliminate the duplicate detection of 
# the same magnet from two adjacent sensors
delta_t = 0.0025 * 50 * default_speed / cur_speed


# Constants and Globals
raw_result = []
raw_name = ['Time Stamp'] + ['Sensor ' + str(i) for i in range(1, num + 1)]
no_x, no_z = 0, 0  # total number of peaks
n = 0  # index for the data points

x, sx, dx, sdx, z, sz, dz, sdz = ([[] for _ in range(num)] for _ in range(8))
slope_list_x, slope_list_z, raw_list_x, raw_list_z = ([[] for _ in range(num)] for _ in range(4))
slope_thrd_x, slope_thrd_z = ([10000] * num for _ in range(2))
estimate_x, estimate_z = ([True] * num for _ in range(2))
LastRAW_x, LastRAW_z = ([0] * num for _ in range(2))  # Record the time of last peak
N_flag_x, S_flag_x, N_flag_z, S_flag_z = ([0] * num for _ in range(4))



# def gaussian(x, pos, wid):
#     g = np.exp(-((x - pos) / (0.60056120439323 * wid)) ** 2)
#     return g
SmoothVector_r = gaussian(np.arange(wnd + 1)[1:], wnd / 2, wnd / 2)
SmoothVector_r = SmoothVector_r / (np.sum(SmoothVector_r))
SmoothVector_d = gaussian(np.arange(wnd_d + 1)[1:], wnd_d / 2, wnd_d / 2)
SmoothVector_d = SmoothVector_d / (np.sum(SmoothVector_d))
sensors = np.zeros((num, 3))

data = bytearray(4 * (3 * num + 1))
cnt = 1
current = 0

tag_x = []
cnt_mag = 0
speed_list, angle_list = [], []
# For denoising wheel noise
denoise_list_lx, denoise_list_ly, denoise_list_lz, denoise_list_rx, denoise_list_ry, denoise_list_rz = ([] for _ in range(6))
ref_list_lx, ref_list_ly, ref_list_lz, ref_list_rx, ref_list_ry, ref_list_rz = ([] for _ in range(6))


# Get velocity and steering wheel angle data (SWA) from CAN Bus
def read_Speed_SWA(listFrames, listFrames2):
    BUS = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate=500000)
    BUS.state = BusState.PASSIVE
    while True:
        msg = BUS.recv(1)
        if msg is not None:
            # CAN ID of the testing EV's speed data : 036A
            if msg.arbitration_id == int('036a', 16):
                bin_data = binascii.hexlify(msg.data)[8:12].decode("utf-8")
                if bin_data[0] == '3':
                    listFrames.append([msg.timestamp * 1000 * 1000, 0.0])
                else:
                    # Decode the speed data
                    listFrames.append([msg.timestamp * 1000 * 1000, int(bin_data[1] + bin_data[2:], 16) / 64])

            # CAN ID of the testing EV's SWA data: 0704
            if msg.arbitration_id == int('0704', 16):
                bin_data = binascii.hexlify(msg.data)[2:6].decode("utf-8")
                # Decode the SWA data
                listFrames2.append([msg.timestamp * 1000 * 1000, (int(bin_data, 16) - 9650) * 0.1 / 9.65])


# Detect the magnet in real time
def detectMag(listFrames, listFrames2):
    print("Begin detecting at", str(datetime.datetime.now()))
    arduino = serial.Serial(port=COM, baudrate=921600, timeout=None)
    arduino.flushInput()
    t = []
    global cnt, current, no_x, no_z, n_x, n, cnt_mag, cnt_exp, x, z, sx, sz, dx, dz, sdx, sdz, LastRAW_x, LastRAW_z
    global slope_thrd_x, slope_thrd_z, slope_list_x, slope_list_z, estimate_x, estimate_z, raw_result, raw_list_x, raw_list_z
    global speed_list, angle_list, delta_t
    global denoise_list_lx, denoise_list_ly, denoise_list_lz, denoise_list_rx, denoise_list_ry, denoise_list_rz
    global ref_list_lx, ref_list_ly, ref_list_lz, ref_list_rx, ref_list_ry, ref_list_rz
    try:
        while True:
            arduino.readinto(data)
            if cnt > 1000:  # discard headers
                if listFrames[-1][1] != 0:
                    # Update the time threshold according to the current speed
                    delta_t = 0.0025 * 50 * default_speed / listFrames[-1][1]
                    raw_result_tmp = [current]
                for i in range(num):
                    sensors[i, 0], = struct.unpack('f', data[(i * 12):(4 + i * 12)])
                    sensors[i, 1], = struct.unpack('f', data[(i * 12 + 4):(8 + i * 12)])
                    sensors[i, 2], = struct.unpack('f', data[(i * 12 + 8):(12 + i * 12)])
                    raw_result_tmp.append((sensors[i, 0], sensors[i, 1], sensors[i, 2]))
                raw_result.append(raw_result_tmp)
                speed_list.append([current, listFrames[-1][1]])
                angle_list.append([current, listFrames2[-1][1]])
                t.append(current)
                interval, = struct.unpack('f', data[(12 * num):(4 + 12 * num)])
                current += interval / 1000 / 1000
                
                '''
                Denoise the wheel noise with a slide window of 50 points, step size = 1 point
                '''
                # default left front sensor: sensor 6 (index 5)
                # default left reference sensor: sensor 7 (index 6)
                denoise_list_lx.append(sensors[5, 0])
                ref_list_lx.append(sensors[6, 0])
                denoise_list_ly.append(sensors[5, 1])
                ref_list_ly.append(sensors[6, 1])
                denoise_list_lz.append(sensors[5, 2])
                ref_list_lz.append(sensors[6, 2])

                # default right front sensor: sensor 13 (index 12)
                # default right reference sensor: sensor 14 (index 13)
                denoise_list_rx.append(sensors[12, 0])
                ref_list_rx.append(sensors[13, 0])
                denoise_list_ry.append(sensors[12, 1])
                ref_list_ry.append(sensors[13, 1])
                denoise_list_rz.append(sensors[12, 2])
                ref_list_rz.append(sensors[13, 2])

                if len(denoise_list_lx) == 50:
                    # denoise left front sensor data
                    denoised_lx, denoised_ly, denoised_lz = real_time_LMS(denoise_list_lx, denoise_list_ly, denoise_list_lz, ref_list_lx, ref_list_ly, ref_list_lz)
                    # denoise right front sensor data
                    denoised_rx, denoised_ry, denoised_rz = real_time_LMS(denoise_list_rx, denoise_list_ry, denoise_list_rz, ref_list_rx, ref_list_ry, ref_list_rz)

                    # update the denoised data
                    sensors[5, 0], sensors[5, 1], sensors[5, 2] = denoised_lx[-1], denoised_ly[-1], denoised_lz[-1]
                    # denoised right front sensor data
                    sensors[12, 0], sensors[12, 1], sensors[12, 2] = denoised_rx[-1], denoised_ry[-1], denoised_rz[-1]
        
                    # update the denoise and reference list
                    denoise_list_lx, denoise_list_ly, denoise_list_lz = denoise_list_lx[1:], denoise_list_ly[1:], denoise_list_lz[1:]
                    denoise_list_rx, denoise_list_ry, denoise_list_rz = denoise_list_rx[1:], denoise_list_ry[1:], denoise_list_rz[1:]
                    ref_list_lx, ref_list_ly, ref_list_lz = ref_list_lx[1:], ref_list_ly[1:], ref_list_lz[1:]
                    ref_list_rx, ref_list_ry, ref_list_rz = ref_list_rx[1:], ref_list_ry[1:], ref_list_rz[1:]


                for i in range(num):
                    z[i].append(sensors[i, 2])
                    x[i].append(sensors[i, 0])
                    
                # buffer x-axis and z-axis data before starting the detection
                if n <= max(wnd, SG_wnd):
                    for i in range(num):
                        sx[i].append(sensors[i, 0])
                        dx[i].append(0)
                        sdx[i].append(0)

                        sz[i].append(sensors[i, 2])
                        dz[i].append(0)
                        sdz[i].append(0)
                    n += 1
                    continue

                # Smoothing the raw data
                for i in range(num):
                    sx[i].append(np.sum(SmoothVector_r * (np.array(x[i][-wnd:]))))
                    sz[i].append(np.sum(SmoothVector_r * (np.array(z[i][-wnd:]))))

                # Savitzky–Golay filter for 1st derivative
                for i in range(num):
                    filtered = savgol_filter(sx[i][-SG_wnd:], SG_wnd, 5, deriv=1)
                    dx[i].append(filtered[(SG_wnd - 1) // 2])  # avoid boundary effect
                    
                    filtered_z = savgol_filter(sz[i][-SG_wnd:], SG_wnd, 1, deriv=1)
                    dz[i].append(filtered_z[(SG_wnd - 1) // 2])  # avoid boundary effect

                # smooth the 1st derivative
                for i in range(num):
                    sdx[i].append(np.sum(SmoothVector_d * (np.array(dx[i][-wnd_d:]))))
                    sdz[i].append(np.sum(SmoothVector_d * (np.array(dz[i][-wnd_d:]))))

                '''
                Detect the infomaion tag, x-axis data
                '''
                for i in range(num):
                    N_flag_x[i] = 0
                    S_flag_x[i] = 0
                    if len(slope_list_x[i]) == 50:
                        if estimate_x[i]:
                            slope_thrd_x[i] = amp_thrd_x[i] * np.abs(np.array(slope_list_x[i][1:])).max()
                            print('X axis of sensor %d: Pre-done with slope threshold equaling to %.2f' % (
                                i + 1, slope_thrd_x[i]))
                            delta_time = (t[n] - t[n - 50]) / 50
                            print('Sampling rate: %.2f Hz' % (1 / delta_time))
                            estimate_x[i] = False
                            Last_x = str(datetime.datetime.now())

                    # Detect the N polarity
                    if sdx[i][-1] > 0 and sdx[i][-2] <= 0:
                        slope_x = (sdx[i][-1] - sdx[i][-2])
                        slope_list_x[i].append(slope_x)
                        raw_x = sx[i][n - int((wnd + 1) / 2)]
                        raw_list_x[i].append(raw_x)
                        if slope_x >= slope_thrd_x[i]:
                            if LastRAW_x[i] == 0:
                                Now_x = str(datetime.datetime.now())
                                t_interval_x = getInterval(Last_x, Now_x)
                                if t_interval_x > delta_t:
                                    N_flag_x[i] = 1
                                    Last_x = Now_x
                                # no = no + 1
                                # print('Sensor %d: No. %d detect a N' % (i+1, no))

                            else:
                                if raw_x - LastRAW_x[i] <= -delta_thrd_x[i]:
                                    Now_x = str(datetime.datetime.now())
                                    t_interval_x = getInterval(Last_x, Now_x)
                                    if t_interval_x > delta_t:
                                        N_flag_x[i] = 1
                                        Last_x = Now_x
                                    # no = no + 1
                                    # print('Sensor %d: No. %d detect a N' % (i+1, no))
                        else:
                            LastRAW_x[i] = raw_x

                    # Detect the S polarity
                    if sdx[i][-1] < 0 and sdx[i][-2] >= 0:
                        slope_x = (sdx[i][-1] - sdx[i][-2])
                        slope_list_x[i].append(slope_x)
                        raw_x = sx[i][n - int((wnd + 1) / 2)]
                        raw_list_x[i].append(raw_x)
                        if slope_x <= -slope_thrd_x[i]:
                            if LastRAW_x[i] == 0:
                                Now_x = str(datetime.datetime.now())
                                t_interval_x = getInterval(Last_x, Now_x)
                                if t_interval_x > delta_t:
                                    S_flag_x[i] = 1
                                    Last_x = Now_x
                                # no = no + 1
                                # print('Sensor %d: No. %d detect a S' % (i+1, no))
                            else:
                                if raw_x - LastRAW_x[i] >= delta_thrd_x[i]:
                                    Now_x = str(datetime.datetime.now())
                                    t_interval_x = getInterval(Last_x, Now_x)
                                    if t_interval_x > delta_t:
                                        S_flag_x[i] = 1
                                        Last_x = Now_x
                                    # no = no + 1
                                    # print('Sensor %d: No. %d detect a S' % (i+1, no))
                        else:
                            LastRAW_x[i] = raw_x

                    file1 = open("results.txt", "a")
                    if np.sum(np.array(N_flag_x)) > 0:
                        # record tag start
                        no_x += 1
                        # speed, angle = listFrames[-1][1], listFrames2[-1][1]
                        print(str(datetime.datetime.now()) + ":", "speed is " + str(speed_list[-1][1]) + ";",
                              "SWA is " + str(angle_list[-1][1]) + ";", 'x axis detects No. %d N;' % no_x,
                              "peak index is " + str(cnt) + '\n')
                        file1.write(str(datetime.datetime.now()) + ": speed is " + str(
                            speed_list[-1][1]) + "; " + "SWA is " + str(
                            angle_list[-1][1]) + "; x axis detects No." + str(no_x) + " N; " + "peak index is " + str(
                            cnt) + '\n')
                        t1 = time.time() * 1000 * 1000
                        tag_x.append([cnt_mag, cnt, "N", speed_list[-1][1], angle_list[-1][1]])
                        cnt_mag += 1
                        # Tag prototype consists of 3 magnets
                        if cnt_mag == 3:
                            print("Tag info:", tag_x)
                            # calculate the distance ratio of the tag
                            calculate_ratio(tag_x, t1, delta_time, speed_list, angle_list)
                            cnt_mag = 0
                            tag_x.clear()

                    if np.sum(np.array(S_flag_x)) > 0:
                        no_x += 1
                        print(str(datetime.datetime.now()) + ":", "speed is " + str(speed_list[-1][1]) + ";",
                              "SWA is " + str(angle_list[-1][1]), 'x axis detects No. %d S polarity;' % no_x,
                              "peak index is " + str(cnt) + '\n')
                        file1.write(str(datetime.datetime.now()) + ": speed is " + str(
                            speed_list[-1][1]) + "; " + "SWA is " + str(
                            angle_list[-1][1]) + "; x axis detects No." + str(no_x) + " S; " + "peak index is " + str(
                            cnt) + '\n')
                        t1 = time.time() * 1000 * 1000
                        tag_x.append([cnt_mag, cnt, "S", speed_list[-1][1], angle_list[-1][1]])
                        cnt_mag += 1
                        # Tag prototype consists of 3 magnets
                        if cnt_mag == 3:
                            print("Tag info:", tag_x)
                            calculate_ratio(tag_x, t1, delta_time, speed_list, angle_list)
                            cnt_mag = 0
                            tag_x.clear()


                '''
                Detect the line tag, z-axis data
                '''
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
                                Now_z = str(datetime.datetime.now())
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
                        print("Detect the N polarity of 90-degree magnet")
                        print("Warning lane departure from the solid line!")
                    
                    if np.sum*np.array(S_flag_z) > 0:
                        print("Detect the S polarity of 90-degree magnet")
                        print("Warning lane departure from the dashed line!")

                n = n + 1
            cnt += 1


    except KeyboardInterrupt:
        # Record the data
        print("Output csv")
        test = pd.DataFrame(columns=raw_name, data=raw_result)
        # Raw data
        test.to_csv("RawData_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        test_x = pd.DataFrame(columns=["THR_X"], data=slope_thrd_x)
        test_z = pd.DataFrame(columns=["THR_Z"], data=slope_thrd_z)
        # Thresholds
        test_x.to_csv("THR_X_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        test_z.to_csv("THR_Z_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        # Raw speed and SWA data
        test_speed = pd.DataFrame(columns=["Time Stamp", "Speed"], data=speed_list)
        test_speed.to_csv(
            "RawSpeed_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        test_SWA = pd.DataFrame(columns=["Time Stamp", "SWA"], data=angle_list)
        test_SWA.to_csv(
            "RawSWA_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")

        # Slope and raw data of x-axis
        for i in range(num):
            test_x = pd.DataFrame(columns=["Slope"], data=slope_list_x[i])
            test2_x = pd.DataFrame(columns=["Raw data"], data=raw_list_x[i])
            test_z = pd.DataFrame(columns=["Slope"], data=slope_list_z[i])
            test2_z = pd.DataFrame(columns=["Raw data"], data=raw_list_z[i])
            test_x.to_csv(
                'Slope_X_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
            test2_x.to_csv(
                'Raw_X_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
            test_z.to_csv(
                'Slope_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
            test2_z.to_csv(
                'Raw_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
        print("Exited")



if __name__ == '__main__':
    shared_list = mp.Manager().list()
    shared_list_SWA = mp.Manager().list()
    p1 = mp.Process(target=read_Speed_SWA, args=(shared_list, shared_list_SWA,))
    p1.start()
    p2 = mp.Process(target=detectMag, args=(shared_list, shared_list_SWA,))
    p2.start()
    p1.join()
    p2.join()
