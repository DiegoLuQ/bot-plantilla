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
def ButtonImage_Message(number, body, footer, options):
    
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
                    "link": "https://dinahosting.com/blog/upload/2022/07/tamanos-imagenes-redes-sociales-2024_dinahosting.png"
                }
            },
            "body": {
                "text": body 
            },
            "footer": {
                "text": footer
            },
            "action": {
                "buttons": [
                {
                    "type": "reply",
                    "reply": {
                        "id": "unique-postback-id-2",
                        "title": "Instagram"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                        "id": "unique-postback-id-1",
                        "title": "Facebook"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                        "id": "unique-postback-id-3",
                        "title": "TikTok"
                    }
                }
            ]
            }
        }
    })
    return data
def contact_Message(number):
    data = json.dumps({
    "messaging_product": "whatsapp",
    "to": number,
    "type": "contacts",
    "contacts": [
        {
            "addresses": [
                {
                    "street": "Por redes sociales",
                    "city": "Iquique",
                    "state": "Alto Hospicio",
                    "country": "Chile",
                    "type": "HOME"
                }
            ],
            "birthday": "1963-07-25",
            "emails": [
                {
                    "email": "santiago@santiagofiltros.cl",
                    "type": "WORK"
                }
            ],
            "name": {
                "first_name": "Santiago",
                "last_name": "Luque",
                "formatted_name": "Santiago Luque"
            },
            "org": {
                "company": "Santiago Filtros",
                "department": "Ventas",
                "title": "Vendedor"
            },
            "phones": [
                {
                    "phone": "+56 98173 2415",
                    "wa_id": "56981732415",
                    "type": "WORK" #"<HOME|WORK>"
                }
            ],
            "urls": [
                {
                    "url": "https://www.instagram.com/santiagofiltros/",
                    "type": "WORK"
                }
            ]
        }
        #PARA ENVIAR OTRO CONTACTO
        # {
        #     "addresses": [
        #         {
        #             "street": "Por redes sociales",
        #             "city": "Iquique",
        #             "state": "Alto Hospicio",
        #             "country": "Chile",
        #             "type": "HOME"
        #         }
        #     ],
        #     "birthday": "1963-07-25",
        #     "emails": [
        #         {
        #             "email": "santiago@santiagofiltros.cl",
        #             "type": "WORK"
        #         }
        #     ],
        #     "name": {
        #         "first_name": "Santiago",
        #         "last_name": "Luque",
        #         "formatted_name": "Santiago Luque"
        #     },
        #     "org": {
        #         "company": "Santiago Filtros",
        #         "department": "Ventas",
        #         "title": "Vendedor"
        #     },
        #     "phones": [
        #         {
        #             "phone": "+56 98173 2415",
        #             "wa_id": "56981732415",
        #             "type": "WORK" #"<HOME|WORK>"
        #         }
        #     ],
        #     "urls": [
        #         {
        #             "url": "https://www.instagram.com/santiagofiltros/",
        #             "type": "HOME"
        #         }
        #     ]
        # }
    ]
})
    return data
