import numpy as np
import matplotlib.pyplot as plt
from Tools._fixedInt import *
from prbs9 import lfsr
from mapper import mapper
from upsample import UpSample
from raised_cosine import RaisedCosine
from tx_filter import FIR
from downsample import decimador
from rta_freq import resp_freq
from graficos import plot_bits, plot_impulse, plot_tx, plot_resp_freq, plot_constelacion, plot_eyediagram, plot_sre, analizar_rango
from ber import calcular_decisor_ber
from resol_desing import analisis_sre

# Este programa simula la cadena de Transmisión
#PRBS9 -> Mapper -> Upsample -> Raised Cosine -> downsample -> BER
# usa la convencion 0 -> +1 y 1 -> -1

################################################################################
#  Ejercicio 1                     Pareamentros
################################################################################
#Fclk=100MHz ==> clk= 1/Fclk = 10ns = Ts
#Ts=Tbaudio/OS ==> Tbaudio = OS*Ts
#Paramentros PRBS9
seed_I=0x1AA
seed_Q=0x1FE
Nbits=1000

#Pareamentros Filtro RC
OS=4                        #oversample
Ts= 10e-9                   #tiempo de muestreo o Tclk
Tbaudio= OS*Ts              #duración del símbolo, 1 baudio son os ciclos de clock
Baudio= 1/Tbaudio           #fcia Baudio
beta=0.5                    #roll off
Nbauds= 6                   #Filtro RC definido en -Nbauds/2< n < Nbauds/2 o sea duración 
                            #del filtro son Nbauds periodos de simbolos
Norm= True                 #nomalización del filtro RC
Nfcia= 1024                 #parámetro respuesta en frecuencia |H(f)|dB

#Diezmado
Phase=0               #phase= 0, 1, 2, ..., (os-1)
print('************************************')
print('Parámetros')
print(f"Ts= {Ts} seg")
print(f"Tbaudio= {Tbaudio} seg")
print(f"F Baudio= {Baudio} Hz")
print(f"oversamle= {OS} ")
print(f"Nbaudios= {Nbauds}")
print(f"roll off= {beta}")
print(f"Phase= {Phase}")
print(f"Normalizació de h= {Norm}")
print('************************************')
print('')
################################################################################
#            Secuencia binaria Pseudoaleatoria  PRBS9
################################################################################
PRBS9_I= lfsr (seed_I, Nbits, "I")
PRBS9_Q= lfsr (seed_Q, Nbits, "Q")

################################################################################
#            Mapeo
################################################################################
Symbol_I=mapper(PRBS9_I)
Symbol_Q=mapper(PRBS9_Q)

################################################################################
#           Upsamble (Interpolador)
################################################################################
upsample_I= UpSample(Symbol_I,OS, "I")
upsample_Q= UpSample(Symbol_Q,OS, "Q")


#print(f"canal I - bits:      {PRBS9_I}")
#print(f"canal I - Simbolos:  {Symbol_I}")
#print(f"canal Q - bits:      {PRBS9_Q}")
#print(f"canal Q - Simbolos:  {Symbol_Q}")
#print(f"canal I - Upsample:  {upsample_I}")
#print(f"canal Q - Upsample:  {upsample_Q}")

################################################################################
#       Coeficientes   Filtro Raised Cosine (RC)
################################################################################
h_n= RaisedCosine(beta, Tbaudio, Nbauds, OS, Norm)
Norma=np.sum(h_n**2)
print("-----------------------------------------------------")
print(f"Energía total del filtro: {Norma}")
H_abs = np.sum(np.abs(h_n))
print(f"Suma de |h[k]| = {H_abs}")
print('Coeficientes del filtro en punto flotante')
print(h_n)
print("-----------------------------------------------------")

################################################################################
#           salida Transmisión del filtro FIR RC
################################################################################
output_I= FIR (h_n, upsample_I, "I")
output_Q= FIR (h_n, upsample_Q, "Q")

################################################################################
#           Downsample (diezmado)
################################################################################
O_I_diezmado= decimador(output_I, OS, Phase, "I")
O_Q_diezmado= decimador(output_Q, OS, Phase, "Q")


################################################################################
#          Decisión - BER
################################################################################

ber_I, errores_I, N_I = calcular_decisor_ber (PRBS9_I,O_I_diezmado, 3, "I")
ber_Q, errores_Q, N_Q = calcular_decisor_ber (PRBS9_Q,O_Q_diezmado, 3, "Q")

print("********************************************************")
print(f"BER canal I = {ber_I}")
print(f"Errores canal I = {errores_I}/{N_I}")

print(f"BER canal Q = {ber_Q}")
print(f"Errores canal Q = {errores_Q}/{N_Q}")
print("********************************************************")

################################################################################
#          Ejercicio 2 - Criterio Resolución de diseño
################################################################################

