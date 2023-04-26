import serial
import pymysql
import time

device = "/dev/ttyACM0"

arduino = serial.Serial(device, 9600)

data = arduino.readline().decode("ASCII")



dbConn = pymysql.connect(host="localhost",user="",password="",database="temperature_db") or die("Cannot connect to database")

#print(dbConn)
while 1:
    print(data)
    cursor = dbConn.cursor()
    cursor.execute("INSERT INTO tempLog (temperature) values (%s)" % (data))
    dbConn.commit()
    cursor.close()
    time.sleep(3)