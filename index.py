from flask import Flask, request
import json
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
 
#Creamos objeto Flask
app = Flask(__name__)
 
#Cargamos la informacion de nuestro archivo config.json
f = open("config.json", "r")
env = json.loads(f.read())
 
#Creamos nuestro primer servicio web
@app.route('/test', methods=['GET'])
def test():
    return "hello world"

@app.route('/send_sms', methods=['POST'])
def send_sms():
    try:
        #variables de configuracion
        account_sid = env['TWILIO_ACCOUNT_SID']
        auth_token = env['TWILIO_AUTH_TOKEN']
        origen = env['TWILIO_PHONE_NUMBER']
        #valida cuenta de twilio
        client = Client(account_sid, auth_token)
        #captura datos de la solicitud
        data = request.json
        contenido = data["contenido"]
        destino = data["destino"]
        #envia mensaje
        message = client.messages.create(
                            body=contenido,
                            from_=origen,
                            to='+57' + destino
                        )
        print(message)
        return "send success"
    except Exception as e:
        print(e)
        return "error"

@app.route('/send_email', methods=['POST'])
def send_email():
    #capturo los datos
    data = request.json
    contenido = data["contenido"]
    destino = data["destino"]
    asunto = data["asunto"]
    print(contenido, destino, asunto)
    #creo el mensaje a enviar
    message = Mail(
    from_email= env['SENDGRID_FROM_EMAIL'],
    to_emails= destino,
    subject= asunto,
    html_content= contenido)
    try:
        #configuro el aipkey y envio mensaje
        sg = SendGridAPIClient(env['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "send success"
    except Exception as e:
        print(e)#.message
        return "error"

#Ejecutamos el servidor
if __name__ == '__main__':
    app.run()
