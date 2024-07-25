from machine import Pin
from time import sleep
import dht

sensor = dht.DHT22(Pin(2))

def read_dht22():
    global temp, hum
    temp = hum = 0
    
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
 
        if (isinstance(temp, float) and isinstance(hum, float)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
            return(msg)
        else:
            return('Invalid sensor readings')
    except OSError as e:
        return('Failed to read sensor: {}'.format(e))
        
def web_page():
    html = """<!DOCTYPE HTML><html>
    <head>
        <title>DHT22</title>
    </head>
    <body>
        <h1>DHT22</h1>
        <p>Temp """ + str(temp) + """</p>
        <p>Hum """ + str(hum) + """</p>
    </body>
    </html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    if debug:
        print('Got a connection from {}'.format(str(addr)))
    request = conn.recv(1024)
    if debug:
        print('Content = {}'.format(request))
    sensor_readings = read_dht22()
    if debug:
        print(sensor_readings)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    sleep(2)