##api para el manejo de los tiempos 


#Cargamos la biblioteca
import datetime

def dstri(day):##funcion entra un numero del 1-7 y devuelve el nombre del dia de la semana iniciando por el lunes
    dayStr =''
    if day == 1:
        dayStr = 'lunes'
    elif day == 2:
        dayStr = 'martes'
    elif day == 3:
        dayStr = 'miercoles'
    elif day == 4:
        dayStr = 'jueves'
    elif day == 5:
        dayStr = 'viernes'
    elif day == 6:
        dayStr = 'sabado'
    elif day == 7:
        dayStr ='domingo'
    else:
        dayStr = 'nan'
    return dayStr

def today():##funcion para obtener el dia de hoy, retorna una variable datatime, un numero de dia, y el nombre del dia de hoy
    dt =  datetime.datetime.today()
    aux=datetime.datetime(dt.year, dt.month, dt.day)
    day = aux.weekday()+1
    dayStr =dstri(day)
    return aux, day,dayStr

def sumday(t,diaDest):##verifica cuantos dias hay entre 2 dias dados
    aux = t.weekday()+1
    i = 0
    while(aux != diaDest):
        aux=(aux+1)%7
        i=i+1
    return i

def strDaytoInt(daystr):#convierte un nombre a numero de dia entre el 1 y 7
    if(daystr.find('lunes')!=-1):
        return 1
    elif(daystr.find('martes')!=-1):
        return 2
    elif(daystr.find('miercoles')!=-1):
        return 3
    elif(daystr.find('jueves')!=-1):
        return 4
    elif(daystr.find('viernes')!=-1):
        return 5
    elif(daystr.find('sabado')!=-1):
        return 6
    elif(daystr.find('domingo')!=-1):
        return 7
    else:
        return None
def today00():#regresa una variable de tipo datetime del dia actal
    dt =  datetime.datetime.today()
    aux=datetime.datetime(dt.year, dt.month, dt.day)
    return aux