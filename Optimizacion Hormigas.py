# Se importa las bibliotecas necesarias.
import numpy as np
import random 
import matplotlib.pyplot as plt
from time import time
from numpy.matrixlib.defmatrix import matrix

# Se definen las variables inciales.
iniciarTiempo = time ()
cantidadHormigas = 20
alpha = 2
beta = 2.5
rho = 0.25


def CargarCiudades():
    """
    Se definen las coordenadas de las ciudades del sistema
    
    Parámetros de la función:
    ------------------------
    No se tienen parámetros para la función.
    
    Salida de la función
    ---------------------
    Lista con los puntos específicos para cada ciudad del sistema.

    """

    coordenadasCiudades = [[0.2554, 18.2366],[0.4339, 15.2476],[0.7377, 8.3137],[1.1354, 16.5638],[1.5820, 17.3030],[2.0913, 9.2924],
[2.2631, 5.3392],[2.6373, 2.6425],[3.0040, 19.5712],[3.6684, 14.8018],[3.8630, 13.7008],[4.2065, 9.8224],[4.8353, 2.0944],[4.9785, 3.1596],
[5.3754, 17.6381],[5.9425, 6.0360],[6.1451, 3.8132],[6.7782, 11.0125],[6.9223, 7.7819],[7.5691, 0.9378],[7.8190, 13.1697],[8.3332, 5.9161],
[8.5872, 7.8303],[9.1224, 14.5889], [9.4076, 9.7166],[9.7208, 8.1154],[10.1662, 19.1705],[10.7387, 2.0090],[10.9354, 5.1813],[11.3707, 7.2406],
[11.7418, 13.6874],[12.0526, 4.7186],[12.6385, 12.1000],[13.0950, 13.6956],[13.3533, 17.3524],[13.8794, 3.9479],[14.2674, 15.8651],
[14.5520, 17.2489],[14.9737, 13.2245],[15.2841, 1.4455],[15.5761, 12.1270],[16.1313, 14.2029],[16.4388, 16.0084], [16.7821, 9.4334],
[17.3928, 12.9692],[17.5139, 6.4828],[17.9487, 7.5563],[18.3958, 3.5112],[18.9696, 19.3565], [19.0928, 16.5453]]
    return coordenadasCiudades


def FeromonasIniciales (cantidadCiudades, tao0):
    """
    Se obtiene una matriz cuadrada con los valores de las feromonas inicales del sistema.
    
    Parámetros de la función:
    ------------------------
    cantidadCiuades: Número de ciudades presente en el sistema.
    tao0: Constante que da el valor a las feromonas iniciales.
    
    Salida de la función
    ---------------------
    Matriz con las feromonas del sistema.

    """

    nivelFeromonas = np.zeros ((cantidadCiudades, cantidadCiudades)) + tao0
    return nivelFeromonas


def ObtenerLongitudCaminoMasCercano (coordenadasCiudades, ciudadActual):
    """
    Se obtiene el trayecto más corto para una ubicación dada.
    
    Parámetros de la función:
    ------------------------
    coordenadasCiudades: Puntos en el espacio donde se ubican las ciudades.
    ciudadActual: Ciudad en la que se inicia el recorrido de la hormiga.
    
    Salida de la función
    ---------------------
    Distancia total recorrida por la hormiga a las ciudades más cercanas.

    """

    nCiudades = len (coordenadasCiudades)
    listaTabu = [ciudadActual]
    distancia = 0
    
    for iIteracion in range (nCiudades - 1):
        longitudCaminoMásCercano = 1e5
        for nuevaCiudad in range (nCiudades):
            if nuevaCiudad == ciudadActual or nuevaCiudad in listaTabu:
                pass
            else:
                posicionActual = coordenadasCiudades [ciudadActual]
                nuevaPosicion = coordenadasCiudades [nuevaCiudad]
                nuevalongitud = np.sqrt ((posicionActual[0]-nuevaPosicion[0])**2 + (posicionActual[1]-nuevaPosicion[1])**2)
                if nuevalongitud < longitudCaminoMásCercano:
                    longitudCaminoMásCercano = nuevalongitud
                    ciudadMasCercana = nuevaCiudad

        ciudadActual = ciudadMasCercana
        listaTabu.append (ciudadActual)
        distancia += longitudCaminoMásCercano
    return distancia


