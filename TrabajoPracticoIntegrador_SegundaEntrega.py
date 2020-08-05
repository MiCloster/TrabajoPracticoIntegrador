import csv
import matplotlib.pyplot as plt
import requests
from datetime import date
from datetime import timedelta
from PIL import Image
from geopy.geocoders import Nominatim

def encontrar_ubicacion(lat,long):
    """Determina la dirección correspondiente a la latitud y longitud ingresadas por el usuario
    pre: Recibe dos int
    post: Devuelve un string
    """
    coords = f"{lat}, {long}"
    #La libreria geopy requiere que se ingrese el limite de ubicaciónes que se van a localizar, o una dirección de mail
    try:
        geolocator = Nominatim(user_agent="mdelcastillo@fi.uba.ar")
        direccion = geolocator.reverse(coords)
        dir_prov = direccion.raw
        try:
            provincia = dir_prov['address']['state']
        except:
            provincia = dir_prov['address']['city']
        pais = dir_prov['address']['country']
    except:
        provincia = "-"
        pais = "-"
    return [provincia,pais]

def verificar_ingreso_numerico(a_verificar,primer_valor,ultimo_valor):
    """Verifica que el valor ingresado por el usuario sea un entero entre los valores requeridos
    pre: Recive una variable con cualquier valor, y dos enteros
    post: Devuelve un int
    """
    while type(a_verificar) != int or (type(a_verificar) == int and (a_verificar < primer_valor or a_verificar > ultimo_valor)):
        if type(a_verificar) != int:
            try:
                a_verificar = int(a_verificar)
            except:
                a_verificar = input(f"Ingreso una opcion inválida, ingrese un entero entre {primer_valor}  y {ultimo_valor}: ")
        elif a_verificar < primer_valor or a_verificar > ultimo_valor:
            a_verificar = input(f"Ingreso una opcion inválida, ingrese un entero entre {primer_valor}  y {ultimo_valor}: ")
    return a_verificar

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

def alertas_actuales_por_usuario(opcion, zona_ingresada='cfk'):
    """ Determina las alertas cercanas o en la provincia ingresada por el usuario
    PRE: recibe la opcion si necesita que ingrese la zona o no
    """
    alerta_actual= requests.get('https://ws.smn.gob.ar/alerts/type/AL')
    datos = alerta_actual.json()
    cont= 0
    localizacion = ["","Argentina"]
    if opcion == 1:
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
    for alerta in range(len(datos)):
        for zona in datos[alerta]['zones']:
            if (datos[alerta]['zones'][zona].find(zona_ingresada)) >= 0:
                cont += 1
                print (f"{datos[alerta]['title']}: {datos[alerta]['description']}\n")
                print("Zonas")
                for zona in datos[alerta]['zones']:
                    print(datos[alerta]['zones'][zona])
                print("---------------------------------------------------------")
    if cont == 0 and localizacion[1] == "Argentina":
        print("\nNo existen alertas para esa zona")

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
    opcion_provincia = input(f"Por favor elegir una provincia del 0 al {len(provincias) - 1}: ")
    opcion_provincia = verificar_ingreso_numerico(opcion_provincia,0,len(provincias) - 1)
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
    opcion_ciudad = input(f"Por favor elegir una ciudad de {provincias[opcion_provincia]} del 0 al {len(ciudades) - 1}: ")
    opcion_ciudad = verificar_ingreso_numerico(opcion_ciudad,0,len(ciudades) - 1)
    print("\n")
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
    imagen_electa = input("\nEscriba ubicación/nombre (sin formato) de la imagen .png a analizar (0 si desea usar una imagen predeterminada): ")
    imagen_electa = imagen_electa + ".png"
    try:
        im = Image.open(imagen_electa)
        im = im.convert("RGB")
        CIUDADES = {"Neuquén":(238,441),"Santa Rosa":(358,342),"Córdoba":(360,129),"Bahia Blanca":(423,428),"Pergamino":(484,232),"Parana":(488,144),"C.A.B.A.":(555,264),"Mar del Plata":(575,404),"Mercedes":(579,42),"La Plata":(571,279),"Paraná":(488,144)}
        for i in CIUDADES:
            colores_contados = suma_colores(im,CIUDADES[i])
            alerta = declarar_alerta(colores_contados)
            print(alerta, "en", i)
    except:
        if imagen_electa == "0.png":
            print("La imagen predeterminada", imagen_electa, "fue eliminada o no se descargo correcramente")
        else:
            print("No existe imagen", imagen_electa, "con el formato correspondiente en la misma carpeta que el archivo .py")


