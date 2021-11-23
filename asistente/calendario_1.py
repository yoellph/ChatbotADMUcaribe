#api calendario


#importamos las biblotecas necesarioas para esta api
import re
import socket
from ssl import SSLCertVerificationError
from threading import Event
from google.auth.credentials import ReadOnlyScoped
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datefinder
import pprint
import json
from uuid import uuid4
import funtime as t
import rfc3339

##descomentar para generar el token json
""" Crear token

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
credentials = flow.run_console()
pickle.dump(credentials, open("token.pkl", "wb")) 

"""

def get_date_string(date_object):#convierte una variable tipo datetime to rfc3339
  return rfc3339.rfc3339(date_object)

def busca_asesorias():#Funcion que busca en el calendario si existe una sesion de asesoria a una hora especifica
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    result = service.calendarList().list().execute()
    calendar_id = result['items'][0]['id']
    result = service.events().list(calendarId=calendar_id).execute()
    return service

def enlista_asesorias(service,ahora, hour):##lista asesorias encontradas
     # Call the Calendar API
    now = ahora#.isoformat()  + 'Z' # 'Z' indicates UTC time
    future =  hour
    future = get_date_string(future)
    now = get_date_string(now)#.isoformat() + 'R'
    print(now)
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=future,singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return None
    li=[]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        li.append(event['attendees'])
    return li


def crea_evento(start_time, summary, duration=1,attendees=None, description=None, location=None):##crea el evento asesoria
    service = busca_asesorias()
    start_time = start_time
    end_time = start_time + datetime.timedelta(hours=duration)
    attendees = attendees.split(",")

    att = []
    att.append({'email': 'matematicas@ucaribe.edu.mx'})
    
    for a in range(0,len(attendees)): 
        att.append({'email': attendees[a] })
    attendees = att
    id = f"{uuid4().hex}"
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Cancun',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Cancun',
        },
        'attendees': attendees,

        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        "conferenceData": {"createRequest": {"requestId": id,
                                                      "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
    }
    return service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1,sendNotifications=True).execute()

hour = 1
fecha = '07 Nov 11:00am'
summary = "Asesoria de prueba creada por el asistente virtual "
duration = 1
participantes = "150300121@ucaribe.edu.mx,150300088@ucaribe.edu.mx"
description =  "Esto es una prueba"
lugar = "Universidad del caribe"

##crea_evento(fecha,summary,duration,participantes,description,lugar)
#

def verificar(inicio,final,correo):##verifica si existe una asesoria
    service = busca_asesorias()
    lista_eventos = enlista_asesorias(service,inicio, final)
    if(lista_eventos==None):
        return True
    for i in lista_eventos:
        print(json.dumps(i).find(correo))
        if(json.dumps(i).find(correo)!=-1):
            return False
    return True

