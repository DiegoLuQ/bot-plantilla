import httpx
import json
import time
from config import settings as sett
from datetime import datetime


async def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        text = 'Mensaje no reconocido'
        return text

    typeMessage = message['type']

    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']

    else:
        text = 'mensaje no reconocido'

    return text


async def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.wsp_token
        whatsapp_url = sett.wsp_url

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}

        async with httpx.AsyncClient() as client:
            response = await client.post(whatsapp_url, headers=headers, data=data)

        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            print("mensaje no enviado", response.status_code)
            print('error al enviar mensaje', response.status_code)
    except Exception as e:
        return str(e), 403

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []

    for i, option in enumerate(options):
        buttons.append({
            "type": "reply",
            "reply": {
                "id": sedd + "_btn_" + str(i+1),
                "title": option
            }
        })
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data   

def text_Message(number, text):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "body": text
        }
    })
    return data

async def enviar_mensaje_usuario(list_for):
    for item in list_for:
        await enviar_Mensaje_whatsapp(item)

def mostrar_menu_principal(number, messageId):
    body = "Hola!, Bienvenido a SoporteSF. Navega por nuestras opciones"
    footer = "Equipo SF"
    options  = ["📟 generar ticket", "🔎 ver estado ticket", "🔄 actualizar ticket"],
    replyButton_Data = buttonReply_Message(
        number, options, body, footer, "sed1", messageId)
    # list_for.append(replyButton_Data)
    return replyButton_Data

async def administrar_chatbot(text, number, messageId, name, timestamp):
    text = text.lower()
    print(f"Mensaje del usuario {name}:", text)
    lista_privada = ["hola", "admin"]
    list_for = []

    if text in lista_privada:
        data = mostrar_menu_principal(number, messageId, text)
        list_for.append(data)
        
    return await enviar_mensaje_usuario(list_for)