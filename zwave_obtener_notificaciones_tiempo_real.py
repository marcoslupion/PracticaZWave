#Importacion de librerias
from pymongo import MongoClient
from datetime import datetime
from time import sleep
import requests
import paho.mqtt.client as mqtt
import json
import sys

#Conexion con la base de datos Mongo para guardar mis datos
client = MongoClient("mongodb+srv://user:pass@tfg-obcxa.gcp.mongodb.net/test?retryWrites=true")
db = client.test
sensor_data = db.sensor_data

#Conexion con MQTT en caso de ser necesario
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)

#URL del dispositivo (Raspberry Pi) que realiza la conexion con Razberry
ip_raspberry = "localhost"

#Funcion encargada de obtener nuevas notificaciones a partir de una notificacion data
def buscar_nuevas(ultima):

    #Se forma la consulta a la API especificando el momento actual, para recibir notificaciones a partir de ahora
    uri_get = "http://"+ip_raspberry+":8083/ZAutomation/api/v1/notifications?since="+str(ultima)

    #Se realiza la consulta GET
    respuesta = requests.get(uri_get, headers=headers).json()

    #Se obtienen los datos en formato JSON
    datos_notificaciones = respuesta["data"]["notifications"]

    #Se recorren las notificaciones recibidas
    for notificacion in datos_notificaciones:

        print(notificacion)
        #Se obtienen los datos importantes de la respuesta de la API
        datos_notificacion = {
            "value" : notificacion["message"]["l"],
            "name" : notificacion["message"]["dev"],
            "timestamp" : notificacion["timestamp"],
            "id" : notificacion["id"],
        }

        #Se gestionan los datos que se quieren guardar y enviar
        fecha_hora = datetime.fromtimestamp(int(datos_notificacion["id"])/1000).strftime('%d/%m/%Y %H:%M:%S')
        insertar = {
                "tipo" : "bin_sensor",
                "sensor" : datos_notificacion["name"],
                "valor" : (notificacion["message"]["l"]).upper(),
                "fecha_str" : fecha_hora,
                "datetime" :  datetime.strptime(fecha_hora, '%d/%m/%Y %H:%M:%S'),
                "timestamp" :int(datos_notificacion["id"])
        }

        #Se muestra la informacion que se quiere guardar
        print(insertar)

        #Se envia a mongo
        sensor_data.insert_one(insertar)

        #Se envia a un broker mqtt. Actualmente desactivado, pero esta seria la forma
        mqtt_client.publish("binario/"+datos_notificacion["name"], payload=json.dumps(datos_notificacion), qos=0, retain=False)

        #Se actualiza el valor de tiempo de la ultima notificacion para luego consultar en base a este valor
        ultima = int(notificacion["id"])+1

    return ultima


#Login a la API
uri = "http://"+ip_raspberry+":8083/ZAutomation/api/v1/login"
form_login = {"login": "****", "password": "****"}
uri_login = requests.post(uri, data=form_login)

#Respuesta de la API
respuesta_json = uri_login.json()

if respuesta_json["code"] == 401:
    print("Debe introducir las credenciales correctas")
    sys.exit()
elif respuesta_json["code"] == 200:
    print("El inicio de sesión se ha realizado correctamente")

#Almacena la cookie para mantener la sesion iniciada
cookie = respuesta_json["data"]["sid"]
headers = {
    'Content-Type': 'application/json',
    "Cookie" : "ZWAYSession="+cookie
}

#Instante de tiempo actual
timestamp_consulta = datetime.timestamp(datetime.now())*1000

#Bucle infinito encargado de obtener nuevas notificaciones
while True:
    print("Se ha realizado una consulta")
    timestamp_consulta = buscar_nuevas(timestamp_consulta)
    sleep(1)