def ObtenerProbabilidad (cantidadCiudades, nivelFeromonas, visibilidad, jCiudad, iCiudad, listaTabu):
    """
    Se obtiene la probabilidad de aceptación para una ciudad dada.
    
    Parámetros de la función:
    ------------------------
    cantidadCiuades: Número de ciudades presente en el sistema.
    nivelFeromonas: Matriz con los valores de las feromonas del sistema.
    visibilidad: Matriz con los valores de visibilidad del sistema.
    jCiudad: Ciudad en la que se encuentra la hormiga.
    iCiudad: Ciudad en a la que se quiere desplazar la hormiga.
    listaTabú: Lista con las ciudades que ya visitó la hormiga.
    
    Salida de la función
    ---------------------
    Probabilidad de aceptación de que la hormiga se desplace a cierta ciudad.

    """
    
    suma = 0
    for mCiudad in range (cantidadCiudades):
        if mCiudad not in listaTabu:
            suma += (nivelFeromonas [mCiudad][jCiudad])**alpha * (visibilidad [mCiudad][jCiudad])**beta

    probabilidad = (nivelFeromonas [iCiudad][jCiudad])**alpha * (visibilidad [iCiudad][jCiudad])**beta / suma
    return probabilidad


def ObtenerNuevaCiudad(matrizProbabilidad):
    """
    Función que define a cual ciudad se debe desplazar la hormiga.
    
    Parámetros de la función:
    ------------------------
    matrizProbabilidad: Matriz que contiene la lista de probabilidades con su respectiva ciudad.
    
    Salida de la función
    ---------------------
    Ciudad a la que se debe desplazar la hormiga.

    """
    matrizProbabilidadOrdenada = sorted (matrizProbabilidad, reverse = True)

    for iCiudad in range (len(matrizProbabilidad)):
        probabilidadMayor = matrizProbabilidadOrdenada [iCiudad][0]
        probabilidad = random.random ()

        if probabilidad < probabilidadMayor:
            nuevaCiudad = matrizProbabilidadOrdenada [iCiudad][1]
            return nuevaCiudad

    nuevaCiudad = matrizProbabilidadOrdenada [0][1]
    return nuevaCiudad
    

def ConstruirTrayecto (nivelFeromonas, visibilidad, cantidadCiudades):
    """
    Función que establece el trayecto que debe seguir una hormiga con base a la visibilidad y al nivel de feromonas.
    
    Parámetros de la función:
    ------------------------
    nivelFeromonas: Matriz con los valores de las feromonas del sistema.
    visibilidad: Matriz con los valores de visibilidad del sistema.
    cantidadCiuades: Número de ciudades presente en el sistema.
    
    Salida de la función
    ---------------------
    Lista con las ciudades ordenadas que debe recorrer la hormiga.

    """

    jCiudad = random.randint (0, cantidadCiudades - 1)
    listaTabu = [jCiudad]
    for jIteracion in range (cantidadCiudades - 1):
        matrizProbabilidad = []
        for iCiudad in range (cantidadCiudades):
            if iCiudad not in listaTabu:
                probabilidad = ObtenerProbabilidad (cantidadCiudades, nivelFeromonas, visibilidad, jCiudad, iCiudad, listaTabu)
                matrizProbabilidad.append ([probabilidad, iCiudad])

        jCiudad = ObtenerNuevaCiudad (matrizProbabilidad)

        listaTabu.append (jCiudad)

    caminoRecorrido = listaTabu
    
    return caminoRecorrido
        

