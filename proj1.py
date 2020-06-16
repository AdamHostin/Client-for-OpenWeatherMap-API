#!/usr/bin/env python3
#Datum: 25.2. 2019

import socket
import json
import sys
import re

#spracovanie argumentov
try:
	KEY= str(sys.argv[1])
except:
	print("key not specified")
	sys.exit()
try:
	CITY = str(sys.argv[2])
except:
	print("city not specified")
	sys.exit()

#priprava prace so socketom
req_string=    "GET /data/2.5/weather?q="+CITY+"&APPID="+KEY+"&units=metric&mode=json HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n"

HOST = 'api.openweathermap.org' 
PORT = 80

#praca so socketom
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(bytes(req_string,'utf-8'))
    data = s.recv(1024)

received_data = repr(data)


#spracovanie spravy
received_data=re.findall("{.*}",received_data)
received_data=re.sub("\"name\".*,","",received_data[0])
x = json.loads(received_data)
try:
	tmp_dic= x['weather'][0]
	description=tmp_dic['description']
except:
	description="not found"

try:
	tmp_dic=x['main']
except:
	humidity = "n/a"
	pressure = "n/a"
	temp = "n/a"
else:
	try:
		humidity = tmp_dic['humidity']
	except:
		humidity = "n/a"
	try:
		pressure = tmp_dic['pressure']
	except:
		pressure = "n/a"
	try:
		temp = tmp_dic['temp']
	except:
		temp = "n/a"


try:
	tmp_dic=x['wind']
except:
	speed = "n/a"
	deg = "n/a"
else:
	try:
		speed = tmp_dic['speed']
		speed = speed*3.6
	except:
		speed = "n/a"
	try:
		deg = tmp_dic['deg']
	except:
		deg = "n/a"

#vypis
print (CITY+'\n'+description+'\ntemp: '+ str(temp) + '°C\nhumidity: ' + str(humidity) + '%\npressure: ' + str(pressure) +' hPa\nwind-speed:'+ str(speed) +' km/h\nwind-deg: '+str(deg))
	