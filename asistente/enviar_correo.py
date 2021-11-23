##api creada para la gestion del envio de correos electronicos

#Importación de bibliotecas
from email.mime import text
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
##Esta funcion establece la coneccion con el servidor smtp de gmail
def connect_email(us,pas):
    mailServer = smtplib.SMTP('smtp.gmail.com',587) # Establecemos conexion con el servidor smtp de gmail
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(us,pas)
    return mailServer
##funcion para enviar un correo electronico
def enviar_email(mailServer,remitente,destinatario,asunto,texto):
    mensaje = MIMEText(texto)
    mensaje['From']=remitente #Enviado por
    mensaje['To']=destinatario # Remitente 
    mensaje['Subject']=asunto# Titulo del correo
    if mailServer.sendmail(remitente,destinatario,mensaje.as_string()):
        print("true")
    mailServer.quit()


#Inicialización de variables para prueba de la biblioteca
us = "matematicas@ucaribe.edu.mx"
pas = "LoremIpsum@2020"
des = "150300121@ucaribe.edu.mx"
asunto = "Prueba python"
texto = "texto de prueba para asistente virtual"

#conectar = connect_email(us,pas) #Funcion Conectar
#enviar_email(conectar,us,des,asunto,texto) #Funcion envia correo