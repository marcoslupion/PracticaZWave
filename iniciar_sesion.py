import requests
#Direccion en la que se encuentra el servidor.
ip_raspberry = "localhost"
uri = "http://"+ip_raspberry+":8083/ZAutomation/api/v1/login"

#Credenciales del usuario
form_login = {"login": "***", "password": "****"}

#Consulta
uri_login = requests.post(uri, data=form_login)

#Respuesta de la API
respuesta_json = uri_login.json()
print(respuesta_json)

if respuesta_json["code"] == 401:
    print("Debe introducir las credenciales correctas")
elif respuesta_json["code"] == 200:
    print("El inicio de sesión se ha realizado correctamente")