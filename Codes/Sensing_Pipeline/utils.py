import datetime
import numpy as np
import pandas as pd
from sklearn import preprocessing
import time
import math


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


def calculate_ratio(tag, end_time, sensor_t, s_list, ang_list):
    global cnt_exp
    polarity = tag[0][2] + tag[1][2] + tag[2][2]
    dis_1, dis_2, ratio, dis_noSWA1, dis_noSWA2, ratio_noSWA = calculate_dis(tag, sensor_t, s_list, ang_list)
    t2 = time.time() * 1000 * 1000
    file1 = open("results.txt", "a")  # append mode
    t = str(datetime.datetime.now())

    speed_info = "(" + str(tag[0][3]) + ", " + str(tag[1][3]) + ", " + str(tag[2][3]) + ")"
    angle_info = "(" + str(tag[0][4]) + ", " + str(tag[1][4]) + ", " + str(tag[2][4]) + ")"
    peak_info = "(" + str(tag[0][1]) + ", " + str(tag[1][1]) + ", " + str(tag[2][1]) + ")"
    file1.write("Tag of Exp." + str(
        cnt_exp) + ": Polarities:" + polarity + ", Angle:" + angle_info + ", Speeds:" + speed_info + ", Peaks:"
                + peak_info + ", Dis_1:" + str(dis_1) + " m, Dis_2:"
                + str(dis_2) + " m, Ratio:" + str(ratio) +
                ", Dis_noSWA1:" + str(dis_noSWA1) + " m, Dis_noSWA2:"
                + str(dis_noSWA2) + " m, Ratio_noSWA:" + str(ratio_noSWA) + ", T1:" + str(end_time) + " us, T2:" + str(
        t2) + " us, Delta t:" + str(t2 - end_time) + " us]\n")

    cnt_exp += 1
    print(t + ":", "Detected a tag",
          "(Polarities=" + polarity + ", Ratio=" + str(ratio) + ")")



def calculate_dis(tag, sensor_t, s_list, ang_list):
    dis_noSWA, dis = [0, 0], [0, 0]
    # extract the speed and angle of the tag
    angles = [ang_list[tag[0][1] - 1000 - 1: tag[1][1] - 1000 - 1],
              ang_list[tag[1][1] - 1000 - 1: tag[2][1] - 1000 - 1]]
    speeds = [s_list[tag[0][1] - 1000 - 1:tag[1][1] - 1000 - 1], s_list[tag[1][1] - 1000 - 1:tag[2][1] - 1000 - 1]]

    int_points = [tag[1][1] - tag[0][1], tag[2][1] - tag[1][1]]
    for i in range(len(int_points)):
        for j in range(0, int_points[i]):
            v = speeds[i][j][1]
            ang = angles[i][j][1]
            dis_noSWA[i] += v / 3.6 * sensor_t
            dis[i] += ((v / 3.6 * sensor_t) * math.cos(abs(ang - angles[0][0][1]) * math.pi / 180))
    # The distance between the two sensors and the tag with and without SWA data
    return dis[0], dis[1], dis[1] / dis[0], dis_noSWA[0], dis_noSWA[1], dis_noSWA[1] / dis_noSWA[0]


# Read the raw magnetic field data of one sensor from the csv file
def xyz_sensor(file_name, sensor_num, flag=0):
    file = pd.read_csv(file_name)
    df = pd.DataFrame(file)
    total_sensor_list = []
    sensor_x, sensor_y, sensor_z = [], [], []
    for i in range(len(df)):
        document = df[i:i+1]
        sensor = list(map(float, document[sensor_num][i][1:-1].split(', ')))
        sensor_x.append(sensor[0])
        sensor_y.append(sensor[1])
        sensor_z.append(sensor[2])
    # Normalize the data
    if(flag):
        sensor_x = preprocessing.scale(sensor_x)
        sensor_y = preprocessing.scale(sensor_y)
        sensor_z = preprocessing.scale(sensor_z)
    return sensor_x, sensor_y, sensor_z