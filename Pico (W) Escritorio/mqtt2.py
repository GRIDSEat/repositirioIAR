from lib.urdm6300 import Rdm6300             #Lectora de tarjeta RFID
import ubinascii
from lib.umqtt.simple import MQTTClient
import machine
from machine import Pin, I2C,RTC
from ssd1306 import SSD1306_I2C          #Displat OLED
import baseDato
from time import sleep
import _thread

import time
card_id1 = 0
card_id = 0


    
#*************************************************************************************************
#*                            Núcleo 0  Comunicación MQTT                                        *
#*************************************************************************************************   
#-------------------------------------------------------
#                  Configura oled
#-------------------------------------------------------
WIDTH =128 
HEIGHT= 32
i2c=I2C(1,scl=Pin(19),sda=Pin(26),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

oled.fill(0)
oled.text("IAR",20,0)       
oled.show()

#-------------------------------------------------------
#                  reloj
#-------------------------------------------------------
rtc = RTC()
rtc.datetime((2017, 8, 23, 2, 12, 48, 0, 0)) # set a specific date and
#--------------------------------------------------------------------
# Default  MQTT_BROKER to connect to
#--------------------------------------------------------------------
MQTT_BROKER = '192.168.0.144'
CLIENT_ID =  ubinascii.hexlify(machine.unique_id())
SUSCRIBE_USUARIO = b"topicoUsuario"
SUSCRIBE_INSTRUMENTAL = b"topicoInstrumental"
SUSCRIBE_SINCROTIEMPO = b"led"
PUBLISH_TOPIC = b"datoRegistradora"

#**********************************************************************************************
#*                          Núcleo 1 lectura de tarjeta RFID                                  *
#**********************************************************************************************
def nucleo1():
    
    global card_id
    lectura_rfid = Rdm6300()
  
    while True:
        time.sleep_ms(20)  #Tiempo entre 1 y 50 ms
        card_id = lectura_rfid.read_card()
        
        
        if card_id != None:
            if card_id1 != card_id:
                card_id1 = card_id
                print("el cardId es: "+card_id)
        else: card_id1 = 0
        
        
        
# Mensaje recibido con topico 
def llamada(topic, msg):
    if topic.decode() == "topicoUsuario":
        print(msg)
        datoBD = msg.decode()
        baseDato.alta(datoBD,"usuario")
    elif topic.decode() == "topicoInstrumento":
        print(msg)
        datoBD = msg.decode()
        baseDato.alta(datoBD,"instrumento")
        if msg.decode()=="verDatetime":
            print("Funcion recibida")
            diaHora=''
            tuplaTiempo = rtc.datetime()
            print(tuplaTiempo)
            stringSalidaFecha = f"{tuplaTiempo[0]}/ {tuplaTiempo[1]}/ {tuplaTiempo[2]}"
            stringSalidaHora  = f"{tuplaTiempo[4]}: {tuplaTiempo[5]}: {tuplaTiempo[6]}"
            oled.text("Hola",20,0)
            oled.fill(0)
            oled.text(stringSalidaFecha,20,0)
            oled.text(stringSalidaHora,10,20)        
            oled.show()
        else:
            oled.fill(0)
            oled.text(msg.decode(), 0, 15)   #Columna, fila
            oled.show()
    elif topic.decode()== "topicoInstrumental":
        oled.fill(0)
        oled.text("Hola",20,0)
        oled.text("COMO VA",10,20)        
        oled.show()
    
def reset():
    print("Resetting...")
    time.sleep_ms(1)
    machine.reset()
    
def nucleo0():
    print("nucleo 0")
    print (CLIENT_ID)
    global card_id
 
    mqttCliente = MQTTClient(CLIENT_ID, MQTT_BROKER)
    mqttCliente.set_callback(llamada)
    mqttCliente.connect()
    mqttCliente.subscribe(SUSCRIBE_SINCROTIEMPO)
    mqttCliente.subscribe(SUSCRIBE_USUARIO)
    mqttCliente.subscribe(SUSCRIBE_INSTRUMENTAL)
    print(f"Conectado al Brocker :: {MQTT_BROKER}, esperando llamada")
    while True:
            mqttCliente.check_msg()
            if card_id != None:
                
                mqttCliente.publish(PUBLISH_TOPIC, str(card_id).encode())
                    
                card_id = None
            time.sleep_ms(10)
            

        
segundo_hilo = _thread.start_new_thread(nucleo1,())
nucleo0()            
