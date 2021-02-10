# PrácticaZWave

En este repositorio se recogen los códigos que ayudan a resolver la práctica sobre ZWave de la asignatura [Infraestructuras en IoT](http://cms.ual.es/UAL/estudios/masteres/plandeestudios/asignaturas/asignatura/MASTER7114?idAss=71143202&idTit=7114&anyo_actual=2018-19)

Los archivos que se encuentran en el repositorio son los siguientes:

- *iniciar_sesion.py*: Inicio se sesión en el software ZWay a través de un script de python. 
- *consultar_notificaciones.py*: Consulta de las notificaciones almacenadas en el software ZWay.
- *mqtt_publicador.py*: Script que manda un mensaje a través de MQTT.
- *mqtt_suscriptor.py*: Script que recibe un mensaje a través de MQTT.
- *zwave_obtener_notificaciones_tiempo_real.py*: Script que recibe notificaciones en tiempo real a través de la API de ZWay, las almacena en una base de datos y las envía con MQTT.
- *zwave_receptor.py*: Script que recibe las notificaciones en tiempo real a través de MQTT.

Las consultas a los datos almacenados en el software *Z-Way* se realizan a través de la API [ZwayHomeAutomation](https://zwayhomeautomation.docs.apiary.io/#)

En los *scripts* se han ocultado nombres de usuario y contraseñas. Antes de ejecutar cada *script* habrá que intoducir el usuario y contraseña correspondiente. 