NBF_values, sre_db, h_norm = analisis_sre(h_n)
plot_sre(NBF_values, sre_db)
plt.show()

################################################################################
#         analizo la resolución a la salida del FIR
#   verifico que la simulación este por debajo de la cota teorica
################################################################################
analizar_rango(output_I, "FIR I")
analizar_rango(output_Q, "FIR Q")

cota = np.sum(np.abs(h_n))
print(f"Cota teórica = {cota}")
print(f"Máximo observado I = {np.max(np.abs(output_I))}")
print(f"Máximo observado Q = {np.max(np.abs(output_Q))}")

################################################################################
#          Punto fijo  -  Función cuantización
################################################################################
def quantize_vector(x, total_bits, frac_bits, round_mode):
    yq = np.zeros(len(x), dtype=float)
    for i, v in enumerate(x):
        q = DeFixedInt(total_bits, frac_bits,
                       signedMode='S',
                       roundMode=round_mode,
                       saturateMode='saturate')
        q.value = float(v)
        yq[i] = q.fValue
    return yq
################################################################################

################################################################################
#            Mapper - Cuantizado
################################################################################
s20_Symbol_I = quantize_vector(Symbol_I, 2, 0, 'trunc')
s20_Symbol_Q = quantize_vector(Symbol_Q, 2, 0, 'trunc')

################################################################################
#            Upsample - Cuantizado
################################################################################
s20_upsample_I = quantize_vector(upsample_I, 2, 0, 'trunc')
s20_upsample_Q = quantize_vector(upsample_Q, 2, 0, 'trunc')

################################################################################
#           Coeficientes Filtro FIR RC- Cuantizado
################################################################################
s87_filtro_rc = quantize_vector(h_n, 8, 7, 'trunc')
print("-----------------------------------------------------")
print('Coeficientes del filtro en punto fijo S(8,7)')
print(s87_filtro_rc)
print("-----------------------------------------------------")
################################################################################
#            salida y[n] - Cuantizado
################################################################################
s10_7_output_I= FIR (s87_filtro_rc, s20_upsample_I, "I")
s10_7_output_Q= FIR (s87_filtro_rc, s20_upsample_Q, "Q")
#s10_7_upsample_I = quantize_vector(output_I, 10, 7, 'trunc')


################################################################################
#            Diezmado - Cuantizado
################################################################################
s10_7_diezmado_I= decimador(s10_7_output_I, OS, Phase, "I")
s10_7_diezmado_Q= decimador(s10_7_output_Q, OS, Phase, "Q")

################################################################################
#          Decisión - BER - Señal recibida cuantizada
################################################################################
s10_7_ber_I, s10_7_errores_I, s10_7_N_I = calcular_decisor_ber (PRBS9_I,s10_7_diezmado_I, 3, "I")
s10_7_ber_Q, s10_7_errores_Q, s10_7_N_Q = calcular_decisor_ber (PRBS9_Q,s10_7_diezmado_Q, 3, "Q")

print("********************************************************")
print(f"BER- Señal recibida cuantizada - canal I = {s10_7_ber_I}")
print(f"Errores canal I = {s10_7_errores_I}/{s10_7_N_I}")

print(f"BER- Señal recibida cuantizada - canal Q = {s10_7_ber_Q}")
print(f"Errores canal Q = {s10_7_errores_Q}/{s10_7_N_Q}")
print("********************************************************")

################################################################################
#          Graficos
################################################################################
#plot_bits(Tbaudio, PRBS9_I, "I")
#plot_bits(Tbaudio, PRBS9_Q, "Q")
#plt.show()

plot_impulse(Tbaudio,h_n, s87_filtro_rc)


#H_dB, freqs = resp_freq(h_n, Ts, Nfcia)
#plot_resp_freq(H_dB, freqs)
plt.show()

plot_tx(Tbaudio, OS, output_I, O_I_diezmado, s10_7_output_I,"I")
plot_tx(Tbaudio, OS, output_Q, O_Q_diezmado, s10_7_output_Q, "Q")
plt.show()

#Me aseguro que el ojo se construya en la zona del regimen permanente y no transitoria
data_I = output_I[100:-100] 
plot_eyediagram(data_I, OS, Ts, 5, "I", "float64")

s10_7data_I = s10_7_output_I[100:-100]
plot_eyediagram(s10_7data_I, OS, Ts, 5, "I", "S(10,7)")

data_Q = output_Q[100:-100]
plot_eyediagram(data_Q, OS, Ts, 5, "Q", "float64")

s10_7data_Q = s10_7_output_Q[100:-100]
plot_eyediagram(s10_7data_Q, OS, Ts, 5, "Q", "S(10,7)")

plot_constelacion(O_I_diezmado, O_Q_diezmado, Phase, "float64")
plot_constelacion(s10_7_diezmado_I, s10_7_diezmado_Q, Phase, "S(10,7)")
plt.show()


