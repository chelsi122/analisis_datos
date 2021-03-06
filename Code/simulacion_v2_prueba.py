#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 08:53:21 2019

@author: fh
"""

#Librerias a usar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from mylib import mylib
portafolio_sim = mylib.portafolio_sim


#%% Cargar resultados anteriores

# Cargar resultados obtenidos del algoritmo genetico
[p,a,m,hist,m_hist] = pickle.load(open('genetico.sav','rb'))

# Obtención del super padre
m0 = m.mean(axis=0) 
lim = .35
m0[np.abs(m0)<=lim] = 0
m0[m0< -lim] = -1
m0[m0>lim] = 1

# Cargar el modelo de clasificacion (KMeans) ya enetrenado
model_close = pickle.load(open('model_close.sav','rb'))


#%% Cargar datos y calcular las situaciones del archivo deseado

# Cargar los datos
archivo = 'WALMEXn'
data = pd.read_csv('../Data/'+archivo+'.csv', index_col=0)
close = data.Close
ndias = [5,20,40,125]

[precio,sit] = mylib.Sit(close,ndias,model_close)
#%% Realizar la simulacion de cada padres y el super padre
# Probar los 16 vectores en una sola acción. 
# Es requerido haber corrido Simulacion_v2 con return(Vp)

n = 16 # número de gráficas
Vp = np.zeros((n,len(sit)))
for i in np.arange(len(m)):
    Vp[i,:] = portafolio_sim(precio,sit,m[i])
Vp_m0 = portafolio_sim(precio,sit,m0)


#%%
def actualización(x0,x1,u,p,rcom):
    vp = x0+p*x1 #Valor presente del portafolios
    x0 = x0-p*u-rcom*p*abs(u) #Dinero disponible
    x1 = x1+u #Acciones disponibles
    return vp,x0,x1
    
#%%    
def actualizacion_m(precio,sit,m):
    #m es la matriz de toma de decisiones de (16,256)  
    
    nn = len(precio)
    mm = len(m)
    M = np.ones(mm)*10
    
    T = np.arange(nn)
        
    Vp = np.zeros((nn,mm))
    X0 = np.zeros((nn,mm)) 
    X1 = np.zeros((nn,mm))
    u =  np.zeros((nn,mm))
    X0[0] = 10000
    rcom = 0.0025
    
    
    
    u_max = np.floor(X0[0]/((1+rcom)*precio[0])) # Numero maximo de la operacion
    u_min  = X1[0] # Numero minimo de la operacion
    
    ####################################################################
    #AC (operacion matricial)
    if m[:,int(sit[0])]>0:
        u[0] = u_max*Ud[int(sit[t])]
    else:
        u[t] = u_min*Ud[int(sit[t])]
    
    Vp[t],X[t+1]=mylib.portafolio(X[t],u[t],precio[t],rcom)
    
    for t in T[1:]:
        
        u_max = np.floor(X[t][0]/((1+rcom)*precio[t])) # Numero maximo de la operacion
        u_min  = X[t][1] # Numero minimo de la operacion
        
        #AC (operacion matricial)
        if Ud[int(sit[t])]>0:
            u[t] = u_max*Ud[int(sit[t])]
        else:
            u[t] = u_min*Ud[int(sit[t])]
        
        Vp[t],X[t+1]=mylib.portafolio(X[t],u[t],precio[t],rcom)
    
#    return T,Vp,X,u
    return Vp
    
    
    
    
    














#%% Realizar la grafica de los resultados de todas las simulaciones
Fig = plt.figure(figsize=(20,7))
cmap = plt.cm.plasma # también se puede plt.get_cmap('plasma')
colors = cmap(np.linspace(0,1,n))
for i in np.arange(n):
    plt.plot(Vp[i,:], c=colors[i,:],label='padre%d'%i)
plt.plot(Vp_m0,'k-',linewidth=4,label='Super padre')
plt.legend(loc=1,bbox_to_anchor=(1.1, 1))
plt.vlines(1129,Vp.min(),Vp.max())
plt.xlim(0,len(Vp_m0))
plt.title(archivo)
plt.xlabel('Time (days)')
plt.ylabel('Vp ($)')
plt.show()

#Fig.savefig('../Data/'+archivo+'.png',bbox_inches='tight')

#%%








