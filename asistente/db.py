#variables donde almacenamos los profesores y materias.
import pandas as pd


datos = {
    'nombre':['eugenio guerrero ruiz','hector fernando gomez garcia','victor romero ','jose enrique alvarez estrada','juan diego canul chale','omar mejenes sanchez','jarmen said virgen suarez','leslye johanna ramirez carmona'],
    'Correo':['eguerrero@ucaribe.edu.mx','fgomez@ucaribe.edu.mx','vromero@ucaribe.edu.mx','jeae@ucaribe.edu.mx','jcanul@ucaribe.edu.mx','omejenes@ucaribe.edu.mx','jvirgen@ucaribe.edu.mx','lramirez@ucaribe.edu.mx'],
    'Horario':[['19-20','12-13','17-19'],['16-18'],['13-14'],['15-16','15-16'],['9-11'],['13-15'],['13-14'],['16-17']],
    'Dias':[['lunes','miercoles','miercoles'],['martes'],['martes'],['martes','jueves'],['miercoles'],["viernes"],['lunes'],['viernes']],
    'Materias':[['any'],['any'],['calculo integral','calculo diferencial','propedeutico de matematicas'],['matematicas discretas','propedeutico de matematicas'],['calculo diferencial','calculo integral','propedeutico de matemticas','ecuaciones diferenciales','probabilidad y estadistica','estadistica analitica','calculo vectorial'],['calculo diferencial','calculo integral','propedeutico de matemticas','ecuaciones diferenciales','calculo vectorial','matematicas discretas'],['calculo diferencial','calculo integral','propedeutico de matemticas','matematicas discretas'],['calculo diferencial','calculo integral','propedeutico de matemticas','calculo vectorial','matematicas discretas']],
    'Nombre':['Eugenio Guerrero Ruiz','Hector Fernando Gomez Garcia','Víctor Romero ','José Enrique Alvárez Estrada','Juan Diego Canul Chale','Omar Mejenes Sánchez','Jarmen Said Virgen Suarez','Leslye Johanna Ramirez Carmona']
}

data = pd.DataFrame(datos)
list_materias = ['calculo integral','calculo diferencial','calculo vectorial','ecuaciones diferenciales','propedeutico de matematicas','matematicas discretas','matematicas financieras','probabilidad y estadistica','estadistica analitica','propedéutico de matemáticas']
lista_dias = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo','mañana','hoy']

