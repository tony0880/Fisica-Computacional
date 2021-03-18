# Se importan la biblioteca integrate para el cálculo de integrales y
# "x" para su uso como variable en la integral
from sympy import integrate
from sympy.abc import x


def Picard (xInicial, yIterador, xFinal):
    """
    Ejecuta el método de Picard para el cálculo de EDO.

    Parámetros de la función:
    ------------------------
    xInicial: Este es el límite inferior de la integral.
    yIterador: Valor de y que cambiará con cada iteración. Se le asignará un valor inicial.
    xFinal: Este es el límite superior de la integral.

    Salida de la función:
    ---------------------
    Resultado aproximado de la EDO.
    """
    iteracion = 0
    diferencia = 1
    # Se define una variable diferencia que será quien determine el final del programa.
    # Se le asigna un valor inicial de 1 para cumplir la condición de la primer iteración.
    
    función = x + yIterador ** 2 

    # Se define la variable función la cual es obtenida por la EDO.

    while diferencia > 0.00001:
        nueva_yIterador = integrate (función, (x, xInicial, xFinal))
        diferencia = abs (yIterador - nueva_yIterador)
        # Se realiza el cáclulo de una integral definida para obtener el valor numérico de "y". Esta es comparada con su
        # valor anterio para determinar la diferencia entre estas.

        función = x + integrate (función) ** 2 
        # Se redefine la variable función con el nuevo valor de "y", obtenido por el cálculo de la integral indefinida 
        # de su expresión anterior.

        yIterador = nueva_yIterador

        print (' y_' + str (iteracion) + ' = ' + str (yIterador))
        print (' La nueva función a evaluar es ' + str (función))
          
        iteracion = iteracion + 1   

# Se establecen los parámetros iniciales
xInicial = 0
yIterador = 0

# Se define el punto en el que se va a calcular y
xFinal = 0.3

Picard (xInicial, yIterador, xFinal)

