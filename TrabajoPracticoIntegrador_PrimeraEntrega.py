import csv
import matplotlib.pyplot as plt
import requests
from datetime import date
from datetime import timedelta
from PIL import Image

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
    if opcion == 1:
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

def suma_colores(im,CIUDAD):
    """ Determina la cantidad de pixeles del mismo color en un rango determinado
    pre: Recibe un image class y una tupla con dos valores (coord x, coord y)
    post: Devuelve un diccionario, con claves total, rojos, amarillos y verdes
    """
    BORDE_COLUMNAS = (4,54)
    BORDE_FILAS = (21,69)
    BLANQUINO = 600
    NEGRINO = 165
    RADIO = 90
    cuenta_colores = {"total":0,"rojos":0,"verdes":0,"azules":0,"amarillos":0}
    pix = im.load()
    
    for i in range(BORDE_COLUMNAS[0],im.size[0] - BORDE_COLUMNAS[1]):
        for j in range(BORDE_FILAS[0],im.size[1] - BORDE_FILAS[1]):
            if (i-CIUDAD[0])**2 + (j-CIUDAD[1])**2 <= RADIO**2 and pix[i,j][0]+pix[i,j][1]+pix[i,j][2] < BLANQUINO and pix[i,j][0]+pix[i,j][1]+pix[i,j][2] > NEGRINO:
                if pix[i,j][1] > pix[i,j][0] and pix[i,j][1] > pix[i,j][2]:
                    cuenta_colores["verdes"] += 1
                elif (pix[i,j][0] == pix[i,j][1] or 2*pix[i,j][1] > pix[i,j][0]) and pix[i,j][0] > pix[i,j][2]:
                    cuenta_colores["amarillos"] += 1
                elif pix[i,j][0] > pix[i,j][1] and pix[i,j][0] > pix[i,j][2]:
                    cuenta_colores["rojos"] +=1
                elif pix[i,j][2] > pix[i,j][0] and pix[i,j][2] >= pix[i,j][1]:
                    cuenta_colores["azules"] += 1
                cuenta_colores["total"] += 1 
            elif (i-CIUDAD[0])**2 + (j-CIUDAD[1])**2 <= RADIO**2:
                cuenta_colores["total"] += 1  
    return cuenta_colores

def declarar_alerta(colores_contados):
    """ Determino el tipo de alerta según el porcentaje de pixeles en un radio
    Tormenta fuerte con probabilidad de granizo: 0.6% pixeles rojos
    Tormenta moderada: 0.9% pixeles amarillos
    Tormenta débil: 7% pixeles verdes
    
    pre: Recibe un diccionario con claves total, rojos, amarillos y verdes
    post: Devuelve un string
    """
    if int(colores_contados["rojos"]*100/0.6) >= colores_contados["total"]:
        return "Tormenta fuerte con probabilidad de granizo"
    elif int(colores_contados["amarillos"]*100/0.9) >= colores_contados["total"]:
        return "Alerta: Tormenta moderada"
    elif int(colores_contados["verdes"]*100/7) >= colores_contados["total"]:
        return "Alerta: Tormenta débil"
    return "Sin alerta proxima"
    
def analisis_imagen():
    try:
        im = Image.open("imagen_a_analizar.png")
        im = im.convert("RGB")
        CIUDADES = {"Neuquén":(238,441),"Santa Rosa":(358,342),"Córdoba":(360,129),"Bahia Blanca":(423,428),"Pergamino":(484,232),"Parana":(488,144),"C.A.B.A.":(555,264),"Mar del Plata":(575,404),"Mercedes":(579,42),"La Plata":(571,279),"Paraná":(488,144)}
        for i in CIUDADES:
            colores_contados = suma_colores(im,CIUDADES[i])
            alerta = declarar_alerta(colores_contados)
            print(alerta, "en", i)
    except:
        print("No existe imagen imagen_a_analizar.png en la misma carpeta que el archivo .py")


