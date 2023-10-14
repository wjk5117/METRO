# Run a quick demo
This directory contains the code for runing a quick demo for METRO.
We provide a simplified code without connecting the CAN network of the vehicle.
Specifically, `real_time_detecting_magnet.py` provides the sensing algorithm for detecting the N/S polarity of a 90-degree passive magnet.
You only require to manufacture the sensor aaray and run the code with Python.
Then, you can get the N/S polarity in real time when you sliding a passive magnet above the sensor array.

To run the code correctly, you need to do following steps.

1. Manufacture the sensor array based on the [README](../PCBs/README.md) file in `../PCBs`.
For a quick demo, you can only build the MCU and one segment of the sensor array (e.g., "LeftBar1").

2. Compile and upload `Codes/Arduino/ReadSensor/ReadSensor.ino` to the sensor array with Arduino IDE. 
Note that the default code is implemented with a total of 14 MLX90393 magnetometer. 
You may need to set the number of the MLX90393 (on line 4) and the chip select pins (on line 8) based on your sensor array.

3. Before running `real_time_detecting_magnet.py`, you need to replace the number of magnetometer you used on line 31 and the serial port connects to the sensor array on line 35.

4. Run `real_time_detecting_magnet.py` and Move a passive magnet with a 90-degree polarity orientation (i.e., N-pole up or S-pole up) above the sensor array.
    - The default speed is set to 5 km/h, you can change the speed parameter on line 48. 
    - By default, the code can reliably detect the N/S polarities of a N52-grade cubic magnet with a size of 15 mm x 15 mm x 9.5 mm at a maximal height of ~30 cm.
    - You can of course use a small passive magnet by replacing the initial parameters and thresholds settings on line 41-51.

For the complete code implementation of the METRO system, please connect to the CAN network of a vehicle and run the codes in `../Codes`.`..Codes/Sensing_Pipeline`.