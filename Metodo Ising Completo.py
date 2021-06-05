# Importación de bibliotecas necesarias.
import random
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Scale, CENTER, Button, Label


# Constantes inciales para la simulación.
constanteBoltzman = 1
numeroEspines = 100
pasos  = 1000
J = 1


def OrientaciónEspin (numeroEspines, orientacion):
    """
    Crea una lista con una orientación definida para un número específico de spines.

    Parámetros de la función:
    ------------------------
    numeroEspines: Cantidad de espines presentes en el cálculo. 
    orientacion: Define la orientación inicial de los spines. Si esta es igual a 1 todos van para arriba, si es -1 van para abajo y si es cualquier otro
    valor se define una orientación aleatoria para cada uno de los spines.

    Salida de la función
    ---------------------
    Lista con valores de 1 o -1 correspondiente a la orientación de los spines.
    """

    if orientacion == 1:
        listaEspines = np.ones (numeroEspines)
    elif orientacion == -1:
        listaEspines = []
        for i in range (numeroEspines):  
            listaEspines.append (-1)
    else:
        listaEspines = []
        for i in range (numeroEspines):  
            orientación = random.randint (0,1)
            if orientación == 0:
                listaEspines.append (1)
            else:
                listaEspines.append (-1)
    
    return listaEspines


def CalculoEnergia (listaEspines):
    """
    Función que calcula el valor de la energía de los spines contenidos en una lista.

    Parámetros de la función:
    ------------------------
    listaEspines: Lista con los valores de la orientación de los spines a analizar.

    Salida de la función
    ---------------------
    Valor de la energía para todo un conjunto de spines.
    """

    energia = 0
    for i in range (numeroEspines-1):
        energia += -J * listaEspines[i] * listaEspines[i+1]    
    
    return energia


def CalculoMagnetizacion (listaEspines):
    """
    Función que calcula el valor de la magnetización de los spines contenidos en una lista.

    Parámetros de la función:
    ------------------------
    listaEspines: Lista con los valores de la orientación de los spines a analizar.

    Salida de la función
    ---------------------
    Valor de la magnetización para todo un conjunto de spines.
    """

    magnetizacion = 0
    for i in range (numeroEspines):
        magnetizacion += listaEspines[i]
    
    return magnetizacion    


def VariacionEspin (listaEspines,temperatura):
    """
    Función terciaria que se encarga de realizar los cálculos de energía y magnetización para una lista de spines, para luego modificar un spin aleatorio
    de dicha lista y valorar la probabilidad con la que este cambio sea aceptado.

    Parámetros de la función:
    ------------------------
    listaEspines: Lista con los valores de la orientación de los spines a analizar.
    temperatura: Valor de temperatura con los que se realizará el cálculo. Este parámetro influira en el grado de aceptación del cambio.

    Salida de la función
    ---------------------
    Energía de la lista de spines final, la cual depende de si se da la aceptación o no.
    Magnetización de la lista de spines final, la cual depende de si se da la aceptación o no.
    Lista de spines final, la cual depende de si se da la aceptación o no.
    """

    # Se calcula la enería y magnetización de la lista original de spines.
    energia = CalculoEnergia (listaEspines)
    magnetizacion = CalculoMagnetizacion (listaEspines)

    # Se escoge un spin aleatorio.
    espinAleatorio = random.randint (0, numeroEspines-1)

    # Se modifica la lista de spines con base al spin escogido aleatoriamente.
    listaEspines [espinAleatorio] = listaEspines [espinAleatorio] * -1
    
    # Se realiza el cálculo de energía y magnetización para la lista de spines actualizada.
    nuevaEnergia = CalculoEnergia (listaEspines)
    nuevaMagnetizacion = CalculoMagnetizacion (listaEspines)
    cambioEnergia = nuevaEnergia - energia

    # Si se cumple que la nueva energía es mayor a la original, se define una probabilidad de aceptación.
    # Si un valor aleatorio está dentro de esta probabilidad se acepta la nueva orientación del spin y su energía.
    if nuevaEnergia > energia:
        probabilidad = np.exp (-cambioEnergia/(constanteBoltzman*temperatura))
        if random.random () < probabilidad:   
            energia = nuevaEnergia
            magnetizacion = nuevaMagnetizacion
                
        else:
            listaEspines [espinAleatorio] = listaEspines [espinAleatorio] * -1

    # En caso contrario siempre se acepta la nueva energía.
    else: 
        energia = nuevaEnergia
        magnetizacion = nuevaMagnetizacion

    return energia, listaEspines, magnetizacion   