def cargar_archivo(lista_clima):
    """
    PRE-CONDICION: recibe una lista vacia.
    POST-CONDICION: devuelve una lista con los datos del archivo csv.
    """
    opc = input("¿Desea agregar un archivo csv? Si la respuesta es no, se usara un archivo predeterminado. (SI/NO) \nRespuesta: ").upper()
    while opc != 'SI' and opc != 'NO':
        opc = input("Respuesta inválida. Reingrese su respuesta: ").upper()
    if opc == 'SI':
        nombre_archivo = input("Ingrese el nombre del archivo csv que desea ingresar: ")
        while nombre_archivo == '':
            nombre_archivo = input("No ingresó ningun nombre. Reingrese: ")
    else:
        nombre_archivo = "clima2016-2020.csv"
    with open(nombre_archivo) as archivo:
        linea = csv.reader(archivo)
        for filas in linea:
           lista_clima.append(filas)
    return lista_clima

def columna_fecha(lista_clima):
    """
    PRE-CONDICION: recibe los datos del archivo csv.
    POST-CONDICION: devuelve la ubicacion de la columna donde estan los años.
    """
    ubicacion_fecha = []
    ubicacion_fecha = lista_clima[0].index("Date")
    return ubicacion_fecha

def define_años(lista_clima, años, ubicacion_fecha):
    """
    PRE-CONDICIONES: recibe la lista con los datos del archivo csv y el indice de la fechas.
                    Se espera recibir las fechas en formato dd/mm/aa.
    POST-CONDICIONES: devuelve una lista con los ultimos cinco años.
    """
    lista_años = []
    for i in range(len(lista_clima)-1):
        lista_años.append(lista_clima[i+1][ubicacion_fecha].split('/'))
        
    for i in range(len(lista_clima)-1):
        chequeo = int(lista_años[i][2]) in años
        if  (chequeo == False):
            años.append(int(lista_años[i][2]))
    
    años.sort()
    while len(años) > 5:
        año_menor=años.index(min(años))
        años.pop(año_menor)
    return años

def diccionario_años(lista_clima, diccionario_clima, años , ubicacion_fecha):
    """
    PRE-CONDICION: recibe un diccionario vacio, los datos del archivo csv, el indice de la columna de la fecha y una lista con los años
                    Solo recibe hasta cinco años.
    POST-CONDICION: crea cinco listas con la informacion de cada año, las cuales seran los valores del diccionario.
                    Las claves del diccionario son los años correspondientes.
                    Devuelve un diccionario con la informacion.
    """
    primer_año = []
    segundo_año = []
    tercer_año = []
    cuarto_año = []
    quinto_año = []
    
    for i in range(len(lista_clima)):
        for j in range(len(años)):
            busqueda = str(años[j]) in lista_clima[i][ubicacion_fecha]
            if (j == 0) and (busqueda == True):
                primer_año.append(lista_clima[i])
            elif (j == 1) and (busqueda == True):
                segundo_año.append(lista_clima[i])
            elif (j == 2) and (busqueda == True):
                tercer_año.append(lista_clima[i])
            elif (j == 3) and (busqueda == True):
                cuarto_año.append(lista_clima[i])
            elif (j == 4) and (busqueda == True):
                quinto_año.append(lista_clima[i])
    
    
    diccionario_clima[años[0]] = primer_año
    if len(años)>=2:
        diccionario_clima[años[1]] = segundo_año
    if len(años)>=3:
        diccionario_clima[años[2]] = tercer_año
    if len(años)>=4:
        diccionario_clima[años[3]] = cuarto_año
    if len(años)==5:
        diccionario_clima[años[4]] = quinto_año
    
    return diccionario_clima

def columna_temperatura(lista_clima):
    """
    PRE-CONDICION:recibe una lista vacia y una lista con los datos del archivo.
    POST-CONDICION: busca en el archivo csv las columnas que contienen el titulo Temperature.
                    Devuelve una lista con el indice de las columnas encontradas.
    """
    columna_temp=[]
    for i in range(len(lista_clima[0])):
        cadena = "Temperature" in lista_clima[0][i]
        if cadena == True:
            columna_temp.append(i)
        
    return columna_temp