def textUrl_Message(number):
    data = json.dumps({
    "messaging_product": "whatsapp",
    "to": number,
    "text": {
        "preview_url": True,
        "body": "Claro que si!, Visitanos en https://linaresupp.cl para ayudarte en tu negocio, no dudes en llamarnos!"
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
def listaDeOpciones_Message(number):
    data = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": number,
    "type": "interactive",
    "interactive": {
        "type": "list",
        "header": {
            "type": "text",
            "text": "Listado de Categorias"
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
                    "title": "Filtro de aire 🍃",
                    "rows": [
                        {
                            "id": "aire-identifier1",
                            "title": "F. Aire PDF",
                            # "description": "row-description-content"
                        },
                        {
                            "id": "aire-identifier2",
                            "title": "F. Aire WEb",
                            # "description": "row-description-content"
                        }
                    ]
                },
                {
                    "title": "Filtro de Combustible ⛽",
                    "rows": [
                        {
                            "id": "combustible-identifier1",
                            "title": "F. Combustible PDF ",
                            # "description": "row-description-content"
                        },
                        {
                            "id": "combustible-identifier2",
                            "title": "F. Combustible WEb",
                            # "description": "row-description-content"
                        }
                    ]
                },
                {
                    "title": "Filtro de aceite 🏁",
                    "rows": [
                        {
                            "id": "aceite-identifier1",
                            "title": "F. Aceite PDF",
                            # "description": "row-description-content"
                        },
                        {
                            "id": "aceite-identifier2",
                            "title": "F. Aceite Web",
                            # "description": "row-description-content"
                        }
                    ]
                },
                
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
def catalgoWSP_Message(number):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "catalog_message",
                "body": {
                    "text": "Hello! Thanks for your interest. Ordering is easy. Just visit our catalog and add items to purchase."
                },
                "action": {
                    "name": "catalog_message",
                    "parameters": {
                        "thumbnail_product_retailer_id": "svtr266tw9"
                    }
                },
                "footer": {
                    "text": "Best grocery deals on WhatsApp!"
                }
            }
        }
    )
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
def mostrar_menu(number, messageId, body, footer, options, sed):
    
    replyButton_Data = buttonReply_Message(
        number, options, body, footer, "sed"+sed, messageId)
    # list_for.append(replyButton_Data)
    return replyButton_Data

async def administrar_chatbot(text, number, messageId, name, timestamp):
    text = text.lower()
    print(f"Mensaje del usuario {name}:", text)
    lista_privada = ["hola", "admin"]
    list_for = []

    if text in "hola":
        body = "Hola!, Bienvenido a SoporteSF. Navega por nuestras opciones"
        footer = "Equipo SF"
        options  = ["Catalogo", "Información", "Inicia tu Negocio"]
        data = mostrar_menu(number, messageId, body, footer, options, sed="1")
        list_for.append(data)
    #CATALOGO
    elif text in "catalogo":
        body = "Buena elección para revisar nuestros productos, te dejo aquí unas opciones"
        footer = "Productos SF"
        options  = ["Descargar PDF", "Lista de Productos", "Catalogo WSP"]
        data = mostrar_menu(number, messageId, body, footer, options, sed="2")
        list_for.append(data)
    elif text in "descargar pdf":
        data = document_Message(number, str(sett.doc_pdf), "PDF de nuestros filtros", "Filtros - SF")
        list_for.append(data)
    elif text in "lista de productos":
        data = listaDeOpciones_Message(number)
        list_for.append(data)    
    
    #Información
    elif text in "información":
        body = "Quieres saber más de nosotros?, te dejo aquí unas opciones"
        footer = "Información SF"
        options  = ["Ubicación?", "Redes Sociales", "Tienen pagina web?"]
        data = mostrar_menu(number, messageId, body, footer, options, sed="2")
        list_for.append(data)
    elif text in "redes sociales":
        data = ButtonImage_Message(number, 
                                   body="Te presento nuestras redes sociales, no olvides seguirnos para enterarte de ofertas y promociones del día", 
                                   footer="SF | Redes Sociales - FIX", 
                                   options=[])
        list_for.append(data)
    elif text in "ubicación?":
        data = location_Message(number, messageId)
        list_for.append(data)
        
    elif text in "tienen pagina web?":
        data = textUrl_Message(number)
        list_for.append(data)
    
    #Inicia tu negocio
    elif text in "inicia tu negocio":
        body = "Emprende junto a nostros! 🤟, te dejo aquí unas opciones"
        footer = "Emprendiendo con SF"
        options  = ["Contactar vendedor", "Tu primer negocio", "Consejos Utiles"]
        data = mostrar_menu(number, messageId, body, footer, options, sed="3")
        list_for.append(data) 
    elif text in "contactar vendedor":
        data = contact_Message(number)
        list_for.append(data)       
        
        
    elif text in "ok":
        data = text_Message(number, "Gracias por contactarse con nosotros")
        list_for.append(data)
        
    elif text in "como es el local?":
        data = Image_Message(number)
        list_for.append(data)


    

    else:
            body = "Hola. ¿Quieres que te ayude con alguna de estas opciones?"
            footer = "Equipo SF"
            options = ["✅ productos", "📅 agendar cita"]
            list_for.append(body)
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed7", messageId)
            list_for.append(replyButtonData)
    return await enviar_mensaje_usuario(list_for)