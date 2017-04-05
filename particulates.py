#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# particulates.py
# based on # SDS011_Feinstaub_Sensor.py
# Copyright 2017 by luetzel <webmaster_at_raspberryblog.de>
# Modifications by Claus Kuehnel <info@ckuehnel.ch> 2017-04-02 

import serial, time, struct

ser = serial.Serial()
ser.port = "/dev/ttyUSB0" # Set this to your serial port 
ser.baudrate = 9600 
ser.open() 
ser.flushInput()

CYCLE = 10 

print "Measuring Particulate Matter by nano PM sensor SDS011"
print "Cycle Time is %d sec" % (CYCLE)

def dump_data(d):
    print(' '.join(x.encode('hex') for x in d))

def process_frame(d):
    #dump_data(d) #debug
    r = struct.unpack('<HHxxBBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    print("PM 2.5: {} g/m^3  PM 10: {} g/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))

def sensor_read():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)
    d = ser.read(size=10)
    if d[0] == "\xc0":
        process_frame(byte + d)

while True:
    sensor_read()
    time.sleep(CYCLE)