def MetodoIsing (valorTemp, orientacion):    
    """
    Función secundaria que se encarga de definir la lista original de spines con base a su orientación. Además ejecuta la función VariacionEspin
    una serie de veces para que la energía, la magnetización y los espines evolucionen con el tiempo.
    Finalmente al alcanzar un número de pasos predeterminados, con base al equilibrio del sistema, calcula la energía interna y la energía interna
    al cuadrado del sistema.

    Parámetros de la función:
    ------------------------
    valorTemp: valor de temperatura con los que se realizará el cálculo.
    orientacion: Define la orientación inicial de los spines.

    Salida de la función
    ---------------------
    Evolución de los spines a través del tiempo.
    Evolución de la energía a través del tiempo.
    Evolución de la magnetización a través del tiempo.
    Evolución de la energía interna a través del tiempo.
    Evolución de la energía interna al cuadrado a través del tiempo.
    """

    # Se obtiene los valores inciales de los espines de manera aleatoria.
    listaEspines = OrientaciónEspin (numeroEspines, orientacion)

    # Se define un valor arbitrario para el punto de equilibrio.
    puntoEquilibrio = 200

    # Se incializan los arreglos que contienen la evolución de la energía, magnetización, energía interna y energía interna al cuadrado.
    evolucionEnergia = np.zeros (pasos)
    evolucionMagnetizacion = np.zeros (pasos)
    evolucionEnergiaInterna =  np.zeros (pasos - puntoEquilibrio)
    evolucionEnergiaInternaCuadrado = np.zeros (pasos - puntoEquilibrio)

    # Se calculan los valores iniciales para la energía, magnetización y los spines.
    resultadoInicial = VariacionEspin(listaEspines, valorTemp)
    evolucionEnergia[0] = resultadoInicial[0]
    evolucionMagnetizacion[0] = resultadoInicial [2] 
    evolucionEspines = [listaEspines]
    
    for i in range (1, pasos):  
        # Al alcanzar un valor predeterminado se incia el cálculo de la energía interna y energía interna al cuadrado. De lo contrario se manejan
        # solamente las originales.
        if i >= puntoEquilibrio:
            resultado = VariacionEspin(listaEspines,valorTemp)    
            listaEspines =  resultado[1]  
            evolucionEnergia[i] = resultado[0]
            evolucionMagnetizacion[i] = resultado[2]
            evolucionEnergiaInterna [i-puntoEquilibrio] = resultado [0]
            evolucionEnergiaInternaCuadrado [i-puntoEquilibrio] = resultado [0] **2
            evolucionEspines.append (np.array(listaEspines)) 
        else:
            resultado = VariacionEspin(listaEspines,valorTemp)    
            listaEspines =  resultado[1]  
            evolucionEnergia[i] = resultado[0]
            evolucionMagnetizacion[i] = resultado[2]
            evolucionEspines.append (np.array(listaEspines)) 

    evolucionEspines =  np.array(evolucionEspines)

    return evolucionEspines, evolucionEnergia, evolucionMagnetizacion, evolucionEnergiaInterna, evolucionEnergiaInternaCuadrado


