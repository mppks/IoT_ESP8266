from machine import Pin
from umqtt.simple import MQTTClient
import time, dht, config


def read_dht22():
    global temp, hum
    temp = hum = 0
    
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
 
        if (isinstance(temp, float) and isinstance(hum, float)):
            msg = ('{0:3.1f},{1:3.1f}'.format(temp, hum))
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


def mqtt_handle(mqtt_timer):
    try:
        payload = 'field1={0:3.1f}&field2={1:3.1f}'.format(temp, hum)
        mqtt.connect()
        mqtt.publish(config.MQTT_TOPIC, payload)
        mqtt.disconnect()
    except OSError as e:
        print('MQTT error: {}'.format(e))


def sensor_handle(sensor_timer):
    sensor_readings = read_dht22()
    if debug:
        print(sensor_readings)

sensor = dht.DHT22(Pin(2))

mqtt = MQTTClient(client_id=config.MQTT_CLIENT_ID, server=config.MQTT_SERVER,
                  user=config.MQTT_USER, password=config.MQTT_PASSWORD)

mqtt_timer = machine.Timer(0)
sensor_timer = machine.Timer(1)

mqtt_timer.init(period=config.MQTT_PUB_TIME*1000, mode=machine.Timer.PERIODIC, callback=mqtt_handle)
sensor_timer.init(period=config.SENSOR_READINGS_TIME*1000, mode=machine.Timer.PERIODIC, callback=sensor_handle)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 80))
sock.listen(5)

while True:
    try:
        conn, addr = sock.accept()
        if debug:
            print('Got a connection from {}'.format(str(addr)))

        request = conn.recv(1024)
        if debug:
            print('Content = {}'.format(request))

        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        print('Server error: {}'.format(e))
