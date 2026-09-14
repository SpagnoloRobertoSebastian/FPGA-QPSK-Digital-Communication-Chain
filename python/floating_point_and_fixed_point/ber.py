import numpy as np
import matplotlib.pyplot as plt

#BER= Bits incorrectos/N
#Para generar los bits incorrectos se compara los bits Tx con los bits Rx
#N= Nro total de bits transmitidos
#Salida del diezmador
#n_delay retardo del FIR, Ndelay=tap_central= taps/2 (muestras) o Ndelay/os (simbolos)

def calcular_decisor_ber(bits_tx, simbolos_rx, n_delay, canal):

    # Decisión del símbolo recibido
    bits_rx = (simbolos_rx < 0).astype(int)

    # Eliminar el retardo del filtro
    #las primeras n_delay posiciones son de retardo y se elimina
    bits_rx = bits_rx[n_delay:]

    # Igualar longitudes para que los bits del transmisor y receptor correspondan al mismo simbolo
    N = min(len(bits_tx), len(bits_rx))

    bits_tx_comp = bits_tx[:N]
    bits_rx_comp = bits_rx[:N]

    # Comparación bit a bit
    errores = np.sum(bits_tx_comp != bits_rx_comp)

    # BER
    ber = errores / N

    print(f" Bits TX para el canal {canal} es {bits_tx_comp[:20]}")  #imprimo los primeros 20 para comparar
    print(f" Bits RX para el canal {canal} es {bits_rx_comp[:20]}")
    print(f" cantidad de errores para el canal {canal} es {errores}")

    return ber, errores, N

#se obtuvo la constelación correcta y se  recupero exactamente la PRBS9.