def Promedio (conjunto, númeroIntentos, cantidadPasos):
    """
    Función que calcula el promedio para un conjunto que repitió su cálculo una serie de veces.

    Parámetros de la función:
    ------------------------
    conjunto: Arreglo que contiene una variable en función de una serie de pasos a través del tiempo repetida una número definido de veces.
    númeroIntentos: Cantidad de veces que se repitió el cálculo.
    cantidadPasos: Cantidad de pasos a través del tiempo que ocupó el cálculo.

    Salida de la función
    ---------------------
    Arreglo con los valores promedio de un conjunto con base a las repeticiones.
    """

    arregloPromedios = np.zeros (cantidadPasos)
    # Al tenerse una lista que contiene variables con base a los pasos dados y esto repetido una serie de veces. Se analizará primero un paso en específico,
    # para luego ir variando con base a las repeticiones. Una vez cumplidas todos los intentos se pasara al siguiente paso en el tiempo.
    # Cada intento para cada paso se promediará para obtener un arreglo de promedios de una variable en función de los pasos a través del tiempo.

    for numeroPaso in range (cantidadPasos):
        sumatoria = 0
        for intento in range (númeroIntentos):
            sumatoria += conjunto [intento][numeroPaso]
        arregloPromedios [numeroPaso] = sumatoria / len (conjunto)
    return arregloPromedios


def CalculoCalorEspecifico (arregloEnergia, arregloEnergioCuadrado, arregloTemperatura):
    """
    Función que calcula calor específico para un sistema.

    Parámetros de la función:
    ------------------------
    arregloEnergía: Arreglo con los valores de la energía interna del sistema en equilibrio.
    arregloEnergíaCuadrado: Arreglo con los valores de la energía interna al cuadrado del sistema en equilibrio.
    arregloTemperatura: Arreglo con los valores de la temperatura en las que se analiza el sistema.

    Salida de la función
    ---------------------
    Arreglo con los valores del calor específico en función de la temperatura.
    """

    cantidadTemps = len (arregloTemperatura)
    arregloCalorEspecifico = []
    for i in range (cantidadTemps):
        calorEspecifico  = 1 / (numeroEspines)**2 * (arregloEnergioCuadrado[i] - arregloEnergia[i]**2)/arregloTemperatura[i]**2
        arregloCalorEspecifico.append (calorEspecifico)
    arregloCalorEspecifico = np.array (arregloCalorEspecifico)
    return arregloCalorEspecifico


def EjecutarUnaTemperatura (orientacion, temperatura):
    """
    Una de las funciones principales que realiza los cálculos de energía y magnetización promedio para un sistema en una sola temperatura.

    Parámetros de la función:
    ------------------------
    orientacion: Define la orientación inicial de los spines.
    temperatura: valor de temperatura con los que se realizará el cálculo.
    
    Salida de la función
    ---------------------
    Gráficas de evolución de los spines, la energía y la magnetización a través del tiempo para una sola temperatura.
    """

    repeticionCalculo = 50
    conjuntoEnergia = []
    conjuntoMagnetizacion = []

    # Condición que repite el cálculo una serie de veces definidas.
    for i in range (repeticionCalculo):
        resultado = MetodoIsing (temperatura, orientacion)
        conjuntoEnergia.append (resultado [1])
        conjuntoMagnetizacion.append (resultado [2])


    conjuntoEnergia = np.array (conjuntoEnergia)
    conjuntoMagnetizacion = np.array (conjuntoMagnetizacion)
    
    #Graficación de los spines a través del tiempo.

    evolucionEspines = resultado [0]

    fig, ax = plt.subplots(figsize = (10,10), dpi = 120)
    ax.imshow(evolucionEspines.T, 'plasma')
    ax.set_title("Evolución de los spines de un sistema a través del tiempo por"
        "\n" 
        r"medio del Método de Ising de 1-D para un kT de " + str(temperatura) )
    ax.set_xlabel('Pasos')
    ax.set_ylabel('Espines')
    
    ax.set_aspect('5')
    

    #Graficación de la energía a través del tiempo.

    #Se promedian los valores para las energías con base a una serie de repeticiones.
    evolucionEnergia = Promedio (conjuntoEnergia, repeticionCalculo, pasos)

    fig, ax = plt.subplots (dpi = 120)
    ax.plot (evolucionEnergia)
    ax.set_title("Evolución de la energía de un sistema a través del tiempo por"
        "\n" 
        r"medio del Método de Ising de 1-D para un kT de " + str(temperatura) )
    ax.set_xlabel('Pasos')
    ax.set_ylabel('Energia')  


    #Graficación de la magnetización a través del tiempo.

    #Se promedian los valores para las magnetizaciones con base a una serie de repeticiones.
    evolucionMagnetizacion = Promedio (conjuntoMagnetizacion, repeticionCalculo, pasos)

    fig, ax = plt.subplots (dpi = 120)
    ax.plot (evolucionMagnetizacion)
    ax.set_title ("Evolución de la magnetización de un sistema a través del tiempo por"
        "\n" 
        r"medio del Método de Ising de 1-D para un kT de " + str(temperatura) )
    ax.set_xlabel('Pasos')
    ax.set_ylabel('Magnetizacion')    
    
    plt.show()



