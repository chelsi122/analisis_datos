#!/usr/bin/env python

import numpy as np
from time import time

###############################################################################
# Se corre la simulación con vectores de decisiones genéticos

l_vec = 256 #longitud del vector de toma de decisiones
l_dec = 128 #Cantidad de vectores de toma de decisiones

### Se otorgan 3 opciones a la toma de decisiones
decisiones = [[np.random.randint(-1,2) for i in range(l_vec)] for i in range(l_dec)] # Inicial. 

t1 = time()

iteraciones = 300
hist = np.zeros(iteraciones)
for cic in range(iteraciones):
    a = []
    m = []
    
    
    for i in decisiones: ## se suman todos vectores de decisión para escoger el que de la suma mayor
        
#        #######################################################################
#        T,Vp,X,u = portafolio_sim(precio,sit,i) ###############################
#        a.append(Vp[-1]) ######################################################
#        #######################################################################
        
        
        #######################################################################
        Sim = portafolios_sim(data,sit,i) #####################################
        a.append(Sim[:,-1].sum()) #############################################
        #######################################################################
        
    hist[cic] = max(a)
    for i in range(l_dec//4): ## se escojen los mejores resultados
        m.append(decisiones[a.index(max(a))])
        a.pop(a.index(max(a)))
    
    m = np.array(m) ## hacemos l_vec nuevos vectores derivados únicamente de los 25% mejores anteriores.
    decisiones = [[np.random.choice(m.T[i]) for i in range(l_vec)] for i in range(l_dec)]
    for k in range(l_dec): ## mutamos un tercio de los dígitos de los l_vec vectores que tenemos. 
        for i in range(int(l_dec//2)):
            decisiones[i][np.random.randint(0,l_vec)] = np.random.randint(0,3)-1
    [decisiones.append(i) for i in m] ## agregamos los 'padres' de las nuevas generaciones a la lista. 


print(decisiones[-5:], time()-t1)

