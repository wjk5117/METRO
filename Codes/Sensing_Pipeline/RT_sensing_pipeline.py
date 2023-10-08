import multiprocessing as mp
import serial
import struct
import pandas as pd
import binascii
import can
from can.bus import BusState
from scipy.signal import savgol_filter
from utils import *

# ------------ Parameter tuning -------------
scenario = "Test_"
cnt_exp = 1
num = 14 # Number of sensors
times = 1
# COM port for Arduino
COM = 'COM11'

# --------- Empirical Parameters & Thresholds ---------
# These are empirical parameters and thresholds for sensing
# May need to finetune for better results if used different sensors
wnd = 15  # Gaussian Smoother for the raw signal
wnd_d = 5  # Gaussian Smoother for the 1st derivative
SG_wnd = 5
delta_thrd_x, delta_thrd_z = ([16] * num for _ in range(2))
amp_thrd_x, amp_thrd_z = ([1.5] * num for _ in range(2))
default_speed = 10
cur_speed = 20
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

SmoothVector_r = gaussian(np.arange(wnd + 1)[1:], wnd / 2, wnd / 2)
SmoothVector_r = SmoothVector_r / (np.sum(SmoothVector_r))
SmoothVector_d = gaussian(np.arange(wnd_d + 1)[1:], wnd_d / 2, wnd_d / 2)
SmoothVector_d = SmoothVector_d / (np.sum(SmoothVector_d))
sensors = np.zeros((num, 3))

data = bytearray(4 * (3 * num + 1))
cnt = 1
current = 0

tag_z = []
cnt_mag = 0
fs = 400
speed_list, angle_list = [], []


# Get velocity and steering wheel angle data (SWA)
def readSpeed_SWA(listFrames, listFrames2):
    BUS = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate=500000)
    BUS.state = BusState.PASSIVE
    while True:
        msg = BUS.recv(1)
        if msg is not None:
            # CAN bus id of speed data: 036A
            if msg.arbitration_id == int('036a', 16):
                bin_data = binascii.hexlify(msg.data)[8:12].decode("utf-8")
                if bin_data[0] == '3':
                    listFrames.append([msg.timestamp * 1000 * 1000, 0.0])
                else:
                    listFrames.append([msg.timestamp * 1000 * 1000, int(bin_data[1] + bin_data[2:], 16) / 64])

            # CAN bus id of SWA data: 0704
            if msg.arbitration_id == int('0704', 16):
                bin_data = binascii.hexlify(msg.data)[2:6].decode("utf-8")
                listFrames2.append([msg.timestamp * 1000 * 1000, (int(bin_data, 16) - 9650) * 0.1 / 9.65])


