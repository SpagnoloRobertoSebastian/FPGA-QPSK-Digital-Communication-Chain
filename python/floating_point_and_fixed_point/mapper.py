import numpy as np
import matplotlib.pyplot as plt

#Esta función recibe bits y devuelve los simbolos +1 y-1
def mapper (bits):
    simbolos=[]
    for i in range (len(bits)):
        if  bits[i] == 0:
            simbolos.append(1)
        elif bits[i]== 1:
            simbolos.append(-1)

    return(simbolos)