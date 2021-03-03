def EvaluarFuncion (variableTiempo):
    """
    Evaluar una variable en la función con la forma f(t) = v_0 + a * t.

    Parámetros de la función:
    ------------------------
    variableTiempo: Tiempo en el cual se evaluará la función de desplazamiento.

    Salida de la función:
    ---------------------
    Posición: Posición en la que se encontrará el movil para el tiempo determinado.
    """

    # Se obtiene que para el problema planteado se experimenta una aceleración de 0.005 m/s**2 y una velocidad incial de 0.5 m/s.
    return 0.5 + 0.005 * variableTiempo
    
def EjecutarMetodoSimpson (limiteInferior,limiteSuperior,intervalos):
    """
    Ejecutar el método de Simpson para los valores brindados.

    Parámetros de la función:
    ------------------------
    límiteInferior: Valor de "a" en el método de Simpson. Define el límite inferior de la integral.

    límiteSuperior: Valor de "b" en el método de Simpson. Define el límite superior de la integral.

    intervalos: Valor de "n" en el método de Simpson. Define la cantidad de intervalos en los que se aplicará el método.

    Salida de la función:
    ---------------------
    Desplazamiento: Resultado aproximado de la integral. Para este caso específico se obtiene el desplazamiento total del móvil
    los valores indicados. 
    """

    tamañoIntervalos = (limiteSuperior-limiteInferior)/(intervalos)
    # Para el método de Simpson se define la variable n como número de intervalos a calcular.
    iContador = 0
    suma = 0
    while iContador < intervalos + 1:
        if iContador == 0 or iContador == intervalos:
            suma = suma + EvaluarFuncion (limiteInferior + tamañoIntervalos * iContador)
            iContador = iContador + 1
        elif iContador % 2 == 0:
            suma = suma + 2 * EvaluarFuncion (limiteInferior + tamañoIntervalos * iContador)
            iContador = iContador +     1
        else:
            suma = suma + 4 * EvaluarFuncion (limiteInferior + tamañoIntervalos * iContador)
            iContador = iContador + 1
    else:
        return tamañoIntervalos / 3 * suma

# Se definen los valores inicales como:

a = 0
b = 100
n = 4

# Ejecución de la función.
desplazamientoMovil = EjecutarMetodoSimpson (a, b, n)

# Impresión del resultado final.
print ("El desplazamiento del móvil a los 100s es de " + str (desplazamientoMovil) + "m.")

