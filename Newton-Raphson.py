# Se importa la función de la raíz cuadrada de la biblioteca math para el cálculo del error.

from math import sqrt

def EvaluarFuncion(variableTiempo):
    """
    Evaluar una variable en la función con la forma f(t) = x_0 + v_0 * t + (a * t ** 2) / 2.

    Parámetros de la función:
    ------------------------
    variableTiempo: Tiempo en el cual se evaluará la función de desplazamiento.

    Salida de la función:
    ---------------------
    Posición: Posición en la que se encontrará el movil para el tiempo determinado.
    """
    return - 5 + 0.005 * variableTiempo ** 2

def EvaluarDerivadaFuncion(variableTiempo):
    """
    Evaluar una variable en la derivada de la función ya definida con la forma f(t) =v_0 + a * t.

    Parámetros de la función:
    ------------------------
    variableTiempo: Tiempo en el cual se evaluará la función de velocidad.

    Salida de la función:
    ---------------------
    Velocidad: Velocidad que poseerá el movil para el tiempo determinado.
    """
    return 0.01 * variableTiempo

def CalcularError (kTiempo):
    """
    Calcular el error entre el valor exacto y el dado como variable. Para este caso específico se obtiene 
    que el resultado exacto del problemas es 10 * sqrt(10)

    Parámetros de la función:
    ------------------------
    kTiempo: Tiempo que será comparado con el tiempo esperado.

    Salida de la función:
    ---------------------
    Error: Error entre el valor de tiempo dado y el valor exacto.
    """
    return abs (kTiempo - 10 * sqrt (10)) / (10 * sqrt (10))
    
def EjecutarNewtonRaphson (kTiempo):
    """
    Ejecutar el método de Newton Raphson para una variable dada.

    Parámetros de la función:
    ------------------------
    kTiempo: Tiempo que será comparado con el tiempo esperado.

    Salida de la función:
    ---------------------
    Error: Error entre el valor de tiempo dado y el valor exacto.
    """
    error = 1
    iContador = 1
    # Se toma un error del 100% para iniciar el cálculo y se define una 
    # variable iContador la cual llevará el registro de iteraciones.
    while error > 0.01:
        # La ecuación para obtener el valor siguiente de kTiempo se toma del libro de Klein y no de la mostrada en clase.
        kTiempo = kTiempo - EvaluarFuncion (kTiempo) / EvaluarDerivadaFuncion (kTiempo)
        # Se define como límite para las iteraciones, que el error sea menor al 1%.
        error = CalcularError (kTiempo)
        iContador = iContador + 1
    else:
        return kTiempo, error, iContador

    
# Ejecución de la función.
tiempoX_0 = EjecutarNewtonRaphson (40)

# Impresión del resultado final.
print ("El momento en el que el móvil se encuentra en la posición de 0m es en " + str (tiempoX_0 [0]) +"s.")
print ("Con un error del " + str ( round(tiempoX_0 [1] *100, 7)) + "%.")
print ("Este cálculo requiere de " + str (tiempoX_0 [2]) + " iteraciones para cumplir con el error dado.")
