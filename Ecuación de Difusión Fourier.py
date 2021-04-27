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

def CalculoDifusiónInicial (x, x0, l, A):
    """
    Se realiza el cálculo de la difusión cuando el valor del tiempo es 0 para las posiciones dadas.
    
    Parámetros de la función:
    ------------------------
    x: Posiciones en el eje X.
    x0, l, A: Variables definidas por el usuario y partícipes de la ecuación.
    
    Salida de la función
    ---------------------
    Valor de la difusión inicial para las posiciónes definidas.

    """

    valorD0 = A * np.exp (-(x0 - x) ** 2 / l)

    return valorD0

def CalculoCoeficienteCn (i, lado, x, x0, l, A):
    """
    Se realiza el cálculo del coeficiente de la serie de Fourier.
    
    Parámetros de la función:
    ------------------------
    i= Valor del contador o n para la serie de Fourier.
    x: Posiciones en el eje X.
    lado, x0, l, A: Variables definidas por el usuario y partícipes de la ecuación.
    
    Salida de la función
    ---------------------
    Valor del coeficiente de la serie de fourier para una iteracion n específica..

    """  

    funciónIntegrar = lambda x: 2/lado * CalculoDifusiónInicial (x, x0, l, A) * np.sin (i * np.pi * x / lado)

    coeficienteCn =  integrate.quad (funciónIntegrar, 0, lado) [0]

    return coeficienteCn

def CalculoDifusión (t, x, tamañoLado, númeroTérminos, x0, l, A, D):
    """
    Realiza el cálculo de la ecuación de difusión en una dimensión a través del tiempo por medio del método de Series de Fourier.

    Parámetros de la función:
    ------------------------
    x: Posiciones en el eje X.
    t: Puntos en el tiempo en los que se realizará el cálculo.
    tamañoLado: Tamaño del lado para el eje x.
    númeroTérminos: Número de términos con el que se realizará el cálculo de la ecuación de difusión.
    x0, l, A, D: Variables definidas por el usuario y partícipes de la ecuación.
    
    Salida de la función
    ---------------------
    Valor aproximado de la ecuación de difusión en una dimensión.
    """

    potencialAproximado = 0

    for iContador in range (1, númeroTérminos+1):

        coeficiente = CalculoCoeficienteCn (iContador, tamañoLado, x, x0, l, A)
        potencialAproximado += coeficiente*np.sin(iContador*np.pi*x/tamañoLado)*np.exp(-D*iContador**2*np.pi**2**t/tamañoLado**2)

    return potencialAproximado

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
    r"y la posición por método de Series de Fourier")  
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
    númeroTérminos = barraTérminos.get()
    x0 = barraX0.get()
    l = barral.get()
    A = barraA.get()
    D = barraD.get()

    # Se definen los puntos en los que se va a evaluar la ecuación.
    puntosMalla = 30
    x = np.seterr(over="ignore")
    t = np.linspace (0, puntosTiempo, puntosMalla)
    x = np.linspace (0, tamañoLado, puntosMalla)
    

    T, X = np.meshgrid (t, x)


    # Se realiza el cálculo de la ecuación de difusión unidimensional..
    difusiónFinal = CalculoDifusión(T, X, tamañoLado, númeroTérminos, x0, l, A, D)

    #Graficación de los resultados
    fig = plt.figure ()
    ax = plt.axes (projection = '3d')    
    ax.set_title (r"Ecuación de Difusión unidimensional dependiente del"
    "\n" 
    r"y la posición por método de Series de Fourier")   
    ax.set_xlabel ('t (s)')
    ax.set_ylabel ('x (m)')
    ax.set_zlabel ('ρ (t,x)')
    ax.plot_surface (T, X, difusiónFinal, rstride=1, cstride=1, cmap= 'cividis', edgecolor ='none')

    # Botón que abre la gráfica en una nueva ventana para realizar un mejor análisis.
    boton = Button(ventana, text='Abrir Grafica', command = lambda: AbrirGrafica(T, X, difusiónFinal))
    boton.place (relx=0.5, rely=0.35, anchor=CENTER)


    # Se define el cuadro en la ventana en la cual se colocarán las gráficas.
    canvas = FigureCanvasTkAgg (fig, master = ventana)
    canvas.draw()
    canvas.get_tk_widget().place (relx=0.5, rely=0.615, anchor=CENTER)
    

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
barraTérminos = Scale(ventana, from_=2, to=50, tickinterval=0.48,length=400, bg = 'White',
resolution=1, showvalue=True, orient='horizontal', label="Número de Términos", cursor = "hand1")
barraTérminos.bind ("<ButtonRelease-1>",Graficar)
barraTérminos.set(10)

barraTérminos.place (relx=0.825, rely=0.05, anchor=CENTER)

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
ventana.title ("Cálculo de la ecuación de difusión en una dimensión por Series de Fourier.")
ventana.mainloop()