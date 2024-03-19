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
        # print(data)
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
def ButtonImage_Message(number, body, footer):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type":  "image",
                "image": {
                    "link": "https://i.postimg.cc/4xzJdjY2/Personal-Portafolio.jpg"
                }
            },
            "body": {
                "text": body 
            },
            "footer": {
                "text": "Marca Kendall - SF"
            },
            "action": {
                "buttons": [
                {
                    "type": "reply",
                    "reply": {
                        "id": "unique-postback-id-2",
                        "title": "Agregar a carrito"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                        "id": "unique-postback-id-1",
                        "title": "buscar producto"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                        "id": "unique-postback-id-3",
                        "title": "revisar en web"
                    }
                }
            ]
            }
        }
    })
    return data
def textUrl_Message(number):
    data = json.dumps({
    "messaging_product": "whatsapp",
    "to": number,
    "text": {
        "preview_url": True,
        "body": "Please visit https://linaresupp.cl to inspire your day!"
    }
})
    return data
def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def location_Message(number, messageId):
    data = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": number,
    "context": {
        "message_id": messageId
    },
    "type": "location",
    "location": {
        "latitude": -20.273872272525107,
        "longitude": -70.09637463862305,
        "name": "Santiago Filtros",
        "address": "Argentina 3086"
    }
    , 
})
    return data
def listImage_Message(number):
    data = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": number,
    "type": "interactive",
    "interactive": {
        "type": "list",
        "header": {
            "type": "text",
            "text": "Filtros en Promocion"
        },
        "body": {
            "text": "30% de Descuento"
        },
        "footer": {
            "text": "SF | Tu vendedor de confianza"
        },
        "action": {
            "button": "Ver productos",
            "sections": [
                {
                    "title": "Filtro de aire",
                    "rows": [
                        {
                            "id": "unique-row-identifier1",
                            "title": "row-title-content",
                            "description": "row-description-content"
                        }
                    ]
                },
                {
                    "title": "Filtro de aceite",
                    "rows": [
                        {
                            "id": "unique-row-identifier2",
                            "title": "row-title-content",
                            "description": "row-description-content"
                        }
                    ]
                }
            ]
        }
    }
})
    return data
def Image_Message(number):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "to": number,
        "type": "image",
        "image": {
            "link": "https://i.postimg.cc/4xzJdjY2/Personal-Portafolio.jpg"
        }
    })
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
    options  = ["📟 Enviar PDF", "🔎 visitar web", "🔄 actualizar ticket"]
    replyButton_Data = buttonReply_Message(
        number, options, body, footer, "sed1", messageId)
    # list_for.append(replyButton_Data)
    return replyButton_Data

async def administrar_chatbot(text, number, messageId, name, timestamp):
    text = text.lower()
    print(f"Mensaje del usuario {name}:", text)
    lista_privada = ["hola", "admin"]
    list_for = []

    if text in "hola":
        data = mostrar_menu_principal(number, messageId)
        list_for.append(data)
    elif text in "ok":
        data = text_Message(number, "Gracias por contactarse con nosotros")
        list_for.append(data)
        
    elif text in "enviar pdf":
        data = document_Message(number, str(sett.doc_pdf), "PDF de nuestros filtros", "Filtros - SF")
        list_for.append(data)
    elif text in "como es el local?":
        data = Image_Message(number)
        list_for.append(data)
    elif text in "visitar web":
        data = textUrl_Message(number)
        list_for.append(data)
    elif text in "lista imagenes":
        data = listImage_Message(number)
        list_for.append(data)
    elif text in "donde estan ubicados?":
        data = location_Message(number, messageId)
        list_for.append(data)
    else:
            body = "Hola. ¿Quieres que te ayude con alguna de estas opciones?"
            footer = "Equipo SF"
            options = ["✅ productos", "📅 agendar cita"]
            list_for.append(body)
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed7", messageId)
            list_for.append(replyButtonData)
    return await enviar_mensaje_usuario(list_for)