def promedio_temperatura(promedios,lista_clima, años, ubicacion_fecha, diccionario_clima):
    """
    PRE-CONDICION: recibe una lista vacia, el diccionario organizado por años, una lista con los años y una lista de los indices
                    de las columnas que contienen los datos de temperatura.
    POST-CONDICION: devuelve una lista con el promedio de temperaturas de los ultimos cinco años.
    """
    suma = 0
    promedio = 0
    cont=0
    columna_temp=[]
    columna_temp=columna_temperatura(lista_clima)
    
    
    while cont < len(años):
        for i in range(len(diccionario_clima[años[cont]])):
            for j in range(len(columna_temp)):
                suma+=float(diccionario_clima[años[cont]][i][columna_temp[j]])
            promedio=suma/len(diccionario_clima[años[cont]])
        promedios.append(promedio)
        suma = 0
        promedio = 0
        cont += 1
    return promedios

def grafico_temp(lista_clima,años, ubicacion_fecha, diccionario_clima):
    """
    PRE-CONDICION: recibe el diccionario con los datos, la lista de los años y la lista con la ubicacion de los datos de temperatura.
    POST-CONDICION: crea un grafico, que se muestra en pantalla, con los promedios de temperatura.
    """
    promedios=[]
    promedio_temperatura(promedios,lista_clima, años, ubicacion_fecha, diccionario_clima)
    colores=["orangered","maroon","darkorange","gold", "brown"]
    plt.title("Promedio de Temperaturas de los últimos cinco años.")
    plt.bar(años, height=promedios, color=colores)
    plt.show()
    
def columna_precipitacion(lista_clima):
    """
    PRE-CONDICION:recibe una lista vacia y una lista con los datos del archivo.
    POST-CONDICION: busca en el archivo csv las columnas que contienen el titulo Precipitation.
                    Devuelve una lista con el indice de las columnas encontradas.
    """
    columna_precip=[]
    for i in range(len(lista_clima[0])):
        cadena="Precipitation" in lista_clima[0][i]
        if cadena == True:
            columna_precip.append(i)
    return columna_precip   

def promedio_precipitacion(promedios_precip, lista_clima, años, ubicacion_fecha,diccionario_clima):
    """
    PRE-CONDICION: recibe una lista vacia, el diccionario organizado por años, una lista con los años y una lista de los indices
                    de las columnas que contienen los datos de precipitacion.
    POST-CONDICION: devuelve una lista con el promedio de precipitaciones de los ultimos cinco años.
    """
    suma = 0
    promedio = 0
    cont = 0
    columna_precip=[]
    columna_precip=columna_precipitacion(lista_clima)
    while cont < len(años):
        for i in range(len(diccionario_clima[años[cont]])):
            for j in range(len(columna_precip)):
                suma += float(diccionario_clima[años[cont]][i][columna_precip[j]])
            promedio = suma/len(diccionario_clima[años[cont]])
        promedios_precip.append(promedio)
        suma = 0
        promedio = 0
        cont += 1
    return promedios_precip
    
def grafico_precip(lista_clima, años, ubicacion_fecha,diccionario_clima):
    """
    PRE-CONDICION: recibe el diccionario con los datos, la lista de los años y la lista con la ubicacion de los datos de precipitación.
    POST-CONDICION: crea un grafico, que se muestra en pantalla, con los promedios de precipitación.
    """
    promedios_precip=[]
    promedio_precipitacion(promedios_precip, lista_clima, años, ubicacion_fecha,diccionario_clima)
    colores=["midnightblue","royalblue","lightsteelblue","cornflowerblue", "slategrey"]
    plt.title("Promedio de Precipitaciones de los últimos cinco años.")
    plt.bar(años, height=promedios_precip, color=colores)
    plt.show()
    
