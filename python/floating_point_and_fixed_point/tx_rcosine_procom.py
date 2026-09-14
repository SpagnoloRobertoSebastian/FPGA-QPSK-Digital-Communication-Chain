# El codigo busca simular la cadena de Tx + el canal
#donde la la cadena de Tx es:
# Generación de símbolos (+1/-1) + Mapper + Upsampling + Filtro RC/RRC (Tx) + Señal conformada en banda base
#!/usr/bin/env python
# coding: utf-8

# In[1]:


# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from Tools._fixedInt import *

##  ipython nbconvert --to latex --post PDF <Name.ipynb>

## Parametros generales

T     = 40e-9        # Periodo de baudio
Nsymb = 1000                # Numero de simbolos
os    = 4 #8                   #over sample Nro de muestras por simbolo para construir la rta al impulso
## Parametros de la respuesta en frecuencia
Nfreqs = 256                # Cantidad de frecuencias

## Parametros del filtro de caida cosenoidal
beta   = [0.0,0.5,0.99]     # Roll-Off
Nbauds = 6 #16                 # ancho temporal del pulso, o sea la sinc se trunca en -8T a 8T
## Parametros funcionales
Ts = T/os                   # Frecuencia de muestreo


# In[2]:

#Esta Clase calcula el filtro raised cosine
def rcosine(beta, Tbaud, oversampling, Nbauds, Norm):
    """ Respuesta al impulso del pulso de caida cosenoidal """
    t_vect = np.arange(-0.5*Nbauds*Tbaud, 0.5*Nbauds*Tbaud, 
                       float(Tbaud)/oversampling)    
               
#float(Tbaud) Lo transforma a punto flotante para asegurar que la división sea en flotante y no enntera

    y_vect = []     #crea un vector vacio, no es necesario agragarle la longitud
                    #Luego usando el append va agregando una muestra a medida que lo vas usando
    for t in t_vect:                                                    # para c/instante de t evalua la ecuacion de RC
        y_vect.append(np.sinc(t/Tbaud)*(np.cos(np.pi*beta*t/Tbaud)/     #o sea calcula la rta al impulso punto a punto
                                        (1-(4.0*beta*beta*t*t/          #np.sinc() calcula sin(πx)/(πx)
                                            (Tbaud*Tbaud)))))

    y_vect = np.array(y_vect)                                           # convierte a vector NumPy

    if(Norm):
        return (t_vect, y_vect/np.sqrt(np.sum(y_vect**2)))  #si es true, devuelve la versión noramaliza RC
        #return (t_vect, y_vect/y_vect.sum())
    else:
        return (t_vect,y_vect)                              #sino devuelve RC


# In[3]:

### Calculo de tres pulsos con diferente roll-off
(t,rc0) = rcosine(beta[0], T,os,Nbauds,Norm=False)
(t,rc1) = rcosine(beta[1], T,os,Nbauds,Norm=False)
(t,rc2) = rcosine(beta[2], T,os,Nbauds,Norm=False)

print('Numeros de coeficientes del filtro RC')
print(Nbauds*os)
#print(len(rc0))
#print(len(t))

print('Mostrando los primeros 10 valores en t')
print(t[:10])

print('Mostrando los primeros 10 coeficientes de h(t)')
print('Es decir h[0], h[1] .. h[127]')
print(rc0[:10])

print (np.sum(rc0**2),np.sum(rc1**2),np.sum(rc2**2))

### Generacion de las graficas Respuesta al impulso para los tres casos de Roll off
plt.figure(figsize=[14,7])
plt.plot(t,rc0,'ro-',linewidth=2.0,label=r'$\beta=0.0$')
plt.plot(t,rc1,'gs-',linewidth=2.0,label=r'$\beta=0.5$')
plt.plot(t,rc2,'k^-',linewidth=2.0,label=r'$\beta=1.0$')
plt.legend()
plt.grid(True)
#plt.xlim(0,len(rc0)-1)
plt.xlabel('tiempo [seg]')
plt.ylabel('Magnitud')
plt.title('Respuesta al impulso - Filtro Raised Cosine')

