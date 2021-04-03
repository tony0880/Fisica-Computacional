# Se importan las bicliotecas.
import numpy as np 
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.fft import ifft

# Parámetros.
tasaMuestreo = 1024
deltaT =1

# Tamaño del arreglo de muestras.
nPuntos = deltaT * tasaMuestreo

# Arreglo de puntos para la coordenada temporal.
puntosTiempo = np.linspace (0, deltaT, nPuntos)

# Se definen las frecuencias y magnitudes para las señales.
frecuencia1 = 75
magnitud1 = 40

frecuencia2 = 50
magnitud2 = 47

frecuencia3 = 25
magnitud3 = 32

frecuencia4 = 100
magnitud4 = 38

frecuencia5 = 125
magnitud5 = 42

# Se crean las señales.
señal1 = magnitud1*np.sin(2*np.pi*frecuencia1*puntosTiempo)
señal2 = magnitud2*np.cos(2*np.pi*frecuencia2*puntosTiempo)
señal3 = magnitud3*np.sin(2*np.pi*frecuencia3*puntosTiempo)
señal4 = magnitud4*np.cos(2*np.pi*frecuencia4*puntosTiempo)
señal5 = magnitud5*np.sin(2*np.pi*frecuencia5*puntosTiempo)

# Ruido para la señal.
ruido = np.random.normal (0, 100, nPuntos)

# Se definen las señal pura y ruidosa.
señalPura = señal1 + señal2 + señal3 + señal4 + señal5
señalRuidosa = señal1 + señal2 + señal3 + señal4 + señal5 + ruido


# Graficación de ambas señales.
fig, (ax1, ax2) = plt.subplots(1, 2, dpi=120, sharey= True)
ax1.plot(puntosTiempo[0:50], señalPura[0:50])
ax1.set_title('Señal original')
ax1.set_xlabel('Tiempo')
ax1.set_ylabel('Amplitud')

ax2.plot(puntosTiempo[1:50], señalRuidosa[1:50])
ax2.set_title('Señal ruidosa')
ax2.set_xlabel('Tiempo')

plt.show()


#==============================================
# Aplicación de la transformada.


# Se definen los puntos de cada frecuencia.
puntosFrecuencia = np.linspace (0.0, nPuntos, int(nPuntos))

# Se aplica la transformada rapida a la señal.
transformadaSeñal = fft(señalRuidosa)

# Se define el valor de la amplitud de cada frecuencia.
amplitudes = (2/nPuntos)*np.abs(transformadaSeñal)


# Graficación de las amplitudes para cada frecuencia
fig, ax = plt.subplots(dpi=120)
ax.plot(puntosFrecuencia, amplitudes)
ax.set_title('Señal en el dominio de la frecuencia')
ax.set_xlabel('Frecuencia [Hz]')
ax.set_ylabel('Amplitud')

plt.show()


#==============================================
# Filtrado de la señal


def EncontarUmbralFiltrado (listaAmplitudes):
    """
    Encuentra el valor de la amplitud en el cual se define el umbral del filtrado.

    Parámetros de la función:
    ------------------------
    listaAmplitudes: Lista que contiene las diferentes amplitudes para cada frecuencia.

    Salida de la función:
    ---------------------
    Amplitud mínima a considerar para el filtrado.
    """
    listaAmplitudes.sort(reverse = True)
    razónMáximos = 1
    iContador = 0
    # Se ordena la lista de mayor a menor. Se define una razón entre los máximos igual a 1 y se inicializa un contador.
    while razónMáximos > 0.68:
        razónMáximos = listaAmplitudes [iContador + 1] / listaAmplitudes [iContador]
        iContador +=  1
    # Se compara los 2 mayores valores de la lista, si el cociente entre estos es mayor a 0.68, se suma 1 al contador. 
    else:
        return listaAmplitudes[iContador]
    # Si el cociente es menor se retorna el valor evaluado para ese contador.
    # Esto se realiza para determinar la diferencia que hay entre los valores. Si esta diferencia es muy grande, 
    # la razon entre los valores es menor a 0.68 y se considera ruido, por los valores siguentes serán también ruido.

def Filtrado (arregloFiltrar):
    """
    Toma un arreglo y elimina los valores menores al definido por el umbral. Este arreglo se normaliza, 
    dando a los puntos deseados valores de 1 y a los que se desean eliminar valores de 0.

    Parámetros de la función:
    ------------------------
    arregloFiltrar: Arreglo en el que se encuentran todas las amplitudes para cada frecuencia.

    Salida de la función:
    ---------------------
    Arreglo conformado por 1´s y 0´s, donde los valores iguales a 1 son los que son considerados parte 
    de la señal original.
    """
    valorUmbral = EncontarUmbralFiltrado (arregloFiltrar.tolist())
    # Se determina el valor como umbral utilizando la función EncontrarUmbralFiltrado.
    for iContador in range (0, len (arregloFiltrar)):
        if valorUmbral >= arregloFiltrar [iContador]:
            arregloFiltrar [iContador] = 0
            iContador = iContador + 1
    # Si el valor evaluado es mayo o igual al del umbral se acepta este valor y se cambia por un 1.
        else:
            arregloFiltrar [iContador] = 1
            iContador = iContador + 1
    # En caso que el valor evaluado sea menor al del umbral se considera ruido por lo que se rechaza
    # y se cambia por un 0.

    else:
        return (arregloFiltrar)

# Graficación del estado de las frecuencias
amplitudes = Filtrado(amplitudes)
fig, ax = plt.subplots(dpi=120)
ax.plot(puntosFrecuencia, amplitudes)
ax.set_title('Estado de frecuencias')
ax.set_xlabel('Frecuencia [Hz]')
ax.set_ylabel('Estado')
plt.table (cellText=[['Aceptado',1],['Rechazado', 0]], colWidths=[0.15, 0.07] , loc='upper center')

plt.show()

#=============================================
# Aplicación de la transformada inversa y comparación con la señal original


# Se multiplican los valores de las amplitudes filtradas por la transformada de Fourier.
# Al realizar esto se eliminan los valores de la transformada que son considerados ruido
transformadaSeñalFiltrada = amplitudes * transformadaSeñal

# Se aplica la transformada inversa rápida de Fourier.
transformadaInversaSeñal = ifft (transformadaSeñalFiltrada)

# Graficación de la señal original y la señal ya filtrada.
fig, (ax1, ax2) = plt.subplots(1, 2, dpi=120, sharey= True)
ax1.plot(puntosTiempo[0:50], señalPura[0:50])
ax1.set_title('Señal original')
ax1.set_xlabel('Tiempo')
ax1.set_ylabel('Amplitud')

ax2.plot(puntosTiempo[1:50], transformadaInversaSeñal[1:50])
ax2.set_title('Señal Filtrada')
ax2.set_xlabel('Tiempo')

plt.show()