def maxima_precipitacion(lista_clima, años, ubicacion_fecha,diccionario_clima):  
    """
    PRE-CONDICION: recibe la lista con los datos del archivo csv y otra lista con la posicion de la columna con datos de precipitacion.
    POST-CONDICION: devuelve el maxima cantidad de precipitacion.
    """
    precipitacion=[]
    cont=0
    columna_precip=columna_precipitacion(lista_clima)
    
    while cont < len(años):
        for i in range(len(diccionario_clima[años[cont]])):
            for j in range(len(columna_precip)):
                precipitacion.append(float(diccionario_clima[años[cont]][i][columna_precip[j]]))
        cont += 1
    maximo=max(precipitacion)
    return maximo

def maxima_temperatura(lista_clima, años, ubicacion_fecha,diccionario_clima):
    """
    PRE-CONDICION: recibe la lista con los datos del archivo csv y otra lista con la posicion de la columna con datos de temperatura.
    POST-CONDICION: devuelve el maxima temperatura alcanzada.
    """
    temperatura=[]
    cont=0
    columna_temp=columna_temperatura(lista_clima)
    while cont < len(años):
        for i in range(len(diccionario_clima[años[cont]])):
            for j in range(len(columna_temp)):
                temperatura.append(float(diccionario_clima[años[cont]][i][columna_temp[j]]))
        cont += 1
    maximo=max(temperatura)
    return maximo


def menu():
    opc=0
    while opc != 6:
        opc = int(input("Bienvenidos a Tormenta. \nMenú principal: \n1.Listado de alertas por geolocalizacion. \n2.Listado de alertas nacionales. \n3.Información de archivo csv. \n4.Pronostico extendido. \n5.Radar. \n6.Salir. \nOpción: "))
        while opc <= 0 or opc > 6:
            opc=int(input("Ingreso una opcion inválida. Reingrese: \n1.Listado de alertas por geolocalizacion. \n2.Listado de alertas nacionales. \n3.Información de archivo csv. \n4.Pronostico extendido. \n5.Radar. \n6.Salir. \nOpción: "))
        if opc == 1:
            alertas_actuales_por_usuario()
        elif opc == 2:
            alertas_actuales()
        elif opc == 3:
            lista_clima = []
            años=[]
            diccionario_clima={}
            cargar_archivo(lista_clima)
            ubicacion_fecha = columna_fecha(lista_clima)
            define_años(lista_clima, años, ubicacion_fecha)
            diccionario_años(lista_clima, diccionario_clima, años , ubicacion_fecha)
            opcion=0
            print("----Carga de archivo exitosa----")
            
            while opcion != 4:
                opcion=int(input("Menú de información: \n1.Promedio de temperatura. \n2.Promedio de precipitacion. \n3.Milímetros y temperatura máxima. \n4.Volver al menú principal. \nOpción: "))
                while opcion <= 0 or opcion > 4:
                    opcion=int(input("Ingreso una opcion inválida. Reingrese: \n1.Promedio de temperatura. \n2.Promedio de precipitacion. \n3.Milímetros y temperatura máxima. \n4.Volver al menú principal. \nOpción: "))
            
                if opcion == 1:
                    grafico_temp(lista_clima,años,ubicacion_fecha,diccionario_clima)
                elif opcion == 2:
                    grafico_precip(lista_clima,años, ubicacion_fecha,diccionario_clima)
                elif opcion == 3:
                    print(f"La cantidad de milímetros maximos registrada en los últimos cinco años fue de {maxima_precipitacion(lista_clima,años,ubicacion_fecha, diccionario_clima): .1f} ml")
                    print(f"La máxima temperatura registrada en los últimos cinco años fue de {maxima_temperatura(lista_clima,años,ubicacion_fecha, diccionario_clima): .1f}ºC")

        elif opc == 4:
            pronostico_extendido()
            alertas_actuales_por_usuario()
        elif opc == 5:
            analisis_imagen()
           
def main():
   menu()
             
main()






