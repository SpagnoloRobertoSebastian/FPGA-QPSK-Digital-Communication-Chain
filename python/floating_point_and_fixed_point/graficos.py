import numpy as np
import matplotlib.pyplot as plt

def plot_bits(T, bits, canal):
    t=np.arange(len(bits)+1)*T
    bits_totales = np.append(bits, bits[-1])
    plt.figure()
#    plt.step(range(len(bits)), bits, where='post')
    plt.step(t, bits_totales, where='post')
    plt.grid(True)

    plt.title(f"Bits transmitidos - Canal {canal}")
    plt.xlabel("tiempo (segundos)")
    plt.ylabel("Bit")
       
def plot_impulse(T, h, hquantize):
    n=np.arange(len(h))
    t=n*T
    plt.figure()
    plt.subplot(2,1,1)
    plt.stem(n,h, label='float64')
    plt.legend()
    plt.grid(True)
    plt.title('Filtro RC - Respuesta al impulso ')
    plt.ylabel('h[n]')
    plt.xlabel('muestras')

    plt.subplot(2,1,2)
    plt.plot(t,h, label='float64')
    plt.plot(t,hquantize, label='S(8,7) trunc')
    plt.legend()
    plt.grid(True)
    plt.ylabel('h(t)')
    plt.xlabel('tiempo (segundos)')
    
def plot_resp_freq(H_dB, freqs):
    plt.figure()
    plt.semilogx(freqs, H_dB)
    plt.grid(True, which='both')
    plt.title("Respuesta en frecuencia del filtro")
    plt.xlabel("Frecuencia")
    plt.ylabel("|H(f)| [dB]")



def plot_tx(T,os, y, yd, yquantize, canal):
    Ts=T/os
    n=np.arange(len(y))
    t=n*Ts
    #grafico a la salida del filtro
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(t,y, label='float64')
    plt.plot(t, yquantize, label='S(10,7) trunc')
    plt.legend()
    plt.grid(True)
    plt.title(f'Transmisión de los simbolos canal {canal}')
    plt.ylabel('y(t)')
    plt.xlabel('tiempo (segundos)')

    plt.subplot(2,1,2)
    plt.stem(n,y) 
    plt.grid(True)
    plt.ylabel('y[n]')
    plt.xlabel('muestras')
    

    #Grafico salida del diezmador
    nd=np.arange(len(yd))
    plt.figure()
    plt.stem(nd,yd)
    plt.grid(True)
    plt.title(f'simbolos Diezmado para el canal {canal}')
    plt.ylabel('yd[n]')
    plt.xlabel('muestras')

#   for i in range (len(y)):
#        print(f"i : {i}  t: {(t[i]) }  y[n] canal {canal}= {y[i]}")

    #for i in range (len(yd)):
        #print(f"i : {i}  t: {(t[i]) }  yd[n] canal {canal}= {yd[i]}")

def plot_eyediagram(y_n, os, Ts, offset, canal, formato):
    span = 2 * os
    segments = int((len(y_n) - offset) / span)
    x = np.arange(-os, os) * Ts
    plt.figure()

    for i in range(segments - 1):
        inicio = i * span + offset
        fin = (i + 1) * span + offset
        segmento = y_n[inicio:fin]
        plt.plot(x, segmento, 'b')
        

    plt.grid(True)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title(f"Diagrama de ojo {canal} - {formato}")

#tomo una ventana de 2T o cada 2*os muestras por segundo para construir el ojo
#Con muchas secuencias superpuestas aparece el famoso "ojo".
#ojo permite observar cómo evoluciona la señal durante el intervalo de símbolo.
#se toma las salida del filtro y[n] sin diezmar para no perder las 
# muestras por simbolo y no perder información.
#El armado del ojo:
#superpone segmenetos durante una ventana de 2Tbaudio = 2(os*Ts)=8Ts (8 muestras) o sea que
#cada segmento tiene 8 muestras


def plot_constelacion(I_dec, Q_dec, phase, formato):
    #I_dec, Q_dec Salidas diezmadas o sea y[n]
    #Elimino el transitorio inicial y final para que no contamine el grafico I vs jQ
    inicio  = 4
    fin     = -4
    I_plot = I_dec[inicio:fin]
    Q_plot = Q_dec[inicio:fin]

    plt.figure(figsize=(6,6))
    plt.plot( I_plot, Q_plot, '.', linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel("Real")
    plt.ylabel("Imag")
    plt.title( f"Constelación QPSK - Fase = {phase} - {formato}")

#La idea es saber si la constelación nos permite comprobar visualmente si estamos 
# recuperando correctamente los símbolos.
# Con phase = 0 se esta tomando las muestras aproximadamente en el máximo de cada símbolo.
# Con las fases 1, 2 y 3 se esta tomando muestras entre símbolos, donde todavía se esta
# viendo la forma de pulso del Raised Cosine. Por eso aparece esa "nube". 
#


def plot_sre(NBF_values, sre_db):

    plt.figure(figsize=(7, 5))
    plt.plot(NBF_values, sre_db, 'o-')
    plt.axhline(40, linestyle='--')
    plt.grid(True)

    plt.xlabel("NBF [bits fraccionarios]")
    plt.ylabel("SRE [dB]")
    plt.title("Relación Señal-Error de cuantización")

#analizo la resolución a la salida
#analizo si la sumatoria de y esta por debajo de la cota teorica planteo 2
def analizar_rango(y, nombre):
        ymin = np.min(y)
        ymax = np.max(y)
        ymax_abs = np.max(np.abs(y))

        print(f"--- Rango {nombre} ---")
        print(f"y_min       = {ymin}")
        print(f"y_max       = {ymax}")
        print(f"|y| máximo  = {ymax_abs}")

#simulación de retardos
#def aplicar_delay(señal, Ndelay):
#    delay = np.zeros(Ndelay)
#    señal_delay = np.concatenate((delay, señal))
#    return señal_delay