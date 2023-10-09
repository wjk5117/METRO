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
    scale_THR = 1
    offset_THR = 28
    new_z = [scale_THR * new_z[i] + offset_THR for i in range(len(new_z))]

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
    plt.tight_layout()
    plt.show()

    # return sz[NFilt-1:]-y, the filterred signal with noise removed
    return sz[NFilt-1:]-y


# Rotation transformation
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


# Determine the scale and offset thresholds
def determine_THR(x, y):
    x = np.array(x)
    y = np.array(y)

    # Calculate the scale_THR and offset_THR using linear regression
    n = len(x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    # Calculate scale_THR using the formula
    numerator = np.sum((x - mean_x) * (y - mean_y))
    denominator = np.sum((x - mean_x) ** 2)
    scale_THR = numerator / denominator
    # Calculate offset_THR using the formula
    offset_THR = mean_y - scale_THR * mean_x

    return scale_THR, offset_THR


# Real-time LMS filter
def real_time_LMS(front_x, front_y, front_z, ref_x, ref_y, ref_z):
    '''
    implement the LMS function in real time
    return the filterred data
    '''

    # LMS filter parameters
    NFilt = 4
    mu = 0.000001
    f = pa.filters.FilterLMS(n=NFilt, mu=mu, w="random")
    
    # Coordinate alignment
    new_ref_x, new_ref_y, new_ref_z = rotation3d(ref_x, ref_y, ref_z)

    # Determine the scale and offset thresholds
    scale_THR_x, offset_THR_x = determine_THR(new_ref_x, front_x)
    scale_THR_y, offset_THR_y = determine_THR(new_ref_y, front_y)
    scale_THR_z, offset_THR_z = determine_THR(new_ref_z, front_z)

    # Data scaling and offsetting
    new_ref_x = [scale_THR_x * new_ref_x[i] + offset_THR_x for i in range(len(new_ref_x))]
    new_ref_y = [scale_THR_y * new_ref_y[i] + offset_THR_y for i in range(len(new_ref_y))]
    new_ref_z = [scale_THR_z * new_ref_z[i] + offset_THR_z for i in range(len(new_ref_z))]

    # Update the input matrix
    x = pa.input_from_history(front_x, NFilt)
    # Apply the LMS filter
    d = new_ref_x[NFilt-1:]
    pred_x, e, w = f.run(d, x)

    y = pa.input_from_history(front_y, NFilt)
    d = new_ref_y[NFilt-1:]
    pred_y, e, w = f.run(d, y)

    z = pa.input_from_history(front_z, NFilt)
    d = new_ref_z[NFilt-1:]
    pred_z, e, w = f.run(d, z)

    denoise_x = front_x[NFilt-1:]-pred_x
    denoise_y = front_y[NFilt-1:]-pred_y
    denoise_z = front_z[NFilt-1:]-pred_z
    return denoise_x, denoise_y, denoise_z




if __name__ == "__main__":
    file = "test.csv"
    LMS(file)