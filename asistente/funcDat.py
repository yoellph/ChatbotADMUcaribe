#api para el manejo de la memoria a corto plazo del asistente

#cargamos las bibliotecas necesarias para esta api
import os
from glob import glob
from sys import path



def ls(expr = '*.*'):#lista los archivos de un directorio
    return glob(expr)

def writeData(asesor,destino,hora,dia,materia):#escribe los datos en un archivo
    file = open(destino, "w")
    file.write('asesor:'+asesor+'\n')
    file.write('hora:'+hora+'\n')
    file.write('dia:'+dia+'\n')
    file.write('materia:'+materia)
    file.close()

def loadData(path):#carga los datos#
    asesor=''
    hora=''
    dia=''
    materia=''
    if(ls(path)==[]):
        return asesor,hora,dia,materia
    with open(path, "r",encoding="utf-8",errors='ignore') as tf:
        lines = tf.read().split('\n')
    for i in lines:
        aux=i.split(':')
        print(aux)
        if(aux[0]=='asesor'):
            asesor=aux[1]
        if(aux[0]=='hora'):
            hora=aux[1]
        if(aux[0]=='dia'):
            dia=aux[1]
        if(aux[0]=='materia'):
            materia=aux[1]
        
    return asesor,hora,dia,materia

def removedata(destino):#elimina la entrada
    if(ls(destino)!=[]):
        os.remove(destino)

