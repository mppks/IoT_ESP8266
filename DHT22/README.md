## Settings file
Before uploading to the device, you need to create a settings file *config.py* with the following contents:
```
# The name and password of the WiFi network to which the sensor is connected,
# and the name of the device on the network
STA_SSID = 'WIFI_SSID'
STA_PASSWORD = 'WIFI_PASSWORD'
STA_HOSTNAME = 'DEVICE_NAME'

# Name and password of the created Access point
AP_SSID = 'ACCESS_POINT_NAME'
AP_PASSWORD = 'ACCESS_POINT_PASSWORD'
```