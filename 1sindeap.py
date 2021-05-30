# -*- coding: utf-8 -*-
"""
Created on Sun May 23 21:34:51 2021

@author: Alexander Humberto Nina P.  5950236
"""

import random
import csv

distancias = "C:/Users/aaale/Desktop/TSPDatos.csv"
filas = []
tam_poblacion = 10  
POBLACION = [] 
with open(distancias, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        filas.append(row)

#print(filas)
ciudades=[x for x in range(len(filas))]
#print(ciudades)
distancias=[]
for i in range(len(ciudades)):
    distancias.append([0]*len(ciudades))

for i in range(len(ciudades)):
    for j in range(len(ciudades)):
        distancias[i][j]=int(filas[i][j])

print(distancias)

prob_mutacion = 0.1
num_generaciones = 1000
tam_ruta = [0]*tam_poblacion
fitness = [0]*tam_poblacion

costo_ruta = 1000


def distancia_ciu(ciudad1, ciudad2):
    return distancias[ciudad1][ciudad2] 

def crear_ruta():
    return random.sample(ciudades, len(ciudades))

def total_ruta():
    for i in range(tam_poblacion):
        ruta_l = 0
        for j in range(1, len(ciudades)):
            ruta_l +=  distancia_ciu(POBLACION[i][j - 1], POBLACION[i][j])

        #mejor ruta
        tam_ruta[i] = ruta_l+distancia_ciu(POBLACION[i][len(ciudades)-1],POBLACION[i][0])
        fitness[i] = 1 / tam_ruta[i]

def crear_poblacion():
    for i in range(tam_poblacion):
        POBLACION.append(crear_ruta())

 # mutación simple 
def cambio_mut(ind):
    dosran = random.sample(range(len(ciudades)), 2)
    temp = POBLACION[ind][dosran[0]]
    POBLACION[ind][dosran[0]] = POBLACION[ind][dosran[1]]
    POBLACION[ind][dosran[1]] = temp

# parcially matched  crossover del libro de Golberg
def pmx(ind1, ind2):
    tam = len(ciudades)
    p1, p2 = [0] * tam, [0] * tam
    for k in range(tam):
        p1[ind1[k]] = k
        p2[ind2[k]] = k

    corte1 = random.randint(0, tam)
    corte2 = random.randint(0, tam - 1)
    if corte2 >= corte1:
        corte2 += 1
    else:  
        corte1, corte2 = corte2, corte1

    # Aplicar cruce 
    for k in range(corte1, corte2):
        temp1 = ind1[k]
        temp2 = ind2[k]
        ind1[k], ind1[p1[temp2]] = temp2, temp1
        ind2[k], ind2[p2[temp1]] = temp1, temp2
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2


def ruleta():
    s = 0
    parcial_s = 0
    ind = 0
    for m in range(tam_poblacion):
        s = s + fitness[m]
    rand = random.uniform(0, s)
    for m in range(tam_poblacion):
        if parcial_s < rand:
            parcial_s = parcial_s + fitness[m]
            ind = ind + 1
    if ind == tam_poblacion:
        ind = tam_poblacion - 1
    return ind


# mejor ruta
def encontrar_mejor():
    llave = 1000
    fittest = 0
    for i in range(tam_poblacion):
        if tam_ruta[i] < llave:
            llave = tam_ruta[i]
            fittest = i
    return fittest
mejor_ruta=[]

# MAIN
crear_poblacion()
total_ruta()
#print(POBLACION)
#print(tam_ruta)
for j in range(num_generaciones):
    for i in range(0, tam_poblacion, 2):
        padres1 = ruleta()
        padres2 = ruleta()
        # diferentes padres no el mismo
        while True:
            if padres1 == padres2:
                padres2 = ruleta()
            else:
                break
        # actualizar
        POBLACION[i], POBLACION[i + 1] = pmx(POBLACION[padres1], POBLACION[padres2])
        #tamaños para la nueva generación
        total_ruta()

    # mutar con la probabilidad especificada
    for i in range(tam_poblacion):
        #simula aleatorios no pseudo
        rand = random.uniform(0, 1)
        
        if rand < prob_mutacion:
            cambio_mut(i)

    # calcular tamaños después de la mutación
    total_ruta()

    # encontrar el mejor camino de toda la poblacion de generaciones 
    if tam_ruta[encontrar_mejor()] < costo_ruta:
        index = encontrar_mejor()
        costo_ruta = tam_ruta[index]
        mejor_ruta=POBLACION[index].copy()

    print("Generacion", j+1, ": ", POBLACION[encontrar_mejor()], tam_ruta[encontrar_mejor()])
 
print()    
print("Mejor Ruta es:", mejor_ruta, "con tamaño ", costo_ruta)