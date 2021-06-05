# Importación de bibliotecas necesarias.
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import random


def CaminoAletorio(listaPosiciones, nIter):
    """
    Elige una dirección en los tres ejes, por lo que se puede mover una partícula.

    Parámetros de la función:
    ------------------------
    listaPosiciones: Lista que almacena las diversa posiciones en los 3 ejes para una partícula.
    nIter: Iterador sobre los pasos que lleva la partícula.

    Salida de la función
    ---------------------
    Lista de posiciones actualizada con el último movimento realizado.
    Ultima posición para los ejes X, Y, Z.
    """

    #Se define el tamaño de cada paso realizado por la partícula.
    l = 5*10**(-5)

    # Se calcula la posición en X con un número aleatorio en un rango de -l y l, luego se calcula la posición en Ycon el mismo rango restando
    # el valor de xPos. Finalmente se calcula la posición en Zs con el único valor restante para que el R entre las tres variables sea igual a l.
    xPos= random.uniform(-l, l)
    yPos = random.uniform (-l + np.abs(xPos), l- np.abs(xPos))
    zPos= np.sqrt (l**2 - xPos**2 - yPos**2)
    
    # Se define la nueva posición con base a los valores antes calculados.
    nuevaxPos = listaPosiciones[0][nIter-1] + xPos
    nuevayPos = listaPosiciones[1][nIter-1] + yPos
    nuevazPos = listaPosiciones[2][nIter-1] + zPos
    
    # Se añade esta posición a la lista con las posiciones.
    listaPosiciones[0].append(nuevaxPos)
    listaPosiciones[1].append(nuevayPos)
    listaPosiciones[2].append(nuevazPos)
    return listaPosiciones, xPos, yPos, zPos


# Se define una lista de 3 dimensiones incializada en 0
camino = [[0.],[0.], [0.]]
# Se define el tamaño del radio al que se desea alcanzar
radio = 5*10**(8)
# Se define una lista con los desplazamiento en cada eje por la partícula.
desplazamiento = [0, 0, 0]
# Se inicializan las variables de R, pasos y n, donde n es un contador para contabilizar los millones de pasos que se tienen.
R = 0
pasos = 1
n=1

# Se define un bucle en el que se calcula una nueva posición para la partícula mientras el R obtenido no sea mayor al radio deseado.
while R <= radio:  
    calculoCamino = CaminoAletorio(camino, pasos)
    camino = calculoCamino [0]
    desplazamiento[0] += calculoCamino [1] 
    desplazamiento[1] += calculoCamino [2]
    desplazamiento[2] += calculoCamino [3]
    R = np.sqrt (desplazamiento[0]**2 + desplazamiento[1]**2 + desplazamiento[2]**2) 
    pasos += 1
    # Condicional para que cada múltiplo de un millón de pasos, se imprima en consola el desplazamiento y los pasos realizado.
    if pasos == n*10**6:
        n += 1
        print ("Desplazamiento del fotón desde el centro es de: ", R)
        print ("Para una cantidad de pasos de: ", pasos)

    # Condicional para obtener la máxima distancia posible por la computadora.
    # if pasos == 290*10**6:
    #     radio = 0

    # Condicional para lograr obtener una gráfica de recorrido
    if pasos == 10**6:
        radio = 0

   
# Gráficación
ejeX = camino [0]
ejeY = camino [1]
ejeZ = camino [2]
fig = plt.figure ()
ax = plt.axes (projection = '3d')    
ax.set_title ("Movimiento aleatorio de una partícula en 3 dimensiones"
"\n" 
        r"con un R igual a:" + str(R))

ax.set_xlabel ('x (m)')
ax.set_ylabel ('y (m)')
ax.set_zlabel ('z (m)')
ax.plot (ejeX, ejeY, ejeZ)
plt.get_current_fig_manager().window.showMaximized ()
plt.show()


