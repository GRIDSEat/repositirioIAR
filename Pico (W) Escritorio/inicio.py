import network, utime, machine



#   Replace the following with your WIFI Credentials
#SSID = "Fibertel WiFi508 2.4GHz"
SSID = "moto g13"
#SSID_PASSWORD = "01417755106"
SSID_PASSWORD = "albertthomas"

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()