import numpy as np
import matplotlib.pyplot as plt
# phase= 0, 1, 2, ..., (os-1)

#Diezmado
def decimador(y, os, phase, canal):
    Nd=((len(y))//os )
    yd=np.zeros(Nd)
    salto=phase
    for i in range(Nd):
        yd[i] = y[salto] 
 #       print(f"i : {i} salto= {salto} yd: {(yd[i]) }  ")
        salto = salto + os 

    Lyd=len(yd)
    print(f"Ly Diezmado para el canal {canal} es {Lyd}")    #Lyd= Ly/os
    return(yd)

#despues del decimador se obtiene 1 muestra por simbolo
#entonces se obtiene os-1 muestras de retardo ya no hay tine Tap_central muestras de retardo
#y_n= list(range(0, 101))
#yd_n= decimador(y_n, 4, 3)

#print('salida y[n]')
#print(y_n)
#print('salida diezamada yd[n]')
#print(yd_n)