def DistanciaRecorrida (trayecto, coordenadasCiudades):
    """
    Función que establece la distancia total recorrida por la hormiga.
    
    Parámetros de la función:
    ------------------------
    trayecto: Lista con el orden que debe seguir la hormiga para cada ciudad.
    coordenadasCiudades: Puntos en el espacio donde se ubican las ciudades.

    Salida de la función
    ---------------------
    Distancia total de la hormiga para el trayecto dado.

    """
    cantidadCiudades = len(trayecto)
    distancia = 0
    for iContador in range (cantidadCiudades-1):
        ciudadActual = trayecto [iContador]
        ciudadSiguiente = trayecto [iContador + 1]
        posX = coordenadasCiudades [ciudadActual][0] - coordenadasCiudades [ciudadSiguiente][0]
        posy = coordenadasCiudades [ciudadActual][1] - coordenadasCiudades [ciudadSiguiente][1]
        distancia += np.sqrt (posX**2 + posy**2)
    return distancia


def CálculoDeltaTau(colecciónCaminos, colecciónLongitudCaminos):
    """
    Función que determina el valor del deltaTao.
    
    Parámetros de la función:
    ------------------------
    colecciónCaminos: Lista con todos los trayectos realizados por la hormiga.
    colecciónLongitudCaminos: Lista con las distancias recorridas por la hormiga.

    Salida de la función
    ---------------------
    Valor del DeltaTao en el sistema.

    """

    cantidadCiudades = len (colecciónCaminos [0])
    nCaminos = len(colecciónCaminos)

    deltaTauTemp = np.zeros ((cantidadCiudades, cantidadCiudades, nCaminos))

    deltaTau = np.zeros ((cantidadCiudades, cantidadCiudades))

    for kHormiga in range (nCaminos):
        for iCiudad in range (cantidadCiudades - 1):
            for jCiudad in range (iCiudad, cantidadCiudades):
                ciudadActual = colecciónCaminos [kHormiga] [iCiudad]
                ciudadSiguiente = colecciónCaminos [kHormiga] [jCiudad]
                distancia = colecciónLongitudCaminos [kHormiga]
                deltaTauTemp [ciudadActual, ciudadSiguiente, kHormiga] = 1/distancia 

    for camino in range (nCaminos):
        deltaTau += deltaTauTemp [:,:,camino]

    return deltaTau

def ObtenerVisibilidad(coordCiudades):
    """
    Función que obtiene la visibilidad en el sistema para las hormigas.
    
    Parámetros de la función:
    ------------------------
    coordenadasCiudades: Puntos en el espacio donde se ubican las ciudades.

    Salida de la función
    ---------------------
    Matriz cuadrada con los valores de visibilidad en el sistema.

    """

    nCiudades = len(coordCiudades)
    arregloVisibilidad = np.zeros((nCiudades , nCiudades))
    
    for ciudadActual in range(nCiudades):
        for ciudadSiguiente in range(nCiudades):
            if ciudadActual != ciudadSiguiente:
                deltaX = coordCiudades[ciudadSiguiente][0]-coordCiudades[ciudadActual][0]
                deltaY= coordCiudades[ciudadSiguiente][1]-coordCiudades[ciudadActual][1]
                longitudCamino=np.sqrt(deltaX**2+deltaY**2)   
                arregloVisibilidad[ciudadActual , ciudadSiguiente] = 1/longitudCamino
                arregloVisibilidad[ciudadSiguiente , ciudadActual] = 1/longitudCamino
                
    return arregloVisibilidad

def ActualizarNivelFeromonas(nivelFeromonas, deltaNivelFeromonas):
    """
    Función que obtiene las feromonas luego de que se completara el trayecto para una hormiga.
    
    Parámetros de la función:
    ------------------------
    nivelFeromonas: Matriz con los valores de las feromonas del sistema.
    deltaNivelFeromonas: Valor del deltaTao.

    Salida de la función
    ---------------------
    Nivel de feromonas actualizado luego de que cada hormiga realice su trayecto.

    """
    nivelFeromonasActualizado = (1-rho) * nivelFeromonas + deltaNivelFeromonas

    return nivelFeromonasActualizado


