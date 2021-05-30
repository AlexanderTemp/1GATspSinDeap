# -*- coding: utf-8 -*-
"""
Created on Wed May 19 11:40:31 2021

@author: aaale
"""
# tamaño maximo de un integer
from sys import maxsize  
# A=0,B=1,C=2,D=3, E=4 
grafo_princ=[[0, 7,  9, 8,20],
            [ 7, 0, 10, 4,11],
            [ 9,10,  0,15, 5],
            [ 8, 4, 15, 0,17],
            [20,11,  5,17, 0]]
num_nodos=5
def siguiente_perm(l):
    n=len(l)
    i=n-2
    while i>=0 and l[i]>l[i+1]:
        i-=1
    if i==-1:
        return False
    j=i+1
    while j<n and l[j]>l[i]:
        j+=1
    j-=1
    l[i],l[j]=l[j],l[i]
    izq=i+1
    der=n-1
    while izq<der:
        l[izq], l[der]=l[der], l[izq]
        izq+=1
        der-=1
    return True
s=0
vertices=[]
for i in range(num_nodos):
    if i != s:
        vertices.append(i)
min_cam=maxsize
while True:
    costo_actual=0
    k=s
    for i in range(len(vertices)):
        costo_actual+=grafo_princ[k][vertices[i]]
        k=vertices[i]
    costo_actual+=grafo_princ[k][s]
    min_cam=min(min_cam, costo_actual)
    if not siguiente_perm(vertices):
        break
print(min_cam)
    



