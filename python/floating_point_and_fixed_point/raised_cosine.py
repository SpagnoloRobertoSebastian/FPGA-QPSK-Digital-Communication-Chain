import numpy as np
import matplotlib.pyplot as plt

#Filtro Raised Cosine
#Calcula los coeficientes del filtro
#La ecuación del RC en el tiempo tiene una indeterminación cuando
#t=+-T/(2*beta) y la ecuacuión del RC=0/0
#Para salvar la indeterminiación se aplica el limite de la ecuación RC se obtiene
#  (beta/2)*np.sin(np.pi/(2*beta))
#Lh= Nbaud*os


def RaisedCosine (beta, T, Nbaud, os, Nomalizado):
    ti=((-Nbaud*T)/2)
    Lh=(Nbaud*os)                                            
    print(f"Nro de coefficientes del filtro o taps: {(Lh)}") 
    Ts=T/os
    TAPc=(Lh-1)/2
    print(f"Tap central: {TAPc}")
    print(f"Retardo filtro RC - Tdelay= {TAPc*Ts} seg")
    h=np.zeros(Lh) 
    for n in range(Lh):
        t_actual=ti+n*Ts
        neg_singularity=np.isclose(t_actual, -T/(2*beta), atol=1e-15)
        pos_singularity=np.isclose(t_actual, T/(2*beta),  atol=1e-15)
        if beta==0:
             h[n] = np.sinc(t_actual/T)
        elif (neg_singularity) or (pos_singularity):
             h[n]=(beta/2)*np.sin(np.pi/(2*beta))
        else:     
             h[n]=np.sinc(t_actual/T)*(np.cos(np.pi*beta*t_actual/T)/
                            (1-(4.0*beta*beta*t_actual*t_actual/ (T*T))))
        #print(f"n : {n}  t: {(t_actual) }  h[n]: {h[n]}")

    if(Nomalizado):
        h_norm=h/np.sqrt(np.sum(h**2))
    
        return(h_norm)
    else:
        return(h)
  


#uso inp.isclose() para no comparar dos variables que son flotantes
#h_n= RaisedCosine(0.5, 1, 6, 4, True)
#print("Coficientes del filtro:")
#print((h_n))
#print("Primer coeficiente")
#print(h_n[0])
#print(f"Tap central n: {len(h_n)//2}")
#print(h_n[len(h_n)//2])
#print("Ultimo coeficiente")
#print(h_n[-1])
#Norma=np.sum(h_n**2)
#print(f"Energía total del filtro: {Norma}")

# el Tap central del filtro es TAPc=(Lh-1)/2=11.5 muestras
#el retardo en segundos del filtro es Tdaley= TAPc*Ts= 12*(T/os)=115ns
#retardo en baudio TNdelay/T= 120ns/40ns bauidos o simbolos
# Ndelay = TAPc = 11.5 muestras
# Tdelay = Ndelay* Ts = 115ns
