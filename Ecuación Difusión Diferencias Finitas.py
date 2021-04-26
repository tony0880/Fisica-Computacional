# Se importa las bibliotecas necesarias.
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk, Scale, CENTER, Button, StringVar, Label
from scipy import integrate

# Se definen las variables para la ventana de interfaz.
ventana = Tk ()
ventana.minsize (1295,1000)
ventana.config (bg='White')

def CalculoDifusiónInicialTiempo (matrizDifusiónInicial, puntosMalla, x, A, x0, l):
    """
    Se realiza el cálculo de la difusión cuando el valor del tiempo es 0 para las posiciones dadas.
    
    Parámetros de la función:
    ------------------------
    x: Posiciones en el eje X.
    x0, l, A: Constantes definidas por el usuario y partícipes de la ecuación.
    
    Salida de la función
    ---------------------
    Valor de la difusión inicial para las posiciónes definidas.

    """
    for i in range (0, puntosMalla):
        matrizDifusiónInicial [i][0] = A * np. exp (-(x[i] - x0) ** 2 / l)
    else:
        return matrizDifusiónInicial


def CalculoDifusión (matrizDifusión, presición, puntosMalla, tamañoLado, puntosTiempo, D):
    """
    Se realiza el cálculo de la ecuación de difusión unidimensional por medio del método de diferencias finitas
    
    Parámetros de la función:
    ------------------------
    matrizDifusión: Matriz que contiene los valores de la ecuación para el tiempo y la posición. Estos valores cambian con cada iteración.
    presición: Presición deseada por el usuario para el cálculo.
    puntosMalla: Cantidad de puntos que existen para cada eje (Tiempo y posición).
    tamañoLado: Valor que tiene todo el recorrido posicional de la ecuación.
    puntosTiempo: Tiempo total en la que se realiza el cálculo
    D: Constante definida por el usuario y partícipe de la ecuación.
    
    Salida de la función
    ---------------------
    Matriz con los valores de la ecuación de difusión para un tiempo y posición.

    """
    contadorIteraciones = 0
    cantidadImprecisiones = 1
    # Se define un contador de iteraciones para registrar la cantidad necesaria para el cálculo. A su vez, se define una variable cantidad Impresiones, que registra 
    # la cantidad de veces que no se cumple la presición deseada en la matriz.
    while cantidadImprecisiones > 0:
        contadorIteraciones += 1
        cantidadImprecisiones = 0
        # Se suma uno al contador de iteraciones y se reinicia el conteo de impresiciones.
    
        for contadorPosición in range (1, puntosMalla - 1):
            for contadorTiempo in range (0, puntosMalla - 2):
        # Por forma de la ecuación a calcular se establece que el contador de posiciones debe iniciar en el segundo valor mientras que el de tiempo en el primer valor.
        # Esto debido a que se cuenta únicamente con los valores inciales del tiempo por lo que se recomienda empezar por el primer valor del tiempo y calcular el 
        # tiempo siguiente.
                difusiónAnterior = matrizDifusión [contadorPosición][contadorTiempo+1]
                gamma = D*puntosTiempo/puntosMalla*(puntosMalla/tamañoLado)**2
                matrizDifusión[contadorPosición][contadorTiempo+1] = matrizDifusión [contadorPosición][contadorTiempo] + \
                gamma * (matrizDifusión[contadorPosición+1][contadorTiempo]+matrizDifusión[contadorPosición-1][contadorTiempo]-2*matrizDifusión [contadorPosición][contadorTiempo])
                diferenciaDifusión = np.abs(difusiónAnterior - matrizDifusión[contadorPosición][contadorTiempo+1])                
                if diferenciaDifusión > presición:
                    cantidadImprecisiones += 1
                if contadorIteraciones > 500:
                    cantidadImprecisiones = 0
                # Se define que si la diferencia entre el valor actual para una casilla y el valor anterior mayor a la presición se le añade 1 al contador de imprecisiones.
                # A su vez si las iteraciones son mayores a 500, se da como resultado el último valor de la ecuación.
    return matrizDifusión, contadorIteraciones


