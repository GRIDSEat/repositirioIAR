import time
import ubinascii
from lib.umqtt.simple import MQTTClient
import machine
from machine import Pin, I2C,RTC
from lib.ssd1306.ssd1306 import SSD1306_I2C
import baseDato
from time import sleep
import _thread
from lib.urdm6300 import Rdm6300
import time

card_id1 = 0
card_id = 0



def nucleo1():
    global card_id
    lectura_rfid = Rdm6300()
    while True:
        time.sleep_ms(45)  #Tiempo entre 1 y 50 ms
        card_id = lectura_rfid.read_card()
        if card_id != None:
            if card_id1 != card_id:
                return(card_id)
                card_id1 = card_id
        else: card_id1 = 0
    
    
    

#-------------------------------------------------------
#                  Configura oled
#-------------------------------------------------------
WIDTH =128 
HEIGHT= 32
#i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
#oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
#-------------------------------------------------------
#                  reloj
#-------------------------------------------------------
rtc = RTC()
rtc.datetime((2017, 8, 23, 2, 12, 48, 0, 0)) # set a specific date and

# Default  MQTT_BROKER to connect to
MQTT_BROKER = '192.168.0.144'
#MQTT_BROKER = '192.168.137.1'
CLIENT_ID =  ubinascii.hexlify(machine.unique_id())
SUBSCRIBE_TOPIC = b"datoPersonal"
PUBLISH_TOPIC = b"datoRegistradora"

# Publish MQTT messages after every set timeout
last_publish = time.time()
publish_interval = 5

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    #print((topic, msg))
    datoBD = msg.decode()
    baseDato.altas(datoBD)

    
    
    """
    if msg.decode()=="verDatetime":
        diaHora=''
        tuplaTiempo = rtc.datetime()
        print(tuplaTiempo)
        stringSalidaFecha=f"{tuplaTiempo[0]}/ {tuplaTiempo[1]}/ {tuplaTiempo[2]}"
        stringSalidaHora=f"  {tuplaTiempo[4]}: {tuplaTiempo[5]}: {tuplaTiempo[6]}"
       
        oled.fill(0)
        oled.text(stringSalidaFecha,20,0)
        oled.text(stringSalidaHora,10,20)        
        oled.show()
    else:
        oled.fill(0)
        oled.text(msg.decode(), 0, 15)   #Columna, fila
        oled.show()
    """

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    

    
def nucleo0():
    global card_id
    print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(SUBSCRIBE_TOPIC)
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")
    while True:
            # Non-blocking wait for message
            mqttClient.check_msg()
            global last_publish
            if (time.time() - last_publish) >= publish_interval:
                print (card_id)
                mqttClient.publish(PUBLISH_TOPIC, str(card_id).encode())
                last_publish = time.time()
            time.sleep(1)

    
if __name__ == "__main__":
    while True:
        try:
            segundo_hilo = _thread.start_new_thread(nucleo1,())
            nucleo0()
          
        except OSError as e:
            print("Error: " + str(e))
            #reset()


