# About
Repo for METRO

<!-- ![image](https://github.com/wjk5117/METRO/blob/main/Img/illustration.png) -->
![plot](./Img/illustration.png)


# Lisense
METRO is licensed under the MIT license included in the [LICENSE](./LICENSE) file.

# Setup
To use METRO, the following hardwares and development tools are required:
* [METRO's sensor array](#metros-sensor-array)
* [Arduino IDE](#arduino-ide-setup)
* [Python environment](#python-environment-setup)
* [PCAN-View](#connect-to-the-can-network)

## METRO's sensor array
We provide the manufacturing details of the METRO's sensor array in `/PCBs`, please see the related [README](./PCBs/README.md) file.

## Arduino IDE setup
Arduino IDE is used for programing the sensor array.

1. Download and install [Arduino IDE](https://www.arduino.cc/en/software)
2. Configure Arduino IDE for the Teensy 4.1 Development Board, according to the [official instruction](https://www.pjrc.com/teensy/td_download.html)
3. Install the Adafruit MLX90393 Library for Arduino IDE:




## Python environment setup
The sensing pipeline of METRO system is implemented based on Python language.

1. Install the python environment. You can use or anaconda
2. Install all dependencies listed in `./Code/Requirements.txt` using 'pip install \<package-name\>'


## Connect to the CAN network
To get the velocity and steering angle data from the CAN network of a vehicle, a [PCAN-USB adapter](https://www.peak-system.com/PCAN-USB.199.0.html?&L=1) for connecting the vehicle and the offical software [PCAN-View](https://www.peak-system.com/PCAN-View.242.0.html?&L=1) is required.

# Run a Quick Demo

# Citing METRO