def AbrirGrafica (T, X, Difusión):
    """
    Se abre una ventana nueva que muestra la gráfica. Esto al ser la ventana dada por la biblioteca matplotlib, la gráfica se puede rotar y acercar para un mejor análisis,
    así como guardarla.
    
    Parámetros de la función:
    ------------------------
    T, X, Difusión: Variables para la graficación de la ecuación
    
    Salida de la función
    ---------------------
    Ventana que muestra la gráfica calculada.

    """
    fig = plt.figure ()
    ax = plt.axes (projection = '3d')    
    ax.set_title (r"Ecuación de Difusión unidimensional dependiente del"
    "\n" 
    r"tiempo y la posición por método de Diferencias Finitas")  
    ax.set_xlabel ('t (s)')
    ax.set_ylabel ('x (m)')
    ax.set_zlabel ('ρ (t,x)')
    ax.plot_surface (T, X, Difusión, rstride=1, cstride=1, cmap= 'cividis', edgecolor ='none')
    plt.get_current_fig_manager().window.showMaximized ()
    animation.FuncAnimation (fig, Graficar, interval = 1000)
    plt.show()
                  

def Graficar (i):
    """
    Realiza la graficación de los datos brindados.

    Parámetros de la función:
    ------------------------
    i: valor cualesquiera para la ejecución del programa. Este parámetro no tiene incidencia en el resultado.
    
    Salida de la función
    ---------------------
    Gráficas de la ecuación de difusión con respecto a la posición y al tiempo.
    """

    # Obtiene los valores dados por el slider en la ventana.
    tamañoLado = barraL.get()
    puntosTiempo = barraTiempos.get()
    presición = barraPresición.get()
    x0 = barraX0.get()
    l = barral.get()
    A = barraA.get()
    D = barraD.get()

    # Se definen los puntos en los que se va a evaluar la ecuación.
    puntosMalla = 30

    t = np.linspace (0, puntosTiempo, puntosMalla)
    x = np.linspace (0, tamañoLado, puntosMalla)
    

    T, X = np.meshgrid (t,x)

    # Se crea una matriz del tamaño antes definido, con valores únicamente de 0.
    matrizDifusiónInicial = np.zeros ((puntosMalla, puntosMalla))

    # Se modifican los valores para el tiempo inicial.
    matrizDifusiónInicial = CalculoDifusiónInicialTiempo (matrizDifusiónInicial, puntosMalla, x, A, x0, l)
    

    # Se realiza el cálculo del potencial.
    resultadoFinal = CalculoDifusión (matrizDifusiónInicial, presición, puntosMalla, tamañoLado, puntosTiempo, D) 
    
    # Se definen las variables que contienen los resultados de la difusión y la cantidad de iteraciones.
    difusiónFinal =  resultadoFinal [0]
    iteracionesTotales = resultadoFinal [1]
    
    # Graficación de los resultados.
    fig = plt.figure ()
    ax = plt.axes (projection = '3d') 
    ax.set_title (r"Ecuación de Difusión unidimensional dependiente del"
    "\n" 
    r"tiempo y la posición por método de Diferencias Finitas")   
    ax.set_xlabel ('t (s)')
    ax.set_ylabel ('x (m)')
    ax.set_zlabel ('ρ (t,x)')
    ax.plot_surface (T, X, difusiónFinal  , rstride=1, cstride=1, cmap= 'cividis')
 
    
    # Se define el cuadro en la ventana en la cual se colocarán las gráficas.
    canvas = FigureCanvasTkAgg (fig, master = ventana)
    canvas.get_tk_widget().config (bg = 'white')
    canvas.draw()
    canvas.get_tk_widget().place (relx=0.5, rely=0.6, anchor=CENTER)

    # Botón que abre la gráfica en una nueva ventana para realizar un mejor análisis.
    boton = Button(ventana, text='Abrir Grafica', command = lambda: AbrirGrafica(T, X, difusiónFinal), cursor = 'hand1')
    boton.place (relx=0.5, rely=0.32, anchor=CENTER)

    # Etiqueta que contiene la cantidad de iteraciones realizadas para el cálculo.
    etiqueta = Label (ventana, text = ('Iteraciones necesarias: ' + str (iteracionesTotales)))
    etiqueta.config (bg = 'white', font = ('Verdana', 15))
    etiqueta.place (relx=0.5, rely=0.37, anchor=CENTER)

    #Función que permite graficar a tiempo real. Esta ejecuta nuevamente la función Graficar para realizar nuevamente el cálculo.
    animation.FuncAnimation (fig, Graficar, interval = 1000)
    plt.close ()
 