def EjecutarVariasTemperaturas (orientacion):
    """
    Una de las funciones principales que realiza los cálculos de energía, magnetización, energía interna y energía interna al cuadrado promedio 
    para un sistema en una serie de temperaturas.

    Parámetros de la función:
    ------------------------
    orientacion: Define la orientación inicial de los spines.
    
    Salida de la función
    ---------------------
    Gráficas de evolución de la energía interna, la magnetización y el calor específico en función de la temperatura.
    """

    repeticionCalculo = 25
    cantidadTemperaturas = 100
    conjuntoEnergia = []
    conjuntoMagnetizacion = []
    conjuntoEnergiaInterna = []    
    conjuntoEnergiaInternaCuadrado = []    

    # Condición que repite el cálculo una serie de veces definidas.
    for i in range (repeticionCalculo):
        valoresTemp = np.linspace (0.1, 5, cantidadTemperaturas)
        listaEnergiaPromedio = []
        listaMagnetizaciónPromedio = []
        listaEnergiaInternaPromedio = []
        listaEnergiaInternaCuadradoPromedio = []
        
        # Condición que realiza los cálculos en una serie de temperaturas.
        for iTemperatura in valoresTemp:

            #Se realiza el cálculo para cada temperatura y se almacena en una lista. 
            resultadoMetodo = MetodoIsing(iTemperatura, orientacion)
            energiaPorCorrida = resultadoMetodo[1]
            magnetizacionPorCorrida = resultadoMetodo [2]
            energiaInternaPorCorrida = resultadoMetodo [3]
            energiaInternaCuadradoPorCorrida = resultadoMetodo [4]

            # Se promedian cada uno de los valores para cada una de las temperaturas y se agregan a una nueva lista con los valores promedios únicamente.
            promedioEnergia = np.sum (energiaPorCorrida)/len(energiaPorCorrida)
            promedioMagnetizacion = np.sum (magnetizacionPorCorrida)/len(magnetizacionPorCorrida)
            promedioEnergiaInterna = np.sum (energiaInternaPorCorrida)/len(energiaInternaPorCorrida)
            promedioEnergiaInternaCuadrado = np.sum (energiaInternaCuadradoPorCorrida)/len(energiaInternaCuadradoPorCorrida)

            listaEnergiaPromedio.append (promedioEnergia)
            listaMagnetizaciónPromedio.append (promedioMagnetizacion)
            listaEnergiaInternaPromedio.append (promedioEnergiaInterna)
            listaEnergiaInternaCuadradoPromedio.append (promedioEnergiaInternaCuadrado)

        # Una vez se analiza el sistema para todas las temperaturas, se guarda la información en una nueva lista y se vuelven a realiza los cálculos desde 0.
        conjuntoEnergia.append (listaEnergiaPromedio)
        conjuntoMagnetizacion.append (listaMagnetizaciónPromedio)
        conjuntoEnergiaInterna.append (listaEnergiaInternaPromedio)
        conjuntoEnergiaInternaCuadrado.append (listaEnergiaInternaCuadradoPromedio)

    conjuntoEnergia = np.array (conjuntoEnergia)
    conjuntoMagnetizacion = np.array (conjuntoMagnetizacion)
    conjuntoEnergiaInterna = np.array (conjuntoEnergiaInterna)
    conjuntoEnergiaInternaCuadrado = np.array (conjuntoEnergiaInternaCuadrado)

    # Se pomedia los valores de la energía interna y energía intera al cuadrado con base a una serie de repeticiones.
    evolucionEnergiaInterna = Promedio (conjuntoEnergiaInterna, repeticionCalculo, cantidadTemperaturas)
    evolucionEnergiaInternaCuadrado = Promedio (conjuntoEnergiaInternaCuadrado, repeticionCalculo, cantidadTemperaturas)

    # Cálculo de la energía interna en función del kT de manera analítica.
    listaUAnalítica = []
    for kTemperatura in valoresTemp:
        uAnalitica = -100 * J * np.tanh (J/kTemperatura)
        listaUAnalítica.append (uAnalitica)

    # Graficación de la energía simulada y analítica en función del kT.
    fig, ax1 = plt.subplots()

    color = "tab:green"
    ax1.set_title("Energía vs kT"
    "\n" 
    r"Método de Ising Simulado")
    ax1.set_xlabel('kT')
    ax1.set_ylabel('Energía Simulada', color = color)
    ax1.plot(valoresTemp, evolucionEnergiaInterna, color = color)
    ax1.tick_params(axis="y", labelcolor= color)
   
    ax2 = ax1.twinx() 
    color = "tab:blue"
    ax2.set_ylabel('Energía Analítica', color = color)
    ax2.plot(valoresTemp, listaUAnalítica, color = color)
    ax2.tick_params(axis="y", labelcolor= color)

    fig.tight_layout ()
    


    # Cálculo de la magnetización en función del kT de manera analítica.
    listaMAnalítica = []

    # Para la simulación se utiliza un campo magnético igual a 0, para el cálculo analítico no es posible debido a que es necesario este valor, por lo que se
    # escoge un valor pequeño arbitario para su cálculo, que varía con respecto a la orientación incial de los spines.
    B = orientacion * 0.2
    for nTemperatura in valoresTemp:
        mAnalitica = 100 * np.exp (J/nTemperatura) * np.sinh (B/nTemperatura) / np.sqrt (np.exp (2*J/nTemperatura)*(np.sinh (B/nTemperatura))**2+np.exp (-2*J/nTemperatura))
        listaMAnalítica.append (mAnalitica)

    # Se promedian los valores para las magnetizaciones con base a una serie de repeticiones.
    evolucionMagnetizacion = Promedio (conjuntoMagnetizacion, repeticionCalculo, cantidadTemperaturas)

    # Graficación de la magnetización simulada y analítica en función del kT.

    fig, ax3 = plt.subplots()

    color = "tab:green"
    ax3.set_title("Magnetización vs kT"
        "\n" 
        r"Método de Ising Simulado ")
    ax3.set_xlabel('kT')
    ax3.set_ylabel('Magnetización', color = color)
    ax3.plot(valoresTemp, evolucionMagnetizacion, color = color)
    ax3.tick_params(axis="y", labelcolor= color)
     
    ax4 = ax3.twinx() 
    color = "tab:blue"
    ax4.set_ylabel('Magnetización Analítica', color = color)
    ax4.plot(valoresTemp, listaMAnalítica, color = color)
    ax4.tick_params(axis="y", labelcolor= color)

    fig.tight_layout ()


    # Cálculo de la magnetización en función del kT de manera analítica.
    listaCAnalítica = []
    for jTemperatura in valoresTemp:
        cAnalitica = (J/jTemperatura)**2 / (np.cosh(J/jTemperatura))**2
        listaCAnalítica.append (cAnalitica)

    # Se realiza el cálculo del calor específico del sistema en equilibrio.
    conjuntoCalorEespecifico = CalculoCalorEspecifico (evolucionEnergiaInterna, evolucionEnergiaInternaCuadrado, valoresTemp)

    # Graficación del calor específico simulado y analítico en función del kT.
    fig, ax5 = plt.subplots()

    color = "tab:green"
    ax5.set_title("Calor específico vs kT"
        "\n" 
        r"Método de Ising Simulado ")
    ax5.set_xlabel('kT')
    ax5.set_ylabel('Calor específico', color = color)
    ax5.plot(valoresTemp, conjuntoCalorEespecifico, color = color)
    ax5.tick_params(axis="y", labelcolor= color)
     
    ax6 = ax5.twinx() 
    color = "tab:blue"
    ax6.set_ylabel('Calor específico Analítico', color = color)
    ax6.plot(valoresTemp, listaCAnalítica, color = color)
    ax6.tick_params(axis="y", labelcolor= color)

    fig.tight_layout ()


    plt.show()


