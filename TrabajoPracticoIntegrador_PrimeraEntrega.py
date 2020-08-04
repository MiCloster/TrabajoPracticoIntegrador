import requests
from datetime import date
from datetime import timedelta

def mostrar_pronostico (datos, provincia, ciudad):
    """Muestra en pantalla el pronostico de la ciudad ingresada
    PRE: datos de la pagina SNM, lista con las provincias y ciudades, opciones legidas por el usuario
    """
    for tiempo in range(len(datos)):
        if datos[tiempo]['name'] == ciudad and datos[tiempo]['province'] == provincia:
            print(f"\nTemperatura a la mañana: {datos[tiempo]['weather']['morning_temp']}°C")
            print(f"Tiempo a la mañana: {datos[tiempo]['weather']['morning_desc']}")
            print(f"Temperatura a la tarde: {datos[tiempo]['weather']['afternoon_temp']}°C")
            print(f"Tiempo a la tarde: {datos[tiempo]['weather']['afternoon_desc']}\n")
            
def fecha_amigable(fecha):
    """ Cambia el formato de la fecha, para que sea más amigable con el usuario
    pre: recibe una fecha en formato dd- mm- aaaa
    Muestra en pantalla un string con el formate de fecha dia de mes del año
    """
    meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    dia = fecha.day
    mes = meses[fecha.month - 1]
    año = fecha.year
    print(f"\n\n{dia} de {mes} del {año}")

def pronostico_extendido():
    """ Determina el pronostico de los proximos tres días
    """
    snm_informacion= ['https://ws.smn.gob.ar/map_items/forecast/1','https://ws.smn.gob.ar/map_items/forecast/2','https://ws.smn.gob.ar/map_items/forecast/3']
    datos= []
    pronostico_extendido = []
    dias= []
    for i in range(len(snm_informacion)):
        pronostico_extendido.append(requests.get(snm_informacion[i]))
        datos.append(pronostico_extendido[i].json())
        dias.append( date.today() + timedelta(days= i))
    provincias = []
    ciudades = []
    for tiempo in range(len(datos[0])):
        if datos[0][tiempo]['province'] not in provincias:
            provincias.append(datos[0][tiempo]['province'])
    provincias.sort(key=str.lower)
    for provincia in range(len(provincias)):
        print (f"{provincia} - {provincias[provincia]}")
    opcion_provincia = int(input(f"\nPor favor elegir una provincia del 0 al {len(provincias)}: "))
    opcion_provincia = verificar_ingreso_numerico(opcion_provincia,0,len(provincias) - 1)
    for tiempo in range(len(datos[0])):
        if datos[0][tiempo]['name'] not in ciudades and datos[0][tiempo]['province'] == provincias[opcion_provincia]:
            ciudades.append(datos[0][tiempo]['name'])
    ciudades.sort(key=str.lower)
    for ciudad in range(len(ciudades)):
        print (f"{ciudad} - {ciudades[ciudad]}")
    opcion_ciudad = int(input(f"\nPor favor elegir una ciudad de {provincias[opcion_provincia]} del 0 al {len(ciudades)}: \n"))
    opcion_ciudad = verificar_ingreso_numerico(opcion_ciudad,0,len(ciudades) - 1)
    for posicion in range(len(snm_informacion)):
        fecha_amigable(dias[posicion])
        mostrar_pronostico(datos[posicion],provincias[opcion_provincia],ciudades[opcion_ciudad])
    alertas_actuales_por_usuario(2, provincias[opcion_provincia])
    
def alertas_actuales():
    """Determina las alertas a nivel nacional
    """
    alerta_actual= requests.get('https://ws.smn.gob.ar/alerts/type/AL')
    datos = alerta_actual.json()
    for alerta in range(len(datos)):
        print(f"\n{datos[alerta]['title']}: {datos[alerta]['description']}")
        print("\nZONAS:")
        for zona in datos[alerta]['zones']:
            print(datos[alerta]['zones'][zona])
        print("---------------------------------------------------------")
        
def ingreso_ubicacion_por_usuario():
    lat = input("Ingrese latitud: ")
    long = input("Ingrese longitud: ")
    localizacion = encontrar_ubicacion(lat,long)
    if localizacion[1] == "Argentina":
        zona_ingresada = localizacion[0]
        print("Provincia correspondiente: ",zona_ingresada)
    elif localizacion[1] != "-":
        print("Las coordenadas introducidas no corresponden a Argentina, corresponden a ", localizacion[1])
    else:
        print("Error, no hay conexión a internet, las coordenadas introducidas corresponden a un Océano o Mar, o no se ingresaron coordenadas validas")
    return zona_ingresada
    
def alertas_actuales_por_usuario(opcion, zona_ingresada="cfk"):
    """ Determina las alertas cercanas o en la provincia ingresada por el usuario
    PRE: recibe la opcion si necesita que ingrese la zona o no
    """
    alerta_actual= requests.get('https://ws.smn.gob.ar/alerts/type/AL')
    datos = alerta_actual.json()
    cont= 0
    if opcion == 1:
        zona_ingresada = ingreso_ubicacion_por_usuario() 
    for alerta in range(len(datos)):
        for zona in datos[alerta]['zones']:
            if (datos[alerta]['zones'][zona].find(zona_ingresada)) >= 0:
                cont += 1
                print (f"\n{datos[alerta]['title']}: {datos[alerta]['description']}")
                print("\nZonas")
                for zona in datos[alerta]['zones']:
                    print(datos[alerta]['zones'][zona])
                print("---------------------------------------------------------")
    if cont == 0:
        print("\n\nNo existen alertas para esa zona")
