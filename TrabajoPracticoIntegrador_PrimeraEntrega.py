import requests
from datetime import date
from datetime import timedelta

def mostrar_pronostico (datos, provincias, opcion_provincia, ciudades, opcion_ciudad):
    """Muestra en pantalla el pronostico de la ciudad ingresada
    PRE: datos de la pagina SNM, lista con las provincias y ciudades, opciones legidas por el usuario
    """
    for tiempo in range(len(datos)):
        if datos[tiempo]['name'] == ciudades[opcion_ciudad] and datos[tiempo]['province'] == provincias[opcion_provincia]:
            print(f"Temperatura a la mañana: {datos[tiempo]['weather']['morning_temp']}°C")
            print(f"Tiempo a la mañana: {datos[tiempo]['weather']['morning_desc']}")
            print(f"Temperatura a la tarde: {datos[tiempo]['weather']['afternoon_temp']}°C")
            print(f"Tiempo a la tarde: {datos[tiempo]['weather']['afternoon_desc']}")
            
def fecha_amigable(fecha):
    """ Cambia el formato de la fecha, para que sea más amigable con el usuario
    pre: recibe una fecha en formato dd- mm- aaaa
    Muestra en pantalla un string con el formate de fecha dia de mes del año
    """
    meses = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    dia = fecha.day
    mes = meses[fecha.month - 1]
    año = fecha.year
    print(f"{dia} de {mes} del {año}")

def pronostico_extendido():
    """ Determina el pronostico de los proximos tres días
    """
    pronosticos_extendidos_1 =  requests.get('https://ws.smn.gob.ar/map_items/forecast/1')
    pronosticos_extendidos_2 =  requests.get('https://ws.smn.gob.ar/map_items/forecast/2')
    pronosticos_extendidos_3 =  requests.get('https://ws.smn.gob.ar/map_items/forecast/3')
    datos_1 = pronosticos_extendidos_1.json()
    datos_2 = pronosticos_extendidos_2.json()
    datos_3 = pronosticos_extendidos_3.json()
    provincias = []
    ciudades = []
    #print(datos_1)
    for tiempo in range(len(datos_1)):
        if datos_1[tiempo]['province'] not in provincias:
            provincias.append(datos_1[tiempo]['province'])
    provincias.sort(key=str.lower)
    for provincia in range(len(provincias)):
        print (f"{provincia} - {provincias[provincia]}")
    print()
    opcion_provincia = int(input(f"Por favor elegir una provincia del 0 al {len(provincias)}: "))
    print()
    for tiempo in range(len(datos_1)):
        #print(datos_1[tiempo]['name'])
        #print(datos_1[tiempo]['province'])
        #print(provincias[opcion_provincia])
        if datos_1[tiempo]['name'] not in ciudades and datos_1[tiempo]['province'] == provincias[opcion_provincia]:
            ciudades.append(datos_1[tiempo]['name'])
    ciudades.sort(key=str.lower)
    for ciudad in range(len(ciudades)):
        print (f"{ciudad} - {ciudades[ciudad]}")
    print()
    opcion_ciudad = int(input(f"Por favor elegir una ciudad de {provincias[opcion_provincia]} del 0 al {len(ciudades)}: "))
    print()
    print()
    hoy = date.today()
    mañana = hoy + timedelta(days=1)
    despues_de_mañana= hoy + timedelta(days=2)
    fecha_amigable(hoy)
    mostrar_pronostico (datos_1, provincias, opcion_provincia, ciudades, opcion_ciudad)
    print()
    fecha_amigable(mañana)
    mostrar_pronostico (datos_2, provincias, opcion_provincia, ciudades, opcion_ciudad)
    print()
    fecha_amigable(despues_de_mañana)
    mostrar_pronostico (datos_3, provincias, opcion_provincia, ciudades, opcion_ciudad)
    alertas_actuales_por_usuario(2, provincias[opcion_provincia])
    
def alertas_actuales():
    """Determina las alertas a nivel nacional
    """
    alerta_actual= requests.get('https://ws.smn.gob.ar/alerts/type/AL')
    datos = alerta_actual.json()
    for alerta in range(len(datos)):
        print()
        print(f"{datos[alerta]['title']}: {datos[alerta]['description']}")
        print()
        print("ZONAS:")
        for zona in datos[alerta]['zones']:
            print(datos[alerta]['zones'][zona])
        print("---------------------------------------------------------")
    
def alertas_actuales_por_usuario(opcion, zona_ingresada=cfk):
    """ Determina las alertas cercanas o en la provincia ingresada por el usuario
    PRE: recibe la opcion si necesita que ingrese la zona o no
    """
    alerta_actual= requests.get('https://ws.smn.gob.ar/alerts/type/AL')
    datos = alerta_actual.json()
    cont= 0
    if opcion == 1
        zona_ingresada = (input("Ingresar provincia: ")).capitalize()
    for alerta in range(len(datos)):
        for zona in datos[alerta]['zones']:
            if (datos[alerta]['zones'][zona].find(zona_ingresada)) >= 0:
                cont += 1
                print (f"{datos[alerta]['title']}: {datos[alerta]['description']}")
                print()
                print("Zonas")
                for zona in datos[alerta]['zones']:
                    print(datos[alerta]['zones'][zona])
                print("---------------------------------------------------------")
    if cont == 0:
        print()
        print("No existen alertas para esa zona")