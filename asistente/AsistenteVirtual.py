import email
import correos_nuevos as cin
import time
import enviar_correo as cout
from pathlib import Path
from glob import glob
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import subprocess
import time
import os
from chatterbot.response_selection import get_random_response
import transformer as pre
import var as v
import platform
import re
from unicodedata import normalize
import funcDat as F
##definir Chatbot
##este se encargara de manejar la conversacion entre el usuario y el agente
chatbot = ChatBot("CAM",
    storage_adapter='chatterbot.storage.SQLStorageAdapter', ##Almacena aprendizaje del chatterbot
    logic_adapters=[
        {'import_path': 'mtadapter.transformer'},##Carga el modulo del transformer para la toma de desisiones
        {'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'nan',
            'maximum_similarity_threshold': 0.99},
    ],database='./database.sqlite', #fichero de la base de datos (si no existe se creará automáticamente)##ubicacion de la bd del aprendizaje del chatterbot
        
    
    read_only=True,
)
chatbot.storage.drop()
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train("chatterbot.corpus.spanish.greetings")

trainer = ListTrainer(chatbot) ##entrenamiento del chatterbot para input triviales

trainer.train([
    "gracias",
    "Gracias, que tengas un buen día",
])


def load_data(path):##carga informacion de archivos
    with open(path, "r",encoding="utf-8") as tf:
        lines = tf.read().split('\n')
    return lines
def ls(expr = '*.*'):#lista los archivos de un directorio
    return glob(expr)
def ping(host):##realiza una solicitud tipo ping para verificar si el destino esta disponible
    param = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', param, '1', host]

    a=subprocess.call(command,stdout=subprocess.DEVNULL ,stderr=subprocess.STDOUT) == 0
    return a

##variables que se pueden extraer del correo
organizacion=''
destino=''
subject=''
texto='hola buen día '
nombreDestino=''
asesoria=''
data=''
string_mensaje = '¿cual es la asignatura de tu asesoria?'+v.asignaturas #mensaje predeterminado
def spar(dt):##Realiza la separacion de variables que el transformer proceso
    aux=dt.split(',')
    for a in aux:
        if(a.split('.')[0].find('asesoria')!=-1):
            v.asesor=(a.split('.')[1])
            print(v.asesor)
        if(a.split('.')[0].find('dia')!=-1):
            v.dia=(a.split('.')[1])

#ciclo principal
while(1):
    ##Los siguientes 3 whiles verifican la disponibilidad de los servidores de Google
    while(ping("smtp.gmail.com")==False):
        print("No Conection to Google Mail")
        for i in range(60):
            time.sleep(1)
            print("Check conection in: ",60-i,"s")
    while(ping("smtp.gmail.com")==False):
        print("No Conection to Google Calendar")
        for i in range(60):
            time.sleep(1)
            print("Check conection in: ",60-i,"s")
    while(ping("smtp.gmail.com")==False):
        print("No Conection to Google Meet")
        for i in range(60):
            time.sleep(1)
            print("Check conection in: ",60-i,"s")
    print("Conection to Google was succesfull")
    ##Obtiene los correos del CAM
    i,result,data,mail = cin.busca_correosnuevos(cin.EMAIL_ACCOUNT,cin.PASSWORD)
    ##crea archivos con todo el cuerpo de correos
    cin.crea_archivo(i,result,data,mail)
    ##lista de todos los correos disponibles
    files=ls('*.txt')
    ##for para cada Email obtenido
    for da in files:
        v.vainit()#iniciamos las variables globales
        data=''
        #cargamos el Email
        li=load_data(da)
        #extremos datos como el correo del destinatario, asunto, nombre del destinatario
        destino=(li[0].split(':')[-1])
        nombreDestino=(destino.split('<')[0]).split(' ')[1]
        destino=(destino.split('<')[-1])
        destino=destino.split('>')[0]
        print(destino)
        subject=(li[3].split(': ')[-1])
        ##revisamos que el origen de la solicitud esta dentro de la organizacion unicaribe.edu.mx
        if(destino.find('ucaribe')==-1):
            print("error origen fuera de organizacion:"+destino)
            continue
        ##revisamos que el asunto del correo no se encuentre la palabra acceptado
        if(li[3].find('Aceptado:')!=-1):
            print("confirmacion de meet"+destino)
            continue
        ##verificamos que el asunto del correo no se encuentre la palabra rechazado
        if(li[3].find('Rechazado:')!=-1):
            print("Rechazo de meet"+destino)
            continue
        #mostramos el origen, su nombre y el asunto
        print("origen: ",destino)
        print("Nombre: ",nombreDestino)
        print("Asunto: ",subject)
        j=0
        i=5
        ##acontinuacion se filtran los datos del body del correo electronico
        while(li[i]!='\t'):
            #print("j: ",j,'-- ',li[i])
            if(li[i]==''):
                j=j+1
            if(li[i].find('Forwarded message')!=-1):
                break
            if(li[i].find('--')!=-1):
                break
            if(j>4):
                break
            if(j >= 1 and li[i+1].find('El ')!=-1):
                break
            if(li[i]!=''):
                data=data+li[i]+' '
                j=0
            i=i+1
        ## se quitan los asentos y simbolos de la Data a procesar
        s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",normalize( "NFD", data), 0, re.I)
        data = normalize( 'NFC', s)
        ##se envian al transformer para extraer caracteristicas
        asesoria=pre.trans(data)
        ##se separan las caracteristicas obtenidas por el transformer
        spar(asesoria)
        ##mostramos las caracteristicas obtenidas por el transformer
        print(asesoria)
        #si exixten datos anteriores para este destinatario se cargan, si no se inicializan las variables en '' 
        z,x,c,b=F.loadData(destino)
        #copiamos las variables locales a variables globales para poder usarlas dentro de los adaptadores del chatterbot
        v.Aasesor=z
        v.Ahora=x
        v.Adia=c
        v.Aasignatura=b
        v.asesoria=asesoria
        v.data=data
        v.destino=destino
        v.nombreDestino=nombreDestino
        v.subject=subject
        v.texto=texto +v.nombreDestino+'.\n'+ string_mensaje
        ##generamos una respuesta del chatterbot, quien gestiona todas las salidas a las apis de calendar
        respose=chatbot.get_response(data)
        #mostramos los datos procesados por el asistente
        print("mensaje:",data)
        print("asesor: "+v.asesor)
        print("dia: "+v.dia)
        print("hora:",v.hora)
        print("asignatura:",v.asignatura)
        #convertimos las respuestas del asistente en una variable de tipo string
        respose=str(respose)
        if(respose=='nan'):
            print(v.texto)
            respose=v.texto
        else:
            print(respose)
        #conectamos a la api de correo electornico
        conectar = cout.connect_email(cout.us,cout.pas) #Funcion Conectar
        #enviamos la respuesta por el correo electronico
        cout.enviar_email(conectar,cout.us,v.destino,"Re: "+v.subject,respose)
    #eliminamos todos los archivos generados y esperamos que se termine el timeout para que no nos bloquee google
    for da in files:
        os.remove(da)
    if(len(files)==0):
        print("No found new emails")
    else:
        print("Found new emails")
    for i in range(30):
        print(".",end=" ",flush=True)
        time.sleep(1)
    print(" ")