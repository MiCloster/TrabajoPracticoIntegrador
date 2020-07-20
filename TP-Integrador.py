"""
PRE-CONDICION: recibe una lista vacia.
POST-CONDICION: devuelve una lista con los datos del archivo csv.
"""
def cargar_archivo(lista_clima):
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


"""
PRE-CONDICION: recibe los datos del archivo csv.
POST-CONDICION: devuelve la ubicacion de la columna donde estan los años.
"""
def columna_fecha(lista_clima):
    ubicacion_fecha = []
    ubicacion_fecha = lista_clima[0].index("Date")
    return ubicacion_fecha


"""
PRE-CONDICIONES: recibe la lista con los datos del archivo csv y el indice de la fechas. 
POST-CONDICIONES: devuelve una lista con los ultimos cinco años.
"""
def define_años(lista_clima, años, ubicacion_fecha):
    lista_años = []
    for i in range(len(lista_clima)-1):
        lista_años.append(lista_clima[i+1][ubicacion_fecha].split('/'))
        
    for i in range(len(lista_clima)-1):
        chequeo = lista_años[i][2] in años
        if  (chequeo == False) and (len(años) < 5):
            años.append(lista_años[i][2])       
    return años

"""
PRE-CONDICION: recibe un diccionario vacio, los datos del archivo csv, el indice de la columna de la fecha y una lista con los años.
POST-CONDICION: crea cinco listas con la informacion de cada año, las cuales seran los valores del diccionario.
                Las claves del diccionario son los años correspondientes.
                Devuelve un diccionario con la informacion.
"""
def diccionario_años(lista_clima, diccionario_clima, años , ubicacion_fecha):
    primer_año = []
    segundo_año = []
    tercer_año = []
    cuarto_año = []
    quinto_año = []
    
    
    for i in range(len(lista_clima)):
        for j in range(len(años)):
            busqueda = años[j] in lista_clima[i][ubicacion_fecha]
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
    diccionario_clima[años[1]] = segundo_año
    diccionario_clima[años[2]] = tercer_año
    diccionario_clima[años[3]] = cuarto_año
    diccionario_clima[años[4]] = quinto_año
    
    return diccionario_clima

"""
PRE-CONDICION:recibe una lista vacia y una lista con los datos del archivo.
POST-CONDICION: busca en el archivo csv las columnas que contienen el titulo Temperature.
                Devuelve una lista con el indice de las columnas encontradas.
"""
def columna_temperatura(lista_clima):
    columna_temp=[]
    for i in range(len(lista_clima[0])):
        cadena = "Temperature" in lista_clima[0][i]
        if cadena == True:
            columna_temp.append(i)
        
    return columna_temp

"""
PRE-CONDICION: recibe una lista vacia, el diccionario organizado por años, una lista con los años y una lista de los indices
                de las columnas que contienen los datos de temperatura.
POST-CONDICION: devuelve una lista con el promedio de temperaturas de los ultimos cinco años.
"""
def promedio_temperatura(promedios,lista_clima, años, ubicacion_fecha):
    suma = 0
    promedio = 0
    cont=0
    columna_temp=[]
    diccionario_clima={}
    columna_temp=columna_temperatura(lista_clima)
    diccionario_años(lista_clima, diccionario_clima,años, ubicacion_fecha)
    
    while cont < 5:
        lista=diccionario_clima[años[cont]]
        for i in range(len(lista)):
            for j in range(len(columna_temp)):
                suma+=float(lista[i][columna_temp[j]])
            promedio=suma/len(lista)
        promedios.append(promedio)
        suma = 0
        promedio = 0
        cont += 1
    return promedios
"""
PRE-CONDICION: recibe el diccionario con los datos, la lista de los años y la lista con la ubicacion de los datos de temperatura.
POST-CONDICION: crea un grafico, que se muestra en pantalla, con los promedios de temperatura.
"""
def grafico_temp(lista_clima):
    promedios=[]
    años=[]
    ubicacion_fecha = columna_fecha(lista_clima)
    define_años(lista_clima, años , ubicacion_fecha)
    promedio_temperatura(promedios,lista_clima, años, ubicacion_fecha)
    colores=["orangered","maroon","darkorange","gold", "brown"]
    plt.title("Promedio de Temperaturas de los últimos cinco años.")
    plt.bar(años, height=promedios, color=colores)
    plt.show()
    
    
"""
PRE-CONDICION:recibe una lista vacia y una lista con los datos del archivo.
POST-CONDICION: busca en el archivo csv las columnas que contienen el titulo Precipitation.
                Devuelve una lista con el indice de las columnas encontradas.
"""
def columna_precipitacion(lista_clima):
    columna_precip=[]
    for i in range(len(lista_clima[0])):
        cadena="Precipitation" in lista_clima[0][i]
        if cadena == True:
            columna_precip.append(i)
    return columna_precip   