def Graficar (coordenadas, trayecto):
    """
    Función que grafica los resultados obtenidos.
    
    Parámetros de la función:
    ------------------------
    coordenadas: Puntos en el espacio para cada una de las ciudades.
    trayecto: Recorrido óptimo realizado por una homiga durante la simulación

    Salida de la función
    ---------------------
    Gráfica con el trayecto más corto realizado por una hormiga.

    """
    ejeX = []
    ejeY = []
    for nPunto in range (len (trayecto)):
        punto = trayecto [nPunto]
        puntoX = coordenadas [punto][0]
        puntoY = coordenadas [punto][1]
        ejeX.append (puntoX)
        ejeY.append (puntoY)
    ejeX.append (ejeX[0])
    ejeY.append (ejeY[0])
    fig, ax = plt.subplots (dpi = 120)  
    ax.set_title ("Movimiento óptimo por SH") 


    ax.set_xlabel ('x (m)')
    ax.set_ylabel ('y (m)')
    ax.plot (ejeX, ejeY)
    plt.plot (ejeX, ejeY, marker = '^', color = 'blue')
    plt.plot (ejeX[0], ejeY[0], marker = "o", color = "red" )
    plt.get_current_fig_manager().window.showMaximized ()
    plt.show()


def OptimizacionHormigas (tiempoInicial):
    """
    Función principal para obtener el recorrido con menor distancia entre varias ciudades.
    
    Parámetros de la función:
    ------------------------
    tiempoInicial: Valor del tiempo cuando se inicia la simulación.

    Salida de la función
    ---------------------
    Trayecto con menor distancia realizado por cierta hormiga.

    """

    ciudades = CargarCiudades ()
    cantidadCiudades = len(ciudades)

    menorDistancia = 1e4
    menorDistanciaDeseada = 120

    iIteración = 0

    ciudadInicial = random.randint (0, cantidadCiudades - 1)
    distanciaMinima = ObtenerLongitudCaminoMasCercano (ciudades, ciudadInicial)
    tao0 = cantidadHormigas / distanciaMinima

    nivelFeromonas = FeromonasIniciales (cantidadCiudades, tao0)

    visibilidad = ObtenerVisibilidad (ciudades)

    while menorDistancia > menorDistanciaDeseada:
        iIteración += 1
        coleccionCaminos = []
        coleccionDistancia = []

        if iIteración > 100:
            menorDistanciaDeseada = 50000
            print ('No se alcanzó la distancia deseada en 100 interaciones.')

        for kHormiga in range (1, cantidadHormigas):
            trayecto = ConstruirTrayecto (nivelFeromonas, visibilidad, cantidadCiudades)

            distanciaRecorrida = DistanciaRecorrida (trayecto, ciudades)


            if distanciaRecorrida < menorDistancia:
                menorDistancia = distanciaRecorrida
                print('Iteración {}, hormiga {}: longitud del camino más corto = {}'.format(iIteración, kHormiga, menorDistancia))
                menorCamino = trayecto

                tiempoTranscurrido = time () - tiempoInicial
                print ('Tiempo transcurrido: ', tiempoTranscurrido)


            coleccionCaminos.append (trayecto)
            coleccionDistancia.append (distanciaRecorrida)


            deltaTau = CálculoDeltaTau(coleccionCaminos, coleccionDistancia)
            nivelFeromonas = ActualizarNivelFeromonas(nivelFeromonas, deltaTau)
    
    
    
    menorCamino = np.array (menorCamino)
    np.savetxt ("caminoMásCorto_SH.txt", menorCamino)
    Graficar (ciudades, menorCamino)


OptimizacionHormigas (iniciarTiempo)