def cargar_archivo():
    """
    Devuelve una lista con los datos del archivo csv.
    """
    lista_clima = []
    opc = input("¿Desea agregar un archivo csv? Si la respuesta es no, se usara un archivo predeterminado. (SI/NO) \nRespuesta: ").upper()
    while opc != 'SI' and opc != 'NO':
        opc = input("Respuesta inválida. Reingrese su respuesta: ").upper()
    if opc == 'SI':
        nombre_archivo = input("Ingrese el nombre del archivo csv que desea ingresar: ")
        nombre_archivo = nombre_archivo + ".csv"
        while nombre_archivo == '':
            nombre_archivo = input("No ingresó ningun nombre. Reingrese: ")
    else:
        nombre_archivo = "clima2016-2020.csv"
    try:
        with open(nombre_archivo) as archivo:
            linea = csv.reader(archivo)
            for filas in linea:
               lista_clima.append(filas)
    except:
        print("Archivo",nombre_archivo ,"no existe")
    return lista_clima

def define_años(lista_clima):
    """
    PRE-CONDICIONES: recibe la lista con los datos del archivo csv.
                    Se espera recibir las fechas en formato dd/mm/aa.
    POST-CONDICIONES: devuelve una lista con los ultimos cinco años.
    """
    años = []
    lista_años = []
    ubicacion_fecha = lista_clima[0].index("Date")
    
    for i in range(len(lista_clima)-1):
        lista_años.append(lista_clima[i+1][ubicacion_fecha].split('/'))
        
    for i in range(len(lista_clima)-1):
        if int(lista_años[i][2]) not in años:
            años.append(int(lista_años[i][2]))
    años.sort()
    
    while len(años) > 5:
        año_menor=años.index(min(años))
        años.pop(año_menor)
    return años

def diccionario_años(lista_clima, años):
    """
    PRE-CONDICION: recibe los datos del archivo csv y una lista con los años.
    POST-CONDICION: Las claves del diccionario son los años correspondientes y sus valores es una lista que contiene datos según el año.
                    Devuelve un diccionario con la informacion.
    """
    diccionario_clima={}
    ubicacion_fecha = lista_clima[0].index("Date")
    
    for j in range(len(años)):
        diccionario_clima[años[j]]=[]

    for i in range(len(lista_clima)):
        for j in range(len(años)):
            if str(años[j]) in lista_clima[i][0]:
                diccionario_clima[años[j]].append(lista_clima[i])
    return diccionario_clima

def ubicacion_columna(lista_clima, nombre_columna):
    """
    PRE-CONDICION: recibe una lista con los datos del archivo y el titulo de la columna que se desea buscar.
    POST-CONDICION: busca en el archivo csv las columnas que contienen el titulo pedido.
                    Devuelve una lista con el indice de las columnas encontradas.
    """
    columna = []
    for i in range(len(lista_clima[0])):
        if nombre_columna in lista_clima[0][i]:
            columna.append(i)
    return columna

