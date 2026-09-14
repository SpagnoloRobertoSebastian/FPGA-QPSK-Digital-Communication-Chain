import numpy as np
import matplotlib.pyplot as plt

#Funcion PRBS9
#Leo el LBS de la PRBS9
# hago la XOR
#Desplazo el registro
#Guardo el resultado de la XOR en el MSB del registro

def lfsr (seed,Nbits, canal):
    bits= []
    lfsr_reg=seed
    #print(f"Iteracion 0: {bin(lfsr_reg)} (Hex: {hex(lfsr_reg)})")
    for i in range (Nbits):
        bit_salida= lfsr_reg & 1         #leo el LBS
        bits.append(bit_salida)          #Guardo el bit LBS
        bit_9= (lfsr_reg >> 8) & 1       #extraigo el bit 9
        bit_5= (lfsr_reg >> 4) & 1       #extraigo el bit 5
        o_xor= bit_9 ^ bit_5             # hago la XOR
        lfsr_reg= lfsr_reg >> 1         #desplazo un lugar hacia la derecha
        lfsr_reg= lfsr_reg | (o_xor<<8) #guardo o_xor en la posicion MSB
        lfsr_reg= lfsr_reg & 0x1FF      #mantengo el tamaño en 9 bits
#        print(f"Iteración {i+1}: {bin(lfsr_reg)} (Hex: {hex(lfsr_reg)})")

    Lbits=len(bits)
    print(f"PRBS9 - Nbits para el canal {canal} es {Lbits}")
    return (np.array(bits))

#semilla=0b110101010
#O_PRBS= lfsr(semilla,5)
#print(O_PRBS)

