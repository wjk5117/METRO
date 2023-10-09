import matplotlib.pylab as plt
import padasip as pa
import numpy as np
import math

from utils import *


# LMS filter implementation
def LMS(file):
    # data from the front sensor (with noise from wheel rotation)
    sx, sy, sz = xyz_sensor(file, "Front_wheel_sensor")

    # data from the reference sensor (pure noise)
    nx, ny, nz = xyz_sensor(file, "Ref_sensor")
    N = len(nx)
    # coodinate alignment
    new_x, new_y, new_z = rotation3d(nx, ny, nz)
    # scale the data based on the raw data
    scale_THR = 28
    new_z = [new_z[i] + scale_THR for i in range(len(new_z))]


    # plt.plot(sz)
    # plt.plot(new_z)
    # plt.show()

    NFilt = 4
    x = pa.input_from_history(sz, NFilt) # input matrix
    d = new_z[NFilt-1:]
    
    # LMS filter from padasip package
    f = pa.filters.FilterLMS(n=NFilt, mu=0.000001, w="random")
    y, e, w = f.run(d, x)

    # show results
    plt.figure(figsize=(16,10))
    plt.subplot(311);plt.title("Raw data (signal + noise) of front sensor");plt.xlabel("Sample")
    plt.plot(sz[NFilt-1:], "b", label="Original data");plt.legend()
    plt.subplot(312);plt.title("Adaptation process");plt.xlabel("Sample")
    plt.plot(d,"b", label="Reference noise")
    plt.plot(y,"g", label="Output noise");plt.legend()
    plt.subplot(313);plt.title("Filterred signal (raw data - output noise)");plt.xlabel("Sample")
    plt.plot(sz[NFilt-1:]-y,"r", label="filterred signal");plt.legend()
    # plt.subplot(414);plt.title("Signal after direct subtraction (raw data - raw reference data)");plt.xlabel("Sample")
    # plt.plot([sz[i]-nx[i] for i in range(NFilt-1, len(nx))],"r", label="Subtracted signal");plt.legend()
    plt.tight_layout()
    plt.show()

    fs = 20
    sz_part = sz[2000:6000]
    d_part = d[2000:6000]
    y_part = y[2000:6000]
    denoise = sz_part - y_part
    x = [i/400 for i in range(len(sz_part))]
    # 
    plt.plot(x, sz_part)
    # plt.plot(x, )
    plt.tick_params(labelsize=fs)
    # plt.legend(fontsize=20)
    # plt.xticks(x, )
    plt.xlabel(r'Time (s)', fontsize=fs)
    plt.ylabel(r'Magnetometer reading (uT)', fontsize=fs)
    # plt.title(title, fontsize=fs)
    plt.show()

    plt.plot(x, d_part)
    # plt.plot(x, )
    plt.tick_params(labelsize=fs)
    # plt.legend(fontsize=20)
    # plt.xticks(x, )
    plt.xlabel(r'Time (s)', fontsize=fs)
    plt.ylabel(r'Magnetometer reading (uT)', fontsize=fs)
    # plt.title(title, fontsize=fs)
    plt.show()

    plt.plot(x, y_part)
    # plt.plot(x, )
    plt.tick_params(labelsize=fs)
    # plt.legend(fontsize=20)
    # plt.xticks(x, )
    plt.xlabel(r'Time (s)', fontsize=fs)
    plt.ylabel(r'Magnetometer reading (uT)', fontsize=fs)
    # plt.title(title, fontsize=fs)
    plt.show()

    plt.plot(x, denoise)
    # plt.plot(x, )
    plt.tick_params(labelsize=fs)
    # plt.legend(fontsize=20)
    # plt.xticks(x, )
    plt.xlabel(r'Time (s)', fontsize=fs)
    plt.ylabel(r'Magnetometer reading (uT)', fontsize=fs)
    # plt.title(title, fontsize=fs)
    plt.show()

    # return sz[NFilt-1:]-y, the filterred signal with noise removed
    return sz[NFilt-1:]-y



def readSensor(data, t_list, idx):  # To simulate the reading process
    if idx >= len(data):
        return -1, -1
    z = data[idx]
    t = t_list[idx]
    time.sleep(0.002)
    return z, t


def rotation3d(dx2, dy2, dz2):
    # rotation matrix
    alpha = -math.pi/2 #
    beta = math.pi/2  #
    gamma = math.pi/2 # 
    rotation_mat = np.array(
    [
        [math.cos(alpha)*math.cos(gamma)-math.cos(beta)*math.sin(alpha)*math.sin(gamma), math.sin(alpha)*math.cos(gamma)+math.cos(beta)*math.cos(alpha)*math.sin(gamma), math.sin(beta)*math.sin(gamma)], 
        [-math.cos(alpha)*math.sin(gamma)-math.cos(beta)*math.sin(alpha)*math.cos(gamma), -math.sin(alpha)*math.sin(gamma)+math.cos(beta)*math.cos(alpha)*math.cos(gamma), math.sin(beta)*math.cos(gamma)],
        [math.sin(beta)*math.sin(alpha), -math.sin(beta)*math.cos(alpha), math.cos(beta)]
    ])
    xyz = np.array([dx2, dy2, dz2])
    new_x, new_y, new_z = np.dot(rotation_mat, xyz)

    return new_x, new_y, new_z


cnt = 1
sig_list = []
# Real-time LMS filter
def RT_LMS(front_z, wheel_z):
    if len(sig_list) < n:
            sig_list.append(front_z)
    if len(sig_list) == n:
        x_input = pa.input_from_history(sig_list, n)[0]
        print(x_input)
        d = wheel_z
        sig_list.pop(0)
        # Simulate real-time prediction and update the filter
        y = filter_min_error.predict(x_input)
        filter_min_error.adapt(d, x_input)
        return front_z-y


if __name__ == "__main__":
    file = "test.csv"
    LMS(file)