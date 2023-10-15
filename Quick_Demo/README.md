# Run a quick demo
This directory contains the code to run a quick demo of METRO.
This demo has been simplified to work without the need for a connection to the vehicle's CAN network. 

Specifically, the file `real_time_detecting_magnet.py` contains the sensing algorithm for detecting the N/S polarity of a 90-degree passive magnet.
To use this, you only need to manufacture the sensor array in  `../PCBs` and run the code using Python. 
With this setup, you can obtain real-time N/S polarity information as you move the passive magnet over the sensor array.

To ensure the correct execution of the code, please follow these steps:

1. Manufacture the sensor array based on the [README](../PCBs/README.md) file in `../PCBs`.
For the quick demo, you can only build the MCU and just one segment of the sensor array (e.g., "LeftBar1").

2. Compile and upload the `Codes/Arduino/ReadSensor/ReadSensor.ino` to the sensor array using the Arduino IDE.
Note that the default code is designed for use with a total of 14 MLX90393 magnetometers.  
You may need to adjust the number of MLX90393 sensors (line 4) and their respective chip select pins (line 8) to match the configuration of your specific sensor array.

3. Before running the `real_time_detecting_magnet.py`, you also need to replace the number of magnetometers used on line 31 and specify the serial port connection to the sensor array on line 35 to match your setup.

4. Run the `real_time_detecting_magnet.py` and move a passive magnet with a 90-degree polarity orientation (i.e., N-pole up or S-pole up) over the sensor array.
    - The default speed is set to 1.8 km/h (0.5 m/s), you can modify the speed parameter on line 48 as needed. 
    - By default, the code is capable of consistently detecting the N/S polarities of an N52-grade cubic magnet measuring 15 mm x 15 mm x 9.5 mm at a maximum height of ~30 cm. If you wish to use a smaller passive magnet or at a larger height, you can adjust the initial parameters and threshold settings within lines 41-51.

For the full implementation of the METRO system, you need to establish a connection to the CAN network of a vehicle and then execute the code provided in the `..Codes/Sensing_Pipeline` directory.