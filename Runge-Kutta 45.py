from scipy import integrate
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

# Se establecen los parámetros iniciales
alturaInicial = 0
presiónIteradora = 101325
tamañoIntervalos = 100


# Se define el punto en el que se va a calcular presión
alturaFinal = 3000

# Se define la cantidad de puntos a evaluar
cantidadPuntos = (alturaFinal-alturaInicial)/tamañoIntervalos +1

# Se define una variable con el resultado de todas las variables que contempla la función integrate.solve.ivp.
# Se debe tener cuidado, pues este método da como resultado varias variables. Por lo que se debe especificar cual de estas
# Se necesita y a su vez si solo se requiere un resultado o todo el arreglo.

soluciónDescriptivaRK45 = integrate.solve_ivp (EvaluarFuncion, [alturaInicial, alturaFinal], [presiónIteradora] ,\
     t_eval=np.linspace( alturaInicial, alturaFinal, int(cantidadPuntos)))

#Se define la variable con la respuesta requerida para una altura deseada.
soluciónPresionRK45 = soluciónDescriptivaRK45.y [0]
soluciónAlturaRK45 =  soluciónDescriptivaRK45.t


#Se imprime el resultado en pantalla.
print ("El valor de presión para altura igual a " + str(alturaFinal) + "m es de " + str (soluciónPresionRK45 [-1]) + "Pa con el método RK45")


# Gráfico
fig, ax = plt.subplots(dpi=120)
ax.plot(soluciónAlturaRK45, soluciónPresionRK45, label='Método RK45')
ax.set_xlabel('$Altura (m)$')
ax.set_ylabel('$Presión (Pa)$')
plt.legend(loc='best', prop={'size':10})
plt.title('Análisis de la presión en función de la altura')
plt.show()