####################################################################################################################################################################################
# Sección de interfaz de usuario.


def Ventana1Temp (ventana):
    """
        Ventana en la que el usuario elige la orientación de los spines y la temperatura específica con la que realizar la simulación.

        Parámetros de la función:
        ------------------------
        ventana: Variable que cierra una ventana ya abierta.
        
        Salida de la función
        ---------------------
        Interfaz gráfica con la que el usuario define los parámetros de la simulación.
        """
        
    # Función para cerrar una ventana definida.
    ventana.destroy ()

    # Parametros iniciales para la ventana gráfica.
    ventana1 = Tk ()
    ventana1.minsize (800, 750)
    ventana1.config (bg='White')

    # Etiquetas que indican al usuario lo que debe seleccionar.
    etiqueta1 = Label (ventana1, text = ('Seleccione la temperatura '
    "\n" 
        r"a analizar" ))
    etiqueta1.config (bg = 'white', font = ('Verdana', 15))
    etiqueta1.place (relx=0.5, rely=0.2, anchor=CENTER)

    etiqueta2 = Label (ventana1, text = ('Seleccione la orientación '
    "\n" 
        r"inicial de los Spines" ))
    etiqueta2.config (bg = 'white', font = ('Verdana', 15))
    etiqueta2.place (relx=0.5, rely=0.45, anchor=CENTER)

    # Se define el slider para la temperatura con la que realizar los cálculos.
    barraTemp = Scale(ventana1, from_=0.1, to=5, tickinterval=4.9, length=400, bg = 'White',
    resolution=0.1, showvalue=True, orient='horizontal', label="Temperatura", cursor = "hand1")
    barraTemp.set(1)
    barraTemp.place (relx=0.5, rely=0.325, anchor=CENTER)

    # Obtiene los valores dados por el slider en la ventana.
    temperatura = barraTemp.get()

    # Se definen los diferentes botones.
    botonArriba = Button(ventana1, text='Hacia arriba', command = lambda: EjecutarUnaTemperatura(1, temperatura), cursor = 'hand1')
    botonArriba.place (relx=0.25, rely=0.575, anchor=CENTER)

    botonAbajo = Button(ventana1, text='Hacia abajo', command = lambda: EjecutarUnaTemperatura(-1, temperatura), cursor = 'hand1')
    botonAbajo.place (relx=0.5, rely=0.575, anchor=CENTER)

    botonAleatorio = Button(ventana1, text='Spines aleatorios', command = lambda: EjecutarUnaTemperatura(0, temperatura), cursor = 'hand1')
    botonAleatorio.place (relx=0.75, rely=0.575, anchor=CENTER)

    botonRegresar = Button(ventana1, text='Regresar', command = lambda: VentanaPrincipal(ventana1), cursor = 'hand1')
    botonRegresar.place (relx=0.775, rely=0.85, anchor=CENTER)

    # Se configura el título de la ventana y se ejecuta.
    ventana1.title ("Cálculo de R para un Sistema Estocástico con base a una sola temperatura")
    ventana1.mainloop()


