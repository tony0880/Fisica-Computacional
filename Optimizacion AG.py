# Se importa las bibliotecas necesarias.
import numpy as np
import random
import matplotlib.pyplot as plt
from time import time

# Se definen las variables iniciales.
iniciarTiempo = time ()

nGenes = 50
cantidadGeneraciones = 1000
tamañoPoblación = 100
p_mut = 1 / nGenes


def CargarCiudades():
    """
    Se definen las coordenadas de las ciudades del sistema.
    
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


def CodificacionCromosoma (nCiudades):
    """
    Codifica un cromosoma con los índices de cada ciudad y los ordena de forma aleatoria.
    
    Parámetros de la función:
    ------------------------
    cantidadCiuades: Número de ciudades presente en el sistema.
    
    Salida de la función
    ---------------------
    Cromosoma con los índices aleatorios de cada ciudad.

    """

    cromosoma = np.linspace (0, nCiudades-1, nCiudades)
    random.shuffle (cromosoma)
    return cromosoma


def FuncionAjuste (coordenadasCiudades, cromosoma):
    """
    Función que realiza el cálculo del valor de ajuste. Para este caso el inverso de la longitud euclidiana del trayecto.
    
    Parámetros de la función:
    ------------------------
    coordenadasCiudades: Puntos en el espacio donde se ubican las ciudades.
    cromosoma: Cromosoma con los índices de cada ciudad.
    
    Salida de la función
    ---------------------
    Valor de la función de ajuste.

    """

    suma = 0
    cantidadCiudades = len (cromosoma)
    for iCiudad in range (cantidadCiudades-1):
        ciudadActual = int(cromosoma [iCiudad])
        ciudadSiguiente = int(cromosoma [iCiudad + 1])
        posX = coordenadasCiudades [ciudadActual][0] - coordenadasCiudades [ciudadSiguiente][0]
        posY = coordenadasCiudades [ciudadActual][1] - coordenadasCiudades [ciudadSiguiente][1]
        suma += np.sqrt (posX**2 + posY**2)

    valorF = 1/suma
    return valorF


def OperadorMutación (cromosoma):
    """
    Función que muta un cromosoma dado, invirtiendo los índices de dos ciudades y lo expone a una probabilidad de aceptación.
    
    Parámetros de la función:
    ------------------------
    cromosoma: Cromosoma con los índices de cada ciudad.
    
    Salida de la función
    ---------------------
    Cromosoma mutado.

    """

    cantidadCiudades = len (cromosoma)
    for iCiudad in range (cantidadCiudades):
        probabilidad = random.random ()
        if probabilidad < p_mut:
            copiaCromosoma = np.copy(cromosoma)
            intercambioAleatorio = random.randint(0, cantidadCiudades-1)
            cromosoma [iCiudad] = copiaCromosoma [intercambioAleatorio]
            cromosoma [intercambioAleatorio] = copiaCromosoma [iCiudad]
    
    return cromosoma


def CrearPoblacion (cantidadCiudades):
    """
    Función crea una población con base a una cierta cantidad de individuos.
    
    Parámetros de la función:
    ------------------------
    cantidadCiuades: Número de ciudades presente en el sistema.
    
    Salida de la función
    ---------------------
    Lista con la información de la población del sistema, en esta se encuentran el cromosoma de cada individuo.

    """

    poblacion = []
    for individuo in range (tamañoPoblación):
        cromosoma = CodificacionCromosoma (cantidadCiudades)
        poblacion.append (cromosoma)

    return poblacion


def Graficar (coordenadas, trayecto, listaMejorValorAjuste, listaPromedioValorAjuste):
    """
    Función que grafica los resultados obtenidos.
    
    Parámetros de la función:
    ------------------------
    coordenadas: Puntos en el espacio para cada una de las ciudades.
    trayecto: Recorrido óptimo realizado por un individuo durante la simulación.
    listaMejorValorAjuste: Lista con los mejores valores de ajuste realizados para cada generación.
    listaPromedioValorAjuste: Lista con el promedio de los valores de ajustes para cada generación.

    Salida de la función
    ---------------------
    Gráfica con el trayecto más corto realizado por un individuo.
    Gráfica comparativa del mejor valor de ajuste y el promedio del mismo para cada generación.

    """

    ejeX = []
    ejeY = []
    for nPunto in range (len (trayecto)):
        punto = int(trayecto [nPunto])
        puntoX = coordenadas [punto][0]
        puntoY = coordenadas [punto][1]
        ejeX.append (puntoX)
        ejeY.append (puntoY)
    ejeX.append (ejeX[0])
    ejeY.append (ejeY[0])
    fig, ax = plt.subplots (dpi = 120)  
    ax.set_title ("Movimiento óptimo por AG")

    ax.set_xlabel ('x (m)')
    ax.set_ylabel ('y (m)')
    ax.plot (ejeX, ejeY)
    plt.plot (ejeX, ejeY, marker = '^', color = 'blue')
    plt.plot (ejeX[0], ejeY[0], marker = "o", color = "red" )
    plt.get_current_fig_manager().window.showMaximized ()


    fig, ax2 = plt.subplots (dpi = 120)
    ax2.plot (listaMejorValorAjuste, label = 'ajuste maximo')
    ax2.plot (listaPromedioValorAjuste, label = 'ajuste promedio')
 
    ax2.set_title ('Evolucion de los valores de ajuste de la poblacion')
    ax2.set_xlabel ('Generaciones')
    ax2.set_ylabel ('Valores de ajuste')
    ax2.legend (loc = 'best')

    plt.show ()


def OptimizacionAG (tiempoInicial):
    """
    Función principal para obtener el recorrido con menor distancia entre varias ciudades.
    
    Parámetros de la función:
    ------------------------
    tiempoInicial: Valor del tiempo cuando se inicia la simulación.

    Salida de la función
    ---------------------
    Trayecto con menor distancia realizado por cierto individuo.

    """

    # Se obtienen las coordenadas y la cantidad de ciudades.
    ciudades = CargarCiudades ()
    cantidadCiudades = len (ciudades)

    valorAjusteMaximo = 0

    # Genera la población inicial.
    poblacion = CrearPoblacion (cantidadCiudades)

    coleccionPromedioValorAjuste = []
    coleccionMejorValorAjuste = []

    # Se define un bucle para cumplir con las generaciones deseadas.
    for iGeneracion in range (cantidadGeneraciones):
        coleccionValorAjuste = []

        # Se define un bucle para recorrer todos los individuos de la población.
        for nIndividuo in range (tamañoPoblación):
            cromosoma = poblacion [nIndividuo]

            # Se obtiene el valor de ajuste para el individuo estudiado y se almacena en una lista.
            valorAjuste = FuncionAjuste (ciudades, cromosoma)
            coleccionValorAjuste.append (valorAjuste)

            # Se define un condicional para imprimir resultados cuando se mejore el recorrido.
            if valorAjuste > valorAjusteMaximo:
                valorAjusteMaximo = valorAjuste
                cromosomaBueno = cromosoma
                print('Para la Generación {}, Individuo {}: longitud del camino más corto = {}'.format(iGeneracion, nIndividuo, 1/valorAjusteMaximo))
                
                tiempoTranscurrido = time () - tiempoInicial
                print ('Tiempo transcurrido: ', tiempoTranscurrido)

            # Se muta el cromosoma del individuo estuduado para pasar al siguiente.
            cromosoma = OperadorMutación (cromosoma)

        # Se almacena el mejor valor de ajuste de la generación en una lista.
        coleccionMejorValorAjuste.append (valorAjusteMaximo)

        # Se obtiene el promedio de los valores de ajuste de la generación y se almacena en una lista.
        promedioValorAjuste = np.mean (coleccionValorAjuste)
        coleccionPromedioValorAjuste.append (promedioValorAjuste)
 
        # Se redefine la población.
        poblacion = []
        for individuo in range (tamañoPoblación):
            poblacion.append (cromosomaBueno)
    
    # Se grafican los resultados y se guardan en un archivo txt.
    cromosomaBueno = np.array (cromosomaBueno)
    np.savetxt ("caminoMásCorto_AGE.txt", cromosomaBueno)
    Graficar (ciudades, cromosomaBueno, coleccionMejorValorAjuste, coleccionPromedioValorAjuste)


OptimizacionAG(iniciarTiempo)