# This file is executed on every boot (including wake-boot from deepsleep)
import config
import machine, network, esp, os, gc, webrepl

try:
    import usocket as socket
except:
    import socket

debug = True
if not debug:
    esp.osdebug(None)
    os.dupterm(None, 1)  # disable REPL on UART(0)
    

def connect_sta():
    """ Connect to LAN """
    sta = network.WLAN(network.STA_IF)
    sta.active(config.STA_ACTIVE)
    if config.STA_ACTIVE:
        sta.config(dhcp_hostname=config.STA_HOSTNAME)
        if not sta.isconnected():
            sta.connect(config.STA_CREDENTIALS)
            while not sta.isconnected():
                pass
            if debug:
                print(sta.ifconfig())


def create_ap():
    """ Create Access point """
    ap = network.WLAN(network.AP_IF)
    ap.active(config.AP_ACTIVE)
    if config.AP_ACTIVE:
        ap.config(essid=config.AP_SSID, password=config.AP_PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)
        while not ap.active():
            pass
        if debug:
            print(ap.ifconfig())


gc.collect()
connect_sta()
create_ap()
webrepl.start()