def calculo_del_promedio(años, diccionario_clima, indice_columna):
    """
    PRE-CONDICION: recibe el diccionario organizado por años, una lista con los años y una lista de los indices
                    de las columnas que contienen los datos pedidos
    POST-CONDICION: devuelve una lista con el promedio de los ultimos cinco años.
    """
    suma = 0
    promedio = 0
    lista_promedios = []
    for m in range(len(años)):
        for i in range(len(diccionario_clima[años[m]])):
            for j in range(len(indice_columna)):
                suma+=float(diccionario_clima[años[m]][i][indice_columna[j]])
            promedio = suma/(len(diccionario_clima[años[m]])*len(indice_columna))
        lista_promedios.append(promedio)
        suma = 0
        promedio = 0
    return lista_promedios
    
def grafico(años,diccionario_clima, indice_columna, colores, titulo):
    """
    PRE-CONDICION: recibe el diccionario con los datos, la lista de los años y la lista con la ubicacion de los datos.
    POST-CONDICION: crea un grafico, que se muestra en pantalla, con los promedios de cada año.
    """
    promedios = calculo_del_promedio( años, diccionario_clima, indice_columna)
    plt.title("Promedio de " + titulo + " de los últimos cinco años.")
    plt.bar(años, height=promedios, color=colores)
    plt.show()
    
def datos_maximos(años,diccionario_clima,indice_columna):  
    """
    PRE-CONDICION: recibe la lista con la posicion de la columna, lista de los años y el diccionario.
    POST-CONDICION: devuelve el numero máximo de la lista de datos pedidos.
    """
    lista_valores=[]
    for m in range(len(años)):
        for i in range(len(diccionario_clima[años[m]])):
            for j in range(len(indice_columna)):
                lista_valores.append(float(diccionario_clima[años[m]][i][indice_columna[j]]))
    maximo = max(lista_valores)
    return maximo

def informacion_archivo():
    lista_clima = cargar_archivo()
    años = define_años(lista_clima)
    diccionario_clima = diccionario_años(lista_clima, años)
    columna_precip = ubicacion_columna(lista_clima, "Precipitation")
    columna_temp = ubicacion_columna(lista_clima, "Temperature")
    colores_1 = ["midnightblue","royalblue","lightsteelblue","cornflowerblue", "slategrey"]
    colores_2= ["orangered","maroon","darkorange","gold", "brown"]
    opcion = 0
    print("----Carga de archivo exitosa----")
    
    while opcion != 4:
        opcion = input("\nMenú de información: \n1.Promedio de temperatura. \n2.Promedio de precipitacion. \n3.Milímetros y temperatura máxima. \n4.Volver al menú principal. \nOpción: ")
        opcion = verificar_ingreso_numerico(opcion,1,4)
        if opcion == 1:
            grafico(años,diccionario_clima,columna_temp, colores_2, "Temperaturas")
        elif opcion == 2:
            grafico(años,diccionario_clima, columna_precip, colores_1, "Precipitaciones")
        elif opcion == 3:
            print(f"La cantidad de milímetros maximos registrada en los últimos cinco años fue de {datos_maximos(años, diccionario_clima,columna_precip): .1f} ml")
            print(f"La máxima temperatura registrada en los últimos cinco años fue de {datos_maximos(años,diccionario_clima,columna_temp): .1f}ºC")

def main():
    print("Bienvenidos a Tormenta.")
    opc=0
    while opc != 6:
        print("\nMenú principal: \n1.Listado de alertas por geolocalizacion. \n2.Listado de alertas nacionales. \n3.Información de archivo csv. \n4.Pronostico extendido. \n5.Radar. \n6.Salir.")
        opc = input("Opción: ")
        opc = verificar_ingreso_numerico(opc,1,6)
        if opc == 1:
            try:
                alertas_actuales_por_usuario(1)
            except:
                print("Error de internet, verifique su conexión y vuelva a intentarlo")
        elif opc == 2:
            try:
                alertas_actuales()
            except:
                print("Error de internet, verifique su conexión y vuelva a intentarlo")
        elif opc == 3:
            informacion_archivo()
        elif opc == 4:
            try:
                pronostico_extendido()
            except:
                print("Error de internet, verifique su conexión y vuelva a intentarlo")
        elif opc == 5:
            analisis_imagen()
main()