def VentanaVariasTemp (ventana):
    """
        Ventana en la que el usuario elige la orientación de los spines con la que realizar la simulación.

        Parámetros de la función:
        ------------------------
        ventana: Variable que cierra una ventana ya abierta.
        
        Salida de la función
        ---------------------
        Interfaz gráfica con la que el usuario define los parámetros de la simulación.
        """

    # Función para cerrar una ventana definida.
    ventana.destroy ()

    # Parametros iniciales para la ventana gráfica.
    ventana2 = Tk ()
    ventana2.minsize (800, 750)
    ventana2.config (bg='White')

    # Etiqueta que indica al usuario lo que debe seleccionar.
    etiqueta = Label (ventana2, text = ('Seleccione la orientación '
    "\n" 
        r"inicial de los Spines" ))
    etiqueta.config (bg = 'white', font = ('Verdana', 22))
    etiqueta.place (relx=0.5, rely=0.275, anchor=CENTER)

    # Se definen los diferentes botones.
    botonArriba = Button(ventana2, text='Hacia arriba', command = lambda: EjecutarVariasTemperaturas (1), cursor = 'hand1')
    botonArriba.place (relx=0.25, rely=0.5, anchor=CENTER)

    botonAbajo = Button(ventana2, text='Hacia abajo', command = lambda: EjecutarVariasTemperaturas (-1), cursor = 'hand1')
    botonAbajo.place (relx=0.5, rely=0.5, anchor=CENTER)

    botonAleatorio = Button(ventana2, text='Spines aleatorios', command = lambda: EjecutarVariasTemperaturas (0), cursor = 'hand1')
    botonAleatorio.place (relx=0.75, rely=0.5, anchor=CENTER)

    botonRegresar = Button(ventana2, text='Regresar', command = lambda: VentanaPrincipal(ventana2), cursor = 'hand1')
    botonRegresar.place (relx=0.775, rely=0.85, anchor=CENTER)

    # Se configura el título de la ventana y se ejecuta.
    ventana2.title ("Cálculo de R para un Sistema Estocástico con base a varias temperaturas")
    ventana2.mainloop()


