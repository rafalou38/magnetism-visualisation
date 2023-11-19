import serial
import datetime
import time

ser = serial.Serial('COM1')  # open serial port
print(ser.name)         # check which port was really used


file = None

print("En attente du démarrage.")
# ser.write(b'hello')     # write a string
while True:
    line = ser.readline()
    print(line)

    if("START" in line):
        if(file != None):
            file.close()
        path = f"data-{time.time()}.csv"
        file = open(path, "w")
        print(path, "created")
    elif ("END" in line):
        print("done")
        file.close()
        # break
    else:
        file.write(line)

ser.close()             # close port