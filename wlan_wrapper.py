import time
import network

wlan = None


def restart_wifi(ssid, key, hostname, timeout=None):
    global wlan
    if wlan is None:
        return False
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    wlan.connect(ssid, key)
    start_time = time.time()
    wlan.config(dhcp_hostname=hostname)
    while not wlan.isconnected():
        if timeout is not None:
            if time.time()-start_time > timeout:
                return False
    print('network config:', wlan.ifconfig())
    print('dhcp hostname', wlan.config('dhcp_hostname'))
    return True


def init_wifi(ssid, key, hostname, timeout=None):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while wlan.status() != network.STAT_IDLE:
        print('Waiting ifup for wlan'.format(wlan.status()))
    wlan.config(dhcp_hostname=hostname)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        start_time = time.time()
        while not wlan.isconnected():
            if timeout is not None:
                if time.time()-start_time > timeout:
                    return False
    print('network config:', wlan.ifconfig())
    print('dhcp hostname', wlan.config('dhcp_hostname'))
    return True