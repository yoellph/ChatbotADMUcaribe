## api para el chatterbot y transformer
from chatterbot.logic import LogicAdapter
from chatterbot.comparisons import LevenshteinDistance
from nltk.tokenize import word_tokenize
from chatterbot.conversation import Statement
import datetime
import nltk
from numpy.core import numeric
import requests
import json
from nltk.corpus import stopwords
from funtime import today
import transformer as tr
import var as av
import calendario_1 as agendar
import db
import funtime as t
import pytz
import funcDat as DF
def veryfi(tex,text):#funcion para verificar una palabra en un Texto
    a = True
    b = len(tex)
    c = len(text)
    for i in range(0,b):
        for j in range(0,c):
            if(text[j]==tex[i]):
                return True

class transformer(LogicAdapter):##LogicAdapter del transformer
    def __int__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
    
    def can_process(self, statement):#verificamos que pueda procesar el transformer y validamos que existan los datos que el tranformer devuelve para tomar como valido ese procesamiento
        si = False
        word = word_tokenize(av.asesor)
        av.asesor='|'.join(word)
        words = word_tokenize(statement.text.lower())
        pos=statement.text.find(':00')
        if(pos!=-1):
            av.hora=(statement.text[pos-2:pos])
        else:
            av.hora='nan'
        
        if(av.data.lower().find(av.dia)==-1):
            av.dia=''
        else:
            si=True
        if(av.dia==''):
            for i in db.lista_dias:
                if(av.data.lower().find(i)!=-1):
                    av.dia=i
                    break
                else:
                    av.dia=''
        for i in db.list_materias:
            if(av.data.lower().find(i.lower())!=-1):
                av.asignatura=i
                si = True
                break
            else:
                av.asignatura=''
        asesor=veryfi(word,words)
        if(asesor):
            return True
        else:
            if(si):
                print("puedo procesar Trans: true")
                av.asesor=''
                if(av.asesor==''and av.asignatura==''and av.dia==''):
                    return False
                return True
            return False
    
    def process(self, input_statement, additional_response_selection_parameters):##funcion donde se toman las deciciones, tomando en cuenta lo que el transformer regreso
        #print(db.data)
        a,b,c=t.today()
        text=''
        if(av.asesor==''):
            if(av.Aasesor!=''):
                av.asesor=av.Aasesor
        if(av.dia==''):
            if(av.Adia!=''):
                av.dia=av.Adia
        if(av.hora==''):
            if(av.Ahora!=''):
                av.hora=av.Ahora
        if(av.asignatura==''):
            if(av.Aasignatura!=''):
                av.asignatura=av.Aasignatura
        #av.asesor=''
        li='Hola buen dia '+av.nombreDestino+'.\nSelecciona el horario que mejor te convenga.'
        if(av.asesor=='' and av.dia=='' and av.asignatura ==''):
            response_statement = Statement(text="Favor de verificar su eleccion de asesoria")
            return response_statement
        if(av.asignatura!='' and av.asesor==''):
            for i in range(len(db.data)):
                for j in db.data.iloc[i]['Materias']:
                    if(j.find(av.asignatura)!=-1 or j=='any'or j.find('financie')!=-1):
                        ad=(db.data.iloc[i,[5,2,3]])
                        if(ad['Dias']!=['nan']):
                            li=li+'\n\n'+ad.to_string()
                        continue
            li=li+'\n\nSelecciona el horario que mejor te convenga.'+"\nFavor de introducir una Hora valida en formato de 24 horas.\nEjemplo: fernando gomez Martes a las 15:00"
            DF.writeData('',av.destino,'','',av.asignatura)
            response_statement = Statement(text=li)
            return response_statement
        data=db.data.loc[db.data['nombre'].str.contains(av.asesor,case=False,regex=True)]
        av.asesor=data['Nombre'].to_string().split('    ')[-1]
        correoAsesor=data['Correo'].to_string().split(' ')[-1]
        dias=data['Dias'].to_list()[0]
        horas=data['Horario'].to_list()[0]
        print('asignatura',av.asignatura)
        if(av.dia==''and av.hora=='nan' and av.asignatura!=''):
            aux=data['Materias'].to_list()[0]
            for i in aux:
                if(i=='any' or i==av.asignatura):
                    DF.writeData(av.asesor,av.destino,'','',av.asignatura)
                    response_statement = Statement(text="Te recordamos que el horario de "+ av.asesor+ "  es el siguiente:\n"+data.iloc[0,[2,3]].to_string() +'\n\nSelecciona el horario que mejor te convenga.'+"\nFavor de introducir una Hora valida en formato de 24 horas.\nEjemplo: fernando gomez Martes a las 15:00"+ av.casoError)
                    return response_statement
                else:
                    li='Estos son los profesores que pueden impartir asesorias de '+av.asignatura+':'
                    for i in range(len(db.data)):
                        for j in db.data.iloc[i]['Materias']:
                            if(av.asignatura==j or j=='any'or j.find('financie')!='-1'):
                                ad=(db.data.iloc[i,[5,2,3]])
                                if(ad['Dias']!=['nan']):
                                    li=li+'\n\n'+ad.to_string()
                                break
                    li=li+'\n\nSelecciona el horario que mejor te convenga.'+"\nFavor de introducir una Hora valida en formato de 24 horas.\nEjemplo: fernando gomez Martes a las 15:00"+av.casoError
                    DF.writeData('',av.destino,'','',av.asignatura)
                    response_statement = Statement(text=li)
                    return response_statement
        print("def proc case 2")
        numericDay=t.strDaytoInt(av.dia)
        if(numericDay==None):
            DF.writeData(av.asesor,av.destino,'','',av.asignatura)
            response_statement = Statement(text="Porfavor verifica el dia ingresado ya que no se pudo identificar correctamente."+av.casoError)
            return response_statement
        deltaday = t.sumday(a,numericDay)
        tam=len(dias)
        if(deltaday==0):
            deltaday=deltaday+7
            #DF.writeData(av.asesor,av.destino,'','',av.asignatura)
            #response_statement = Statement(text="Te recordamos que el periodo minimo para agendar una asesorias debe ser mayor a 24 horas"+av.casoError)
            #return response_statement
        if(av.hora=='nan'):
            #create func to return horario
            DF.writeData(av.asesor,av.destino,'',av.dia,av.asignatura)
            response_statement = Statement(text="\nFavor de introducir una Hora valida en formato de 24 horas.\nEjemplo: fernando gomez Martes a las 15:00"+"\n\nTe recordamos que el horario de "+ av.asesor+ "  es el siguiente:\n"+data.iloc[0,[2,3]].to_string() +'\n\nSelecciona el horario que mejor te convenga.' +av.casoError)
            return response_statement
        hour=False
        equal=False
        day=False
        age=False
        for i in range(tam):
            hour=False
            equal=False
            day=False
            if(dias[i].find('nan')!=-1):
                response_statement = Statement(text="Favor de contactar al prof: "+av.asesor+"\nAl Correo: "+correoAsesor+'\n\nGracias por usar el CAM para agendar asesorias'+av.casoError)
                return response_statement
            if(av.dia.find(dias[i])!=-1):
                day=False
                equal=False
                hour=False
                for j in range(tam):
                    hour=False
                    equal=False
                    if(j!=i):
                        continue
                    inicio=int(horas[j].split('-')[0])
                    final=int(horas[j].split('-')[1])
                    if(inicio<=int(av.hora) and int(av.hora)<final):
                        a=t.today00()
                        delinicio=datetime.timedelta(days=deltaday,hours=(int(av.hora)))
                        delfinal=datetime.timedelta(days=deltaday,hours=(int(av.hora)+1))
                        if(agendar.verificar(a+delinicio,a+delfinal,correoAsesor)):
                            age=True
                            DF.removedata(av.destino)
                            print("agenda success")
                            agendar.crea_evento(a+delinicio,agendar.summary,agendar.hour,correoAsesor+','+av.destino,agendar.description,agendar.lugar)
                            response_statement = Statement(text="Su asesoria ha sido realizada con exito, favor de confirmar su asistencia por medio de correo de invitacion a Google Meet."+av.CasoSucces+"\n\nGracias por Solicitar una asesoria en el CAM")
                            return response_statement
                        else:
                            hour=True
                    else:
                        equal=True
            else:
                day=True
            if(age):
                break
        if(hour):
            DF.writeData(av.asesor,av.destino,'',av.dia,av.asignatura)
            response_statement = Statement(text="La hora seleccionada no esta disponible para la asesoria. elije otra hora diferente"+av.casoError)
            return response_statement 
        if(equal):
            DF.writeData(av.asesor,av.destino,'',av.dia,av.asignatura)
            response_statement = Statement(text="El profesor no esta disponible para impartir asesorias en la hora seleccionada"+av.casoError)
            return response_statement
        if(day):
            DF.writeData(av.asesor,av.destino,'','',av.asignatura)
            response_statement = Statement(text="El profesor no esta disponible para impartir asesorias en el dia seleccionado"+av.casoError)
            return response_statement 
        
        response_statement = Statement(text="Su asesoria ha sido realizada con exito, favor de confirmar su asistencia por medio de correo de invitacion a Google Meet."+av.CasoSucces+"\n\nGracias por Solicitar una asesoria en el CAM")
        return response_statement