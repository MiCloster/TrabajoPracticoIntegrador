from PIL import Image
from geopy.geocoders import Nominatim

def encontrar_ubicacion(lat,long):
    """Determina la dirección correspondiente a la latitud y longitud ingresadas por el usuario
    pre: Recibe dos int
    post: Devuelve una lista con dos strings
    """
    coords = f"{lat}, {long}"
    MAIL = "mdelcastillo@fi.uba.ar"
    try:
        geolocator = Nominatim(user_agent = MAIL)
        direccion = geolocator.reverse(coords)
        dir_prov = direccion.raw
        if 'city' in dir_prov['address']:
            provincia = dir_prov['address']['city']
        elif 'state' in dir_prov['address']:
            provincia = dir_prov['address']['state']
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
        if not a_verificar.isnumeric():
            a_verificar = input(f"Ingreso una opcion inválida, ingrese un entero entre {primer_valor}  y {ultimo_valor}: ")
        else:
            a_verificar = int(a_verificar)
            if a_verificar < primer_valor or a_verificar > ultimo_valor:
                a_verificar = input(f"Ingreso una opcion inválida, ingrese un entero entre {primer_valor}  y {ultimo_valor}: ")
    return a_verificar

def suma_colores(im,CIUDAD):
    """ Analiza la circunferencia con centro predefinido, determinando la cantidad total de pixeles, y el color de cada uno
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
    """ Determino el tipo de alerta según el porcentaje de cada color respecto del total
    Tormenta fuerte con probabilidad de granizo: 0.8% pixeles rojos
    Tormenta moderada: 1.2% pixeles amarillos
    Tormenta débil: 7% pixeles verdes
    
    pre: Recibe un diccionario con claves total, rojos, amarillos y verdes
    post: Devuelve un string
    """
    PORCENTAJE_TORMENTA_F = 0.8/100
    PORCENTAJE_TORMENTA_M = 1.2/100
    PORCENTAJE_TORMENTA_D = 7.0/100
    if colores_contados["rojos"] >= (colores_contados["total"]*PORCENTAJE_TORMENTA_F):
        return "Tormenta fuerte con probabilidad de granizo"
    elif colores_contados["amarillos"] >= (colores_contados["total"]*PORCENTAJE_TORMENTA_M):
        return "Alerta: Tormenta moderada"
    elif colores_contados["verdes"] >= (colores_contados["total"]*PORCENTAJE_TORMENTA_D):
        return "Alerta: Tormenta débil"
    return "Sin alerta proxima"
    
def analisis_imagen():
    """ Carga la imagen elegida por el usuario y analiza el estado de alerta de cada ciudad que se localiza en esta 
    """
    CENTRO_NEUQUEN = (238,441)
    CENTRO_SANTA_ROSA = (358,342)
    CENTRO_CORDOBA = (360,129)
    CENTRO_BAHIA_BLANCA = (423,428)
    CENTRO_PERGAMINO = (484,232)
    CENTRO_PARANA = (488,144)
    CENTRO_CABA = (555,264)
    CENTRO_MAR_DEL_PLATA = (575,404)
    CENTRO_MERCEDES = (579,42)
    CENTRO_LA_PLATA = (571,279)
    CENTRO_PARANA = (488,144)
    
    imagen_electa = input("\nEscriba ubicación/nombre (sin formato) de la imagen .png a analizar (0 si desea usar una imagen predeterminada): ")
    imagen_electa = imagen_electa + ".png"
    try:
        im = Image.open(imagen_electa)
        im = im.convert("RGB")
        CIUDADES = {"Neuquén":CENTRO_NEUQUEN,"Santa Rosa":CENTRO_SANTA_ROSA,"Córdoba":CENTRO_CORDOBA,"Bahia Blanca":CENTRO_BAHIA_BLANCA,"Pergamino":CENTRO_PERGAMINO,"Parana":CENTRO_PARANA,"C.A.B.A.":CENTRO_CABA,"Mar del Plata":CENTRO_MAR_DEL_PLATA,"Mercedes":CENTRO_MERCEDES,"La Plata":CENTRO_LA_PLATA,"Paraná":CENTRO_PARANA}
        for i in CIUDADES:
            colores_contados = suma_colores(im,CIUDADES[i])
            alerta = declarar_alerta(colores_contados)
            print(alerta, "en", i)
    except:
        if imagen_electa == "0.png":
            print("La imagen predeterminada", imagen_electa, "fue eliminada o no se descargo correcramente")
        else:
            print("No existe imagen", imagen_electa, "con el formato correspondiente en la misma carpeta que el archivo .py")
