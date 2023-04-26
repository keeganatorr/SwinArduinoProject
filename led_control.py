import serial
import pymysql
import time
import threading
import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

# Dictionary of pins with name of pin and state ON/OFF
pins = {
    2 : {'name' : 'PIN 2', 'state' : 0 },
    3 : {'name' : 'PIN 3', 'state' : 0 }
    }
    
# Main function when accessing the website
@app.route("/")
def index():
    # TODO: Read the status of the pins ON/OFF and update dictionary

    
    #This data wii be sent to index.html (pins dictionary)
    templateData = { 'pins' : pins }

    data = showData()
    
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData, data=data)

@app.route("/", methods=['POST'])
def index_post():
    # TODO: Read the status of the pins ON/OFF and update dictionary
    text = request.form['light']
    print(text)

    #This data wii be sent to index.html (pins dictionary)
    templateData = { 'pins' : pins }

    data = showData()
    
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData, data=data)

# Function with buttons that toggle depending on the status
@app.route("/<changePin>/<toggle>")
def toggle_function(changePin, toggle):
    # Convert the pin from the URL into an interger:
    changePin = int(changePin)
    # Get the device name for the pin being chnaged:
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code intended below:
    if toggle == "on":
        #Set the pin high
        if changePin == 2:
            arduino.write(b"1")
            pins[changePin]['state'] = 1
        if changePin == 3:
            arduino.write(b"3")
            pins[changePin]['state'] = 1
        #Save the status message to be passed into the template:
        message = "Turned" + deviceName + "on."
    if toggle == "off":
        if changePin == 2:
            arduino.write(b"2")
            pins[changePin]['state'] = 0
        if changePin == 3:
            arduino.write(b"4")
            pins[changePin]['state'] = 0
        #Set the pin low
        message = "Turned" + deviceName + "off."
    
    #This data wii be sent to index.html (pins dictionary)
    templateData = { 'pins' : pins }

    data = showData()
    
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData, data=data)

#Function to send simple commands
@app.route("/<action>")
def action(action):
    if action == 'action1':
        arduino.write(b"1")
        pins[2]['state'] = 1
    if action == 'action2':
        arduino.write(b"2")
        pins[2]['state'] = 0
    if action == 'action3':
        arduino.write(b"3")
        pins[3]['state'] = 1
    if action == 'action4':
        arduino.write(b"4")
        pins[3]['state'] = 0
    
    #This data wii be sent to index.html (pins dictionary)
    templateData = { 'pins' : pins }

    data = showData()
    
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData, data=data)

@app.route("/delete")
def delete():

    cursor = dbConn.cursor()
    cursor.execute("DELETE FROM tempLog where tempId > 0")
    dbConn.commit()
    cursor.close()

    cursor = dbConn.cursor()
    cursor.execute("ALTER TABLE tempLog AUTO_INCREMENT = 1")
    dbConn.commit()
    cursor.close()

    templateData = { 'pins' : pins }

    data = showData()
    
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData, data=data)


def readThread():
    while 1:
        data = arduino.readline().decode('ASCII')
        if data:
            print(data)
            cursor = dbConn.cursor()
            cursor.execute("INSERT INTO tempLog (time, temperature, temp2) values (\'{0}\', \'{1}\', \'{2}\')".format(datetime.datetime.now(), data.strip(), data.strip()))
            dbConn.commit()
            cursor.close()
            time.sleep(2)

def showData():
    cur = dbConn.cursor()
    cur.execute("select * from tempLog")
    return cur.fetchall()

# Main function, set up serial bus, indicate port for the webserver,
# ans start the service.
if __name__ == '__main__':
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    arduino.flush()
    dbConn = pymysql.connect(host="localhost",user="keegan",password="",database="temperature_db") or die("Cannot connect to database")
    x = threading.Thread(target=readThread)
    x.start()
    app.run(host='0.0.0.0', port = 80, debug = True)