# This file is executed on every boot (including wake-boot from deepsleep)
debug = True

import config

try:
    import usocket as socket
except:
    import socket

import esp
if debug:
    esp.osdebug(None)

import os, machine
if not debug:
    os.dupterm(None, 1) # disable REPL on UART(0)
    
import gc
gc.collect()

# Connect to LAN
import network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(dhcp_hostname = config.AP_HOSTNAME)
sta.connect(config.STA_SSID, config.STA_PASSWORD)

while sta.isconnected() == False:
    pass

if debug:
    print(sta.ifconfig())

# Create Access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid = config.AP_SSID, password = config.AP_PASSWORD, authmode = network.AUTH_WPA_WPA2_PSK)

while ap.active() == False:
    pass

if debug:
    print(ap.ifconfig())

# Start WebREPL
import webrepl
webrepl.start()