#genera una secuencia o tren de impulsos y lo convoluciona con el filtro con diferente roll off
symb00    = np.zeros(int(os)*3+1);symb00[os:len(symb00)-1:int(os)] = 1.0
rc0Symb00 = np.convolve(rc0,symb00);
rc1Symb00 = np.convolve(rc1,symb00);
rc2Symb00 = np.convolve(rc2,symb00);

offsetPot = os*((Nbauds//2)-1) + int(os/2)*(Nbauds%2) + 0.5*(os%2 and Nbauds%2)

#Genera grafico de la rta al impulso por separado y luego la resultante
plt.figure(figsize=[14,7])
plt.subplot(3,1,1)
plt.plot(np.arange(0,len(rc0)),rc0,'r.-',linewidth=2.0,label=r'$\beta=0.0$')
plt.plot(np.arange(os,len(rc0)+os),rc0,'k.-',linewidth=2.0,label=r'$\beta=0.0$')
plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')
plt.grid(True)
plt.legend()
plt.plot(rc0Symb00[os::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
#plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
plt.title('Rcosine - OS: %d'%int(os))

#plt.figure()
plt.subplot(3,1,2)
plt.plot(np.arange(0,len(rc1)),rc1,'r.-',linewidth=2.0,label=r'$\beta=0.5$')
plt.plot(np.arange(os,len(rc1)+os),rc1,'k.-',linewidth=2.0,label=r'$\beta=0.5$')
plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')
plt.grid(True)
plt.legend()
plt.plot(rc1Symb00[os::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
#plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
#plt.title('Rcosine - OS: %d'%int(os))

#plt.figure()
plt.subplot(3,1,3)
plt.plot(np.arange(0,len(rc2)),rc2,'r.-',linewidth=2.0,label=r'$\beta=1.0$')
plt.plot(np.arange(os,len(rc2)+os),rc2,'k.-',linewidth=2.0,label=r'$\beta=1.0$')
plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')
plt.grid(True)
plt.legend()
plt.plot(rc2Symb00[os::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
#plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
#plt.title('Rcosine - OS: %d'%int(os))

plt.show()


# In[4]:

#Respuesta en frecuencia
def resp_freq(filt, Ts, Nfreqs):
    """Computo de la respuesta en frecuencia de cualquier filtro FIR"""
    H = [] # Lista de salida de la magnitud
    A = [] # Lista de salida de la fase
    filt_len = len(filt)

    #### Genero el vector de frecuencias
    freqs = np.matrix(np.linspace(0,1.0/(2.0*Ts),Nfreqs))
    #### Calculo cuantas muestras necesito para 20 ciclo de
    #### la mas baja frec diferente de cero
    Lseq = 20.0/(freqs[0,1]*Ts)

    #### Genero el vector tiempo
    t = np.matrix(np.arange(0,Lseq))*Ts

    #### Genero la matriz de 2pifTn
    Omega = 2.0j*np.pi*(t.transpose()*freqs)

    #### Valuacion de la exponencial compleja en todo el
    #### rango de frecuencias
    fin = np.exp(Omega)

    #### Suma de convolucion con cada una de las exponenciales complejas
    for i in range(0,np.size(fin,1)):
        fout = np.convolve(np.squeeze(np.array(fin[:,i].transpose())),filt)
        mfout = abs(fout[filt_len:len(fout)-filt_len])
        afout = np.angle(fout[filt_len:len(fout)-filt_len])
        H.append(mfout.sum()/len(mfout))
        A.append(afout.sum()/len(afout))

    return [H,A,list(np.squeeze(np.array(freqs)))]


# In[5]:


### Calculo respuesta en frec para los tres pulsos
[H0,A0,F0] = resp_freq(rc0, Ts, Nfreqs)
[H1,A1,F1] = resp_freq(rc1, Ts, Nfreqs)
[H2,A2,F2] = resp_freq(rc2, Ts, Nfreqs)

### Generacion de los graficos - filtro en el dominio frecuencial
plt.figure(figsize=[14,6])
plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.0$')
plt.semilogx(F1, 20*np.log10(H1),'g', linewidth=2.0, label=r'$\beta=0.5$')
plt.semilogx(F2, 20*np.log10(H2),'k', linewidth=2.0, label=r'$\beta=1.0$')

plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
plt.legend(loc=3)
plt.grid(True)
plt.xlim(F2[1],F2[len(F2)-1])
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.title('Filtro Raised cosine en el dominio frecuencial')
plt.show()


# In[6]:

#generan los symbolsI y symbolsQ  aleatorios con valores +1 y -1.
#parece que es 2-PAM o BPSK en banda base
# I y Q son secuencias que tienen impulsos discretos +1 y -1
symbolsI = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;
symbolsQ = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;

#np.random.uniform genara Nsymb valores aleatorio entre 1 y -1
# luego lo compara con cero convierte el vector numerico a booleano, si es >0 es true y sino es false
# python concidera que true es 1 y false es 0 entonces al multiplicarlo 
#por 2 genera un vector con 0 y 1 y luego al restarle -1 obtiene un vector  de -1 y +1
#es así como genera los simbolos 1 y -1
#la función np.random.uniform la función genera valores con misma probabilidad 

label = 'Simbolos: %d' % Nsymb
plt.figure(figsize=[14,6])
plt.subplot(1,2,1)
plt.hist(symbolsI,label=label)
plt.legend()
plt.xlabel('Simbolos')
plt.ylabel('Repeticiones')
plt.subplot(1,2,2)
plt.hist(symbolsQ,label=label)
plt.legend()
plt.xlabel('Simbolos')
plt.ylabel('Repeticiones')

plt.show()

#en el histograma se observa que la fuente binaria es aproximadamente equiprobable

# In[7]:

# Upsample o interpolador, agrega ceros a cada simbolo
zsymbI = np.zeros(os*Nsymb); zsymbI[1:len(zsymbI):int(os)]=symbolsI
zsymbQ = np.zeros(os*Nsymb); zsymbQ[1:len(zsymbQ):int(os)]=symbolsQ

#zsymbI = np.zeros(os*Nsymb) crea un vector de ceros con longitud os*Nsymb
#El zsymbI comienza desde el indice 1 y va salntando cada os y agrega un simbolo del vector symbolsI
#o sea coloca un simbolo cada os
#Al empezar de 1 tenes un corriemiento temporal de la secuencia o desfaseje temporal
#

plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(zsymbI,'o')
plt.xlim(0,20)
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(zsymbQ,'o')
plt.xlim(0,20)
plt.grid(True)

plt.show()


# In[8]:


# # Calculo de tres pusos con diferente roll-off
# (t,rc01) = rcosine(0.1, T,os,Nbauds,Norm=True)
# (t,rc05) = rcosine(0.5, T,os,Nbauds,Norm=True)
# # Generacion de las graficas
# plt.figure()
# plt.plot(rc01,'o-r',linewidth=2.0,label=r'$\beta=0.1$')
# plt.plot(rc05,'s-g',linewidth=2.0,label=r'$\beta=0.5$')
# plt.legend()
# plt.grid(True)
# plt.xlim(0,len(rc01)-1)
# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')
# #plt.show()


# In[13]:

#simulando la señal recibida una vez que pasa por el canal
#aplica filtro FIR RC
symb_out0I = np.convolve(rc0,zsymbI,'same'); symb_out0Q = np.convolve(rc0,zsymbQ,'same')
symb_out1I = np.convolve(rc1,zsymbI,'same'); symb_out1Q = np.convolve(rc1,zsymbQ,'same')
symb_out2I = np.convolve(rc2,zsymbI,'same'); symb_out2Q = np.convolve(rc2,zsymbQ,'same')

# el modo 'same' lo que hace es la longitud de salida symb_out0I lo deja igual a la longitud rc0 o sea le 
# quita los ceros que vienen de zsymbI para poder graficarlo directamente


#Esta pasando la secuencia por el filtro FIR RC del transmisor que equivale a y[n]=x[n]∗h[n]
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])  #la funcion plt ya genera el eje x como muestras n=0 1 2 3 ..
plt.plot(symb_out1I,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
plt.plot(symb_out2I,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
plt.title('Señal a la salida del filtro FIR RC')

plt.subplot(2,1,2)
plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
plt.plot(symb_out1Q,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
plt.plot(symb_out2Q,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
#plt.figure(figsize=[10,6])
#plt.plot(np.correlate(symbolsI,2*(symb_out0I[3:len(symb_out0I):int(os)]>0.0)-1,'same'))

plt.show()


# In[14]:

#simulando el diagrama de ojo 
def eyediagram(data, n, offset, period):
    span     = 2*n
    segments = int(len(data)/span)
    xmax     = (n-1)*period
    xmin     = -(n-1)*period
    x        = list(np.arange(-n,n,)*period)
    xoff     = offset

    plt.figure()
    for i in range(0,segments-1):
        plt.plot(x, data[(i*span+xoff):((i+1)*span+xoff)],'b')       
    plt.grid(True)
    plt.xlim(xmin, xmax)
    plt.show()


# In[15]:
# al hacer symb_out0I[100:len(symb_out0I)-100] elimina los transitorios
#offset depliega los segmentos
#para cada β dibuja dos ojos, uno para I y otro para Q. En total son 6 diagramas. 
eyediagram(symb_out0I[100:len(symb_out0I)-100],os,5,Nbauds) #beta=0.0 ==> I y Q
eyediagram(symb_out0Q[100:len(symb_out0Q)-100],os,5,Nbauds)

eyediagram(symb_out1I[100:len(symb_out1I)-100],os,5,Nbauds) #beta=0.5 ==> I y Q
eyediagram(symb_out1Q[100:len(symb_out1Q)-100],os,5,Nbauds)

eyediagram(symb_out2I[100:len(symb_out2I)-100],os,5,Nbauds) #beta=1  ==> I y Q
eyediagram(symb_out2Q[100:len(symb_out2Q)-100],os,5,Nbauds)

plt.show()

#plt.show(block=False)
#raw_input("Press Enter")
#plt.close()


# In[16]:

# Constelaciones
# le esta aplicando las constelacionaes a la salida del filtro FIR RC o sea a y[n]
offset = 2             #es un desplazamiento que le permite que le indica donde comienza a muestrear
plt.figure(figsize=[6,6])
plt.plot(symb_out0I[100+offset:len(symb_out0I)-(100-offset):int(os)],
         symb_out0Q[100+offset:len(symb_out0Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
#Esta recorriendo el vector desde 100+offset hasta len(symb_out0I) a pasos de os
#O sea esta tomando una muesta cada os simbolos
#Comienza a partir de 100 para dejar pasar el transitorio y esperar que se forme la sinc
#Corta el final para descarter el transitorio final
#al hacer :int(os) esta saltando cada os o sea DECIMADOR
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
#plt.title('Constelaciones para simbolos I, Q - Roll Off = %.2f' % beta[0])
plt.title(f'Constelaciones para simbolos I,  Q - Roll Off = {beta[0]:.2f}')

plt.figure(figsize=[6,6])
plt.plot(symb_out1I[100+offset:len(symb_out1I)-(100-offset):int(os)],
         symb_out1Q[100+offset:len(symb_out1Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.title(f'Constelaciones para simbolos I,  Q - Roll Off = {beta[1]:.2f}')

plt.figure(figsize=[6,6])
plt.plot(symb_out2I[100+offset:len(symb_out2I)-(100-offset):int(os)],
         symb_out2Q[100+offset:len(symb_out2Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.title(f'Constelaciones para simbolos I,  Q - Roll Off = {beta[2]:.2f}')
plt.show()


# In[ ]:


#Lo que esta haciendo el codigo es:
#Símbolos
#↓
#Upsample
#↓
#filtro RC
#↓
#Descarto transitorio inicial
#↓
#Descarto transitorio final
#↓
#Tomo una muestra cada símbolo
#↓
#Grafico I vs Q

