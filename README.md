# About
This directory contains all code implementation and hardware designs for METRO.

As a brief summary, road surface markings, like symbols and line markings, are vital
traffic infrastructures for driving safety and efficiency. However,
real-world conditions can impair the utility of existing road markings. For example, adverse weather conditions such as snow and
rain can quickly obliterate visibility.

We propose a novel MagnETic ROad marking system (METRO)
for robust recognition of road markings at low cost and high deployability. METRO pairs (a) easily deployable passive magnetic road
markings with (b) an automotive-grade magnetic sensing framework that detects and interprets these markings. The design of
METRO addresses several real-world challenges, such as mitigating
the impact of magnetic disturbances, lowering deployment costs,
and enhancing the durability of magnetic tags. On-road field tests of
METRO demonstrate an overall accuracy of over 96% in interpreting
various road markings in adverse conditions with less cost (only
$0.17 per meter) than traditional road markings ($0.21-7.70 per meter). Our field evaluation of METRO over one month demonstrates
the practicality and robustness of METRO in real-world settings.


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
After this step, you can see the boad information when you click the Tools menu item:
  ![plot](./Img/teensy_arduino_configuration.png)

3. Install the Adafruit MLX90393 Library for Arduino IDE:
    - Click 'Sketch' --> 'Include Library' --> 'Manage Libraries...'
    ![plot](./Img/sensor_arduino_library.png)
    - Search for Adafruit MLX90393, and install the Adafruit MLX90393 library:
    ![plot](./Img/install_MLX90393_library.png)




## Python environment setup
The sensing pipeline of METRO system is implemented based on Python language.

1. Install the python environment. You can install the [official python](https://www.python.org/downloads/) or [Anaconda](https://www.anaconda.com/download)
2. Install all dependencies listed in `./Code/Requirements.txt` using 'pip install \<package-name\>'


## Connect to the CAN network
To get the velocity and steering angle data from the CAN network of a vehicle, a [PCAN-USB adapter](https://www.peak-system.com/PCAN-USB.199.0.html?&L=1) for connecting the vehicle and the offical software [PCAN-View](https://www.peak-system.com/PCAN-View.242.0.html?&L=1) is required.

# Run a Quick Demo
We provide a quick demo without connecting the CAN network of a vehicle in `/Quick Demo`, please see the related [README](./Quick_Demo/README.md) file for more details.

# Citing METRO
If you use METRO in your research or wish to refer to the baseline results, please use the following BibTeX entry.