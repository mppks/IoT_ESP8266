## Settings file
Before uploading to the device, you need to create a settings file *config.py* with the following contents:
```
# The name and password of the WiFi network to which the sensor is connected,
# and the name of the device on the network
STA_ACTIVE = True
STA_SSID = 'WIFI_SSID'
STA_PASSWORD = 'WIFI_PASSWORD'
STA_HOSTNAME = 'DEVICE_NAME'

# Name and password of the created Access point
AP_ACTIVE = False
AP_SSID = 'ACCESS_POINT_NAME'
AP_PASSWORD = 'ACCESS_POINT_PASSWORD'

# MQTT server data
MQTT_SERVER = 'mqtt3.thingspeak.com'
MQTT_CLIENT_ID = ''
MQTT_USER = ''
MQTT_PASSWORD = ''
MQTT_CHANNEL_ID = ''
MQTT_PUB_TIME = 60
MQTT_TOPIC = 'channels/' + MQTT_CHANNEL_ID + '/publish'

SENSOR_READINGS_TIME = 50
```