import numpy as np
import matplotlib.pyplot as plt

# Esta función hace la convolución, es decir y[n]= x[n]*h[n]
# donde x[n] es la secuencia o simbolo y h[n] es la rta al impulso
# ingreso los coefficientes h[n] del filtro y los símbolos x[n] 
# y devuelve la señal transmitida y[n]
# con full obtengo Ly=Lx+Lh-1
# con same obtengo Ly=Lh

def FIR (h, x, canal):
        y=np.convolve(h,x,'full')
        Ly=len(y)
        print(f"Ly para el canal {canal} es {Ly}")
        return(y)