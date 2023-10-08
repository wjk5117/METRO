import datetime
import numpy as np
import time
import math
import pandas as pd


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


def calculate_ratio(file1, tag, end_time, sensor_t, s_list, ang_list):
    global cnt_exp
    polarity = tag[0][2] + tag[1][2] + tag[2][2]
    dis_1, dis_2, ratio, dis_noSWA1, dis_noSWA2, ratio_noSWA = calculate_dis(tag, sensor_t, s_list, ang_list)
    t2 = time.time() * 1000 * 1000
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
          "(Polarities=" + polarity + ", Ratio=" + str(ratio) + ")")  # ", Ratio_noSWA=" + str(ratio_noSWA) + ")")


def calculate_dis(tag, sensor_t, s_list, ang_list):
    dis_noSWA, dis = [0, 0], [0, 0]
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
    return dis[0], dis[1], dis[1] / dis[0], dis_noSWA[0], dis_noSWA[1], dis_noSWA[1] / dis_noSWA[0]


def save_dataframe(filename: str, columns: list, list_data: list) -> None:
    df = pd.DataFrame(columns=columns, data=list_data)
    df.to_csv(filename)