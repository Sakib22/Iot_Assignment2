#! /usr/bin/env python
import serial
from serial import Serial
import time
EV3 = serial.Serial('/dev/rfcomm0')
print "Listening for EV3 Bluetooth messages, press CTRL C to quit."
try:   
    while 1:      
        n = EV3.inWaiting()      
        if n <> 0:
            s = EV3.read(n)
            EV3.write(s)         
            
            for n in range(len(s)):            
                print "x%02X" % ord(s[n]),         
            
            numberOfBytes = ord(s[0]) + ord(s[1])*25
            numberOfCounter = ord(s[2]) + ord(s[3])*256
            
            s = s[6:]
            
            mailboxNameLength = ord(s[0])
            mailboxName = s[1:1+mailboxNameLength-1]
            
            s = s[mailboxNameLength+1: ]
            
            payloadLength = ord(s[0]) + ord(s[1])*256
            payload = s[2:2+payloadLength-1]
            
            print "\t", mailboxName, ",", payload
            
        else:         
        # No data is ready to be processed         
            time.sleep(0.5)
except KeyboardInterrupt:   
    pass
EV3.close()

