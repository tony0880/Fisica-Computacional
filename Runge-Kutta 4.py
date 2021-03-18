import numpy as np
import matplotlib.pyplot as plt

def EvaluarFuncion (altura , presión):
    """
    Evaluar una variable en la función con la forma dp(t)/dy = -gM/R * p(y) * (293 - y/200)**(-1) 

    Parámetros de la función:
    ------------------------
    altura: Altura a la que se está calculando la presión

    presión: Presión del aire

    Salida de la función:
    ---------------------
    Derivada de la presión con respecto a la altura: Valor del cambio de presión con respecto a la altura.
    """
    return -9.8 * 0.0289647 / 8.134462 * (293 - altura / 200) ** (-1) * presión

def EjecutarRungeKutta4 (alturaInicial, valoresPresion, alturaFinal, tamañoIntervalos):
    """
    Ejecuta el método de Runge-Kutta 4 para el cálculo de una EDO 

    Parámetros de la función:
    ------------------------
    alturaInicial: Altura a la que se inicia el cálculo.

    valoresPresion: Presión variable del aire con respecto a la altura.

    alturaFinal: Altura a la que se espera el resultado final de la presión.
    
    tamañoIntervalos: Espaciado entre los intervalos de altura.

    Salida de la función:
    ---------------------
    Presión: Presión del aire a la altura final dada.
    """
    iContador = 0
    # Se define una variable iContador para contabilizar las iteraciones.
    # Se define la variable cantidadIntevalos para definir el n del método de Runge-Kutta. En este caso 
    # n es igual al número de intervalos y no al de puntos.

    while iContador < cantidadIntervalos:
        k1 = tamañoIntervalos * EvaluarFuncion (alturaInicial + iContador * tamañoIntervalos, valoresPresion[iContador])
        k2 = tamañoIntervalos * EvaluarFuncion (alturaInicial + iContador * tamañoIntervalos + tamañoIntervalos / 2, valoresPresion[iContador] + k1 / 2)
        k3 = tamañoIntervalos * EvaluarFuncion (alturaInicial + iContador * tamañoIntervalos + tamañoIntervalos / 2, valoresPresion[iContador] + k2 / 2)
        k4 = tamañoIntervalos * EvaluarFuncion (alturaInicial + iContador * tamañoIntervalos + tamañoIntervalos, valoresPresion[iContador] + k3)
        nuevaPresion = valoresPresion[iContador] +1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
        valoresPresion = valoresPresion + [nuevaPresion]
        iContador = iContador + 1
        # Se definen las kn con n = [1, 4] comos las pendientes para cada intervalo.
        
    else:
        return (valoresPresion) 

# Se establecen los parámetros iniciales
alturaInicial = 0
valoresPresion = [101325]
tamañoIntervalos = 100

# Se define el punto en el que se va a calcular presión
alturaFinal = 3000

# Se define la cantidad de intervalos a evaluar
cantidadIntervalos = (alturaFinal-alturaInicial)/tamañoIntervalos

valoresAltura = np.linspace( alturaInicial, alturaFinal, int(cantidadIntervalos + 1))

# Se ejecuta el programa
soluciónPresiónRK4 = EjecutarRungeKutta4 (alturaInicial, valoresPresion, alturaFinal, tamañoIntervalos)

#Se imprime el resultado en pantalla.
print ("El valor de presión para altura igual a " + str(alturaFinal) + " es de " + str (soluciónPresiónRK4 [-1]) + " con el método RK4")

# Gráfico
fig, ax = plt.subplots(dpi=120)
ax.plot(valoresAltura, soluciónPresiónRK4, label='Método RK4')
ax.set_xlabel('$Altura (m)$')
ax.set_ylabel('$Presión (Pa)$')
plt.legend(loc='best', prop={'size':10})
plt.title('Análisis de la presión en función de la altura')
plt.show()