def VentanaPrincipal (ventana):
    """
        Ventana en la que el usuario elige si desea realizar la simulación para una sola temperatura o para una serie de ellas.

        Parámetros de la función:
        ------------------------
        ventana: Variable que cierra una ventana ya abierta.
        
        Salida de la función
        ---------------------
        Interfaz gráfica con la que el usuario define los parámetros de la simulación.
        """

    # Función para cerrar una ventana definida.
    ventana.destroy ()

    # Parametros iniciales para la ventana gráfica.
    ventana = Tk ()
    ventana.minsize (800, 750)
    ventana.config (bg='White')

    # Etiqueta que indica al usuario lo que debe seleccionar.
    etiqueta = Label (ventana, text = ('Seleccione si desea realizar el cálculo para '
    "\n" 
        r"una temperatura o para una serie" ))
    etiqueta.config (bg = 'white', font = ('Verdana', 22))
    etiqueta.place (relx=0.5, rely=0.275, anchor=CENTER)

    # Se definen los diferentes botones.
    boton1Temp = Button(ventana, text='Ejecutar para una Temperatura', command = lambda: Ventana1Temp(ventana), cursor = 'hand1')
    boton1Temp.place (relx=0.35, rely=0.5, anchor=CENTER)

    botonVariasTemp = Button(ventana, text='Ejecutar para una serie de Temperaturas', command = lambda: VentanaVariasTemp(ventana), cursor = 'hand1')
    botonVariasTemp.place (relx=0.65, rely=0.5, anchor=CENTER)

    # Se configura el título de la ventana y se ejecuta.
    ventana.title ("Cálculo de R para un Sistema Estocástico")
    ventana.mainloop()


ventana = Tk ()
VentanaPrincipal (ventana)