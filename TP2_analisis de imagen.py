from PIL import Image

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
    
def main():
    try:
        im = Image.open("imagen_a_analizar.png")
        im = im.convert("RGB")
        CIUDADES = {"Neuquén":(238,441),"Santa Rosa":(358,342),"Córdoba":(360,129),"Bahia Blanca":(423,428),"Pergamino":(484,232),"Parana":(488,144),"C.A.B.A.":(555,264),"Mar del Plata":(575,404),"Mercedes":(579,42),"La Plata":(571,279),"Paraná":(488,144)}
        for i in CIUDADES:
            colores_contados = suma_colores(im,CIUDADES[i])
            alerta = declarar_alerta(colores_contados)
            print(alerta, "en", i)
    except:
        print("No exsiste imagen imagen_a_analizar.png en la misma carpeta que el archivo .py")
main()