def detectMag(listFrames, listFrames2):
    print("Begin detecting at", str(datetime.datetime.now()))
    arduino = serial.Serial(port=COM, baudrate=921600, timeout=None)
    arduino.flushInput()
    t = []
    global cnt, current, no_x, no_z, n_x, n, cnt_mag, cnt_exp, x, z
    global slope_thrd_x, slope_thrd_z, slope_list_x, slope_list_z, estimate_x, estimate_z, raw_result, raw_list_x, raw_list_z
    global speed_list, angle_list, delta_t
    try:
        while True:
            arduino.readinto(data)
            if cnt > 1000:  # discard headers
                if listFrames[-1][1] != 0:
                    delta_t = 0.0025 * 50 * default_speed / listFrames[-1][1]
                    # used for fuse detection results from two adjacent sensors that detect the same magent
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

                # buffer some data firstly
                if n <= max(wnd, SG_wnd):
                    for i in range(num):
                        sz[i].append(sensors[i, 2])
                        dz[i].append(0)
                        sdz[i].append(0)
                    n += 1
                    continue

                # Smoothing the raw data
                for i in range(num):
                    sz[i].append(np.sum(SmoothVector_r * (np.array(z[i][-wnd:]))))

                # Savitzky–Golay filter for 1st derivative
                for i in range(num):
                    filtered = savgol_filter(sz[i][-SG_wnd:], SG_wnd, 1, deriv=1)
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
                            print('Z axis of sensor %d: Pre-done with slope threshold equaling to %.2f' % (
                                i + 1, slope_thrd_z[i]))
                            delta_time = (t[n] - t[n - 50]) / 50
                            print('Sampling rate: %.2f Hz' % (1 / delta_time))
                            estimate_z[i] = False
                            Last_z = str(datetime.datetime.now())

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
                    file1 = open("Data/23_9_25_TrafficJam/results.txt", "a")
                    if np.sum(np.array(N_flag_z)) > 0:
                        # record tag start
                        no_z += 1
                        # speed, angle = listFrames[-1][1], listFrames2[-1][1]
                        print(str(datetime.datetime.now()) + ":", "speed is " + str(speed_list[-1][1]) + ";",
                              "SWA is " + str(angle_list[-1][1]) + ";", 'z axis detects No. %d N;' % no_z,
                              "peak index is " + str(cnt) + '\n')
                        file1.write(str(datetime.datetime.now()) + ": speed is " + str(
                            speed_list[-1][1]) + "; " + "SWA is " + str(
                            angle_list[-1][1]) + "; z axis detects No." + str(no_z) + " N; " + "peak index is " + str(
                            cnt) + '\n')
                        t1 = time.time() * 1000 * 1000
                        tag_z.append([cnt_mag, cnt, "N", speed_list[-1][1], angle_list[-1][1]])
                        cnt_mag += 1
                        if cnt_mag == 3:
                            print("Tag info:", tag_z)
                            calculate_ratio(tag_z, t1, delta_time, speed_list, angle_list)
                            cnt_mag = 0
                            tag_z.clear()

                    if np.sum(np.array(S_flag_z)) > 0:
                        no_z += 1
                        # t_s = process_time()

                        # t_e = process_time()
                        # print("Time of speed:", t_e-t_s)
                        print(str(datetime.datetime.now()) + ":", "speed is " + str(speed_list[-1][1]) + ";",
                              "SWA is " + str(angle_list[-1][1]), 'Z axis detects No. %d S polarity;' % no_z,
                              "peak index is " + str(cnt) + '\n')
                        file1.write(str(datetime.datetime.now()) + ": speed is " + str(
                            speed_list[-1][1]) + "; " + "SWA is " + str(
                            angle_list[-1][1]) + "; z axis detects No." + str(no_z) + " S; " + "peak index is " + str(
                            cnt) + '\n')
                        t1 = time.time() * 1000 * 1000
                        tag_z.append([cnt_mag, cnt, "S", speed_list[-1][1], angle_list[-1][1]])
                        cnt_mag += 1
                        if cnt_mag == 3:
                            print("Tag info:", tag_z)
                            calculate_ratio(tag_z, t1, delta_time, speed_list, angle_list)
                            cnt_mag = 0
                            tag_z.clear()
                n = n + 1
            cnt += 1

    except KeyboardInterrupt:
        print("Output csv")
        test = pd.DataFrame(columns=raw_name, data=raw_result)
        test.to_csv("Data/23_9_25_TrafficJam/RawData_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        test_z = pd.DataFrame(columns=["THR_Z"], data=slope_thrd_z)
        test_z.to_csv("Data/23_9_25_TrafficJam/THR_Z_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")

        test_speed = pd.DataFrame(columns=["Time Stamp", "Speed"], data=speed_list)
        test_speed.to_csv(
            "Data/23_9_25_TrafficJam/RawSpeed_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")
        test_SWA = pd.DataFrame(columns=["Time Stamp", "SWA"], data=angle_list)
        test_SWA.to_csv(
            "Data/23_9_25_TrafficJam/RawSWA_" + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + ".csv")

        for i in range(num):
            test_z = pd.DataFrame(columns=["Slope"], data=slope_list_z[i])
            test2_z = pd.DataFrame(columns=["Raw data"], data=raw_list_z[i])
            test3_z = pd.DataFrame(columns=["Index"], data=AuxiliaryNum_z[i])
            test_z.to_csv(
                'Data/23_9_25_TrafficJam/Slope_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
            test2_z.to_csv(
                'Data/23_9_25_TrafficJam/Raw_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
            test3_z.to_csv(
                'Data/23_9_25_TrafficJam/Num_Z_' + scenario + "_" + str(cur_speed) + "kmh_" + str(times) + "_S" + str(
                    i + 1) + '.csv')
        print("Exited")



if __name__ == '__main__':
    shared_list = mp.Manager().list()
    shared_list_SWA = mp.Manager().list()
    p1 = mp.Process(target=readSpeed_SWA, args=(shared_list, shared_list_SWA,))
    p1.start()
    p2 = mp.Process(target=detectMag, args=(shared_list, shared_list_SWA,))
    p2.start()
    p1.join()
    p2.join()