"""
PRE-CONDICION: recibe una lista vacia, el diccionario organizado por años, una lista con los años y una lista de los indices
                de las columnas que contienen los datos de precipitacion.
POST-CONDICION: devuelve una lista con el promedio de precipitaciones de los ultimos cinco años.
"""
def promedio_precipitacion(promedios_precip, lista_clima, años, ubicacion_fecha):
    suma = 0
    promedio = 0
    cont = 0
    columna_precip=[]
    diccionario_clima={}
    diccionario_años(lista_clima, diccionario_clima,años, ubicacion_fecha)
    columna_precip=columna_precipitacion(lista_clima)
    while cont < 5:
        lista = diccionario_clima[años[cont]]
        for i in range(len(lista)):
            for j in range(len(columna_precip)):
                suma += float(lista[i][columna_precip[j]])
            promedio = suma/len(lista)
        promedios_precip.append(promedio)
        suma = 0
        promedio = 0
        cont += 1
    return promedios_precip
    
    

"""
PRE-CONDICION: recibe el diccionario con los datos, la lista de los años y la lista con la ubicacion de los datos de precipitación.
POST-CONDICION: crea un grafico, que se muestra en pantalla, con los promedios de precipitación.
"""
def grafico_precip(lista_clima):
    promedios_precip=[]
    años=[]
    ubicacion_fecha = columna_fecha(lista_clima)
    define_años(lista_clima, años, ubicacion_fecha)
    promedio_precipitacion(promedios_precip, lista_clima, años, ubicacion_fecha)
    colores=["midnightblue","royalblue","lightsteelblue","cornflowerblue", "slategrey"]
    plt.title("Promedio de Precipitaciones de los últimos cinco años.")
    plt.bar(años, height=promedios_precip, color=colores)
    plt.show()
    

"""
PRE-CONDICION: recibe la lista con los datos del archivo csv y otra lista con la posicion de la columna con datos de precipitacion.
POST-CONDICION: devuelve el maxima cantidad de precipitacion.
"""
def maxima_precipitacion(lista_clima):
    precipitacion=[]
    columna_precip=columna_precipitacion(lista_clima)
    for i in range(len(lista_clima)):
        for j in range(len(columna_precip)):
            if i+1 < len(lista_clima):
                precipitacion.append(float(lista_clima[i+1][columna_precip[j]]))
            
    maximo=max(precipitacion)
    return maximo
"""
PRE-CONDICION: recibe la lista con los datos del archivo csv y otra lista con la posicion de la columna con datos de temperatura.
POST-CONDICION: devuelve el maxima temperatura alcanzada.
"""
def maxima_temperatura(lista_clima):
    temperatura=[]
    columna_temp=columna_temperatura(lista_clima)
    for i in range(len(lista_clima)):
        for j in range(len(columna_temp)):
            if i+1 < len(lista_clima):
                temperatura.append(float(lista_clima[i+1][columna_temp[j]]))
            
    maximo=max(temperatura)
    return maximo


def menu():
    lista_clima = []
    opc=0
    while opc != 6:
        opc = int(input("Bienvenidos a Tormenta. \nMenú principal: \n1.Listado de alertas por geolocalizacion. \n2.Listado de alertas nacionales. \n3.Información de archivo csv. \n4.Pronostico extendido. \n5.Radar. \n6.Salir. \nOpción: "))
        while opc <= 0 or opc > 6:
            opc=int(input("Ingreso una opcion inválida. Reingrese: \n1.Listado de alertas por geolocalizacion. \n2.Listado de alertas nacionales. \n3.Información de archivo csv. \n4.Pronostico extendido. \n5.Radar. \nOpción: "))
        if opc == 1:
            alertas_actuales_por_usuario()
        elif opc == 2:
            alertas_actuales()
        elif opc == 3:
            opcion=0
            cargar_archivo(lista_clima)
            print("----Carga de archivo exitosa----")
            while opcion != 4:
                opcion=int(input("Menú de información: \n1.Promedio de temperatura. \n2.Promedio de precipitacion. \n3.Milímetros y temperatura máxima. \n4.Volver al menú principal. \nOpción: "))
                while opcion <= 0 or opcion > 4:
                    opcion=int(input("Ingreso una opcion inválida. Reingrese: \n1.Promedio de temperatura. \n2.Promedio de precipitacion. \n3.Milímetros y temperatura máxima. \n4.Volver al menú principal. \nOpción: "))
            
                if opcion == 1:
                    grafico_temp(lista_clima)
                elif opcion == 2:
                    grafico_precip(lista_clima)
                elif opcion == 3:
                    print(f"La cantidad de milímetros maximos registrada en los últimos cinco años fue de {maxima_precipitacion(lista_clima)}")
                    print(f"La máxima temperatura registrada en los últimos cinco años fue de {maxima_temperatura(lista_clima)}")

        elif opc == 4:
            pronostico_extendido()
        elif opc == 5:
            analisis_imagen()
           

import csv
import matplotlib.pyplot as plt

def main():
   menu()
       
        
main()




