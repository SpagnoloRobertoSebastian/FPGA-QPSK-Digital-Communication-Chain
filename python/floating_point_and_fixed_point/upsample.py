import numpy as np
import matplotlib.pyplot as plt
#Upsample
#Esta función recibe un vector de simbolos y devuelve un vector muestras entre simbolos
# Secuencia x[n] = símbolos

def UpSample (simbolos, os, canal):
    Nsym=len(simbolos)
    sobremuestero=np.zeros(Nsym*os) 
    for i in range(len(simbolos)):
        sobremuestero[i*os]=simbolos[i]

    Lx=len(sobremuestero)
    print(f"Lx Oversample para el canal {canal} es {Lx}")   #Lx=Nbits*os
    return(sobremuestero)