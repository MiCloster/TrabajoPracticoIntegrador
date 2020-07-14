"""
PRE-CONDICION: recibe una lista vacia.
POST-CONDICION: devuelve una lista con los datos del archivo csv.
"""
def cargar_archivo(lista_clima):
    with open("clima2016-2020.csv") as archivo:
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
def define_años(lista_clima, ubicacion_fecha, años):
    fecha_repetida = 0
    lista_clima.pop(0)
    
    for i in range(len(lista_clima)):
        lista_clima[i][ubicacion_fecha] = lista_clima[i][ubicacion_fecha].split('/')
        
    for i in range(len(lista_clima)):
        chequeo=lista_clima[i][ubicacion_fecha][2] in años
        if (lista_clima[i][ubicacion_fecha][2] != fecha_repetida) and (chequeo == False) and (len(años) < 5):
            años.append(lista_clima[i][ubicacion_fecha][2])
            fecha_repetida=lista_clima[i][ubicacion_fecha][2]
    return años


"""
PRE-CONDICION: recibe un diccionario vacio, los datos del archivo csv, el indice de la columna de la fecha y una lista con los años.
POST-CONDICION: crea cinco listas con la informacion de cada año, las cuales seran los valores del diccionario.
                Las claves del diccionario son los años correspondientes.
                Devuelve un diccionario con la informacion.
"""
def diccionario_años(lista_clima, diccionario_clima, ubicacion_fecha, años):
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
def columna_temperatura(columna_temp, lista_clima):
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
def promedio_temperatura(promedios,diccionario_clima,años,columna_temp):
    suma = 0
    promedio = 0
    cont=0
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
def grafico_temp(diccionario_clima,años,columna_temp):
    promedios=[]
    promedio_temperatura(promedios,diccionario_clima,años,columna_temp)
    print(promedios)
    colores=["orangered","maroon","darkorange","gold", "brown"]
    plt.title("Promedio de Temperaturas de los últimos cinco años.")
    plt.bar(años, height=promedios, color=colores)
    plt.show()
    
"""
PRE-CONDICION:recibe una lista vacia y una lista con los datos del archivo.
POST-CONDICION: busca en el archivo csv las columnas que contienen el titulo Precipitation.
                Devuelve una lista con el indice de las columnas encontradas.
"""
def columna_precipitacion(lista_clima ,columna_precip):
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
def promedio_precipitacion(promedios_precipitacion,diccionario_clima,años,columna_precip):
    suma = 0
    promedio = 0
    cont = 0
    while cont < 5:
        lista = diccionario_clima[años[cont]]
        for i in range(len(lista)):
            for j in range(len(columna_precip)):
                suma += float(lista[i][columna_precip[j]])
            promedio = suma/len(lista)
        promedios_precipitacion.append(promedio)
        suma = 0
        promedio = 0
        cont += 1
    return promedios_precipitacion

"""
PRE-CONDICION: recibe el diccionario con los datos, la lista de los años y la lista con la ubicacion de los datos de precipitación.
POST-CONDICION: crea un grafico, que se muestra en pantalla, con los promedios de precipitación.
"""
def grafico_prep(diccionario_clima,años,columna_precip):
    promedios_precipitacion=[]
    promedio_precipitacion(promedios_precipitacion,diccionario_clima,años,columna_precip)
    print(promedio_precipitacion)
    colores=["midnightblue","royalblue","lightsteelblue","cornflowerblue", "slategrey"]
    plt.title("Promedio de Precipitaciones de los últimos cinco años.")
    plt.bar(años, height=promedios_precipitacion, color=colores)
    plt.show()
    
    
import csv
import matplotlib.pyplot as plt

def main():
    lista_clima = []
    diccionario_clima = {}
    años = []
    columna_temp = []
    columna_precip = []


    cargar_archivo(lista_clima)
    columna_temperatura(columna_temp, lista_clima)
    columna_precipitacion(lista_clima ,columna_precip)
    ubicacion_fecha = columna_fecha(lista_clima)
    define_años(lista_clima,ubicacion_fecha, años)
    diccionario_años(lista_clima,diccionario_clima, ubicacion_fecha, años)
    grafico_temp(diccionario_clima,años,columna_temp)
    grafico_prep(diccionario_clima,años,columna_precip)



main()




