#!/usr/bin/python

# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SHT31
# This code is designed to work with the SHT31_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SHT31_I2CS#tabs-0-product_tabset-2
# Minor modifications: 2017-02-05 by Claus Kuehnel info@ckuehnel.ch  
# Tested w/ Grove SHT31 module

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# SHT31 address, 0x44(68)
# Send measurement command, 0x2C(44)
#		0x06(06)	High repeatability measurement
bus.write_i2c_block_data(0x44, 0x2C, [0x06])

time.sleep(0.5)

# SHT31 address, 0x44(68)
# Read data back from 0x00(00), 6 bytes
# Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
data = bus.read_i2c_block_data(0x44, 0x00, 6)

# Convert the data
temp = data[0] * 256 + data[1]
cTemp = round((-45 + (175 * temp / 65535.0)),1)
#fTemp = -49 + (315 * temp / 65535.0)
humidity = round((100 * (data[3] * 256 + data[4]) / 65535.0),1)

# Output data to screen
print "Temperature in Celsius is : %.2f C" %cTemp
#print "Temperature in Fahrenheit is : %.2f F" %fTemp
print "Relative Humidity is : %.2f %%RH" %humidity

f = open("/home/TEMP","w")
f.write(str(cTemp))
f.close()

f = open("/home/HUMI","w")
f.write(str(humidity))
f.close() 
