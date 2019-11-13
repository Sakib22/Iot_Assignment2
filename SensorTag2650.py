import time
import json
import struct
import sensortag
import paho.mqtt.publish as mqtt


#declared variable with specific address of our sensortag
sensor = '54:6C:0E:B5:76:04'

#used bluepy library "sensortag" to create tag where all
#the sensor data can be accessed
tag = sensortag.SensorTag(sensor)

#this is printed if sensortag is able to be detected and connected
#to the pi
print ("Connected to SensorTag", sensor)

sensorOn  = struct.pack("B", 0x01)
sensorbarcal =  struct.pack("B", 0x02)
sensorMagOn = struct.pack("H", 0x0007)
sensorGyrOn = struct.pack("H", 0x0007)
sensorAccOn = struct.pack("H", 0x0038)

#this enables data from the sensor
tag.IRtemperature.enable()
tag.humidity.enable()
tag.barometer.enable()
tag.accelerometer.enable()
tag.lightmeter.enable()



base_topic = 'assignment1/cc2650/%s' % sensor.replace(':', '').lower()

while True:
    msgs = []
    
    #sensor data is read after enabling
    ambient_temp, target_temp = tag.IRtemperature.read()
    ambient_temp, rel_humidity = tag.humidity.read()
    ambient_temp, pressure_millibars = tag.barometer.read()
    x_accel, y_accel, z_accel = tag.accelerometer.read()
    light = tag.lightmeter.read()
    
    #array of all the sensor data
    data = {
        'ambient_temp'  : ambient_temp,
        'target_temp'   : target_temp,
        'humidity'      : rel_humidity,
        'millibars'     : pressure_millibars,
        'tst'           : int(time.time()),
    }
    
    #prints the array of the sensortag data
    payload = json.dumps(data)
    print (light)
    
    #allows client to specifying which sensor data they want
    #by extending the message
    msgs.append((base_topic, payload, 0, False))
    for k in data:
        msgs.append( ( "%s/%s" % (base_topic, k), data[k], 0, False ) )
    
    #hostname is the server of mqtt
    mqtt.multiple(msgs, hostname='test.mosquitto.org')

    time.sleep(10)

tag.disconnect()