# Se define el slider para el tamaño del lado.
barraL = Scale(ventana, from_=7, to=20, tickinterval=13, length=400, bg = 'White',
resolution=1, showvalue=True, orient='horizontal', label="Tamaño del Lado (Lx)", cursor = "hand1")
barraL.bind ("<ButtonRelease-1>",Graficar)
barraL.set(10)

barraL.place (relx=0.175, rely=0.05, anchor=CENTER)

# Se define el slider para el tiempo a evaluar.
barraTiempos = Scale(ventana, from_=1, to=5, tickinterval=4,length=400, bg = 'White',
resolution=0.5, showvalue=True, orient='horizontal', label="Tiempo (s)", cursor = "hand1")
barraTiempos.bind ("<ButtonRelease-1>",Graficar)
barraTiempos.set(3)

barraTiempos.place (relx=0.5, rely=0.05, anchor=CENTER)

# Se define el slider para el número de términos.
barraPresición = Scale(ventana, from_=0.001, to=1, tickinterval=0.999,length=400, bg = 'White',
resolution=0.001, showvalue=True, orient='horizontal', label="Presición", cursor = "hand1")
barraPresición.bind ("<ButtonRelease-1>",Graficar)
barraPresición.set(0.05
)

barraPresición.place (relx=0.825, rely=0.05, anchor=CENTER)

# Se define el slider para la variable X0.
barraX0 = Scale(ventana, from_=2, to=6, tickinterval=4,length=400, bg = 'White',
resolution=1, showvalue=True, orient='horizontal', label="x0", cursor = "hand1")
barraX0.bind ("<ButtonRelease-1>",Graficar)
barraX0.set(5)

barraX0.place (relx=0.175, rely=0.15, anchor=CENTER)

# Se define el slider para la variable l.
barral = Scale(ventana, from_=0.5, to=3, tickinterval=2.5,length=400, bg = 'White',
resolution=0.25, showvalue=True, orient='horizontal', label="l", cursor = "hand1")
barral.bind ("<ButtonRelease-1>",Graficar)
barral.set(1.5)

barral.place (relx=0.5, rely=0.15, anchor=CENTER)

# Se define el slider para la variable A.
barraA = Scale(ventana, from_=1, to=4, tickinterval=3,length=400, bg = 'White',
resolution=0.5, showvalue=True, orient='horizontal', label="A", cursor = "hand1")
barraA.bind ("<ButtonRelease-1>",Graficar)
barraA.set(2)

barraA.place (relx=0.825, rely=0.15, anchor=CENTER)

# Se define el slider para la variable D.
barraD = Scale(ventana, from_=0.05, to=1, tickinterval=0.95,length=400, bg = 'White',
resolution=0.05, showvalue=True, orient='horizontal', label="D", cursor = "hand1")
barraD.bind ("<ButtonRelease-1>",Graficar)
barraD.set(0.5)

barraD.place (relx=0.5, rely=0.25, anchor=CENTER)

# Para cada slider se realiza un "bindeo" para que el cálculo se realice hasta que el botón del mouse se suelte.
# Esto debido a que sino el programa responde muy lento pues para cada moviento del slider se realiza un cálculo.
# A su vez para cada slider se le establece una posición inicial, de acuerdo a los valores brindados para la 
# realización del problema.


# Se ejecuta la graficación con los valores ya establecidos para el problema. 
Graficar (0)


# Se configura el título de la ventana y se ejecuta.
ventana.title ("Cálculo de la ecuación de difusión en una dimensión por diferencias finitas.")
ventana.mainloop()
