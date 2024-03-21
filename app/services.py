import httpx
import json
import time
from asyncio import sleep
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
    elif typeMessage == 'order':
        # Llama a una función que procesa y resume la orden, esta función se debe definir
        text = message['order']

    else:
        text = 'mensaje no reconocido'

    return text


async def sumar_total_pedido(product_items):
    total = 0
    for item in product_items:
        total += item['item_price'] * item['quantity']
    return total


async def procesar_orden(order):
    total_pedido = await sumar_total_pedido(order['product_items'])
    return f'Orden recibida. Total del pedido: {total_pedido} {order["product_items"][0]["currency"]}'


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


def ButtonImage_Message(number, body, footer, options, url_img):
    id_base = "unique-postback-id-"
    accion = {
        "buttons": []
    }
# Iterar sobre la lista de títulos de botones y crear botones correspondientes
    for i, titulo in enumerate(options, start=0):
        boton = {
            "type": "reply",
            "reply": {
                "id": f"{id_base}{i}",
                "title": titulo
            }
        }
        accion["buttons"].append(boton)

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
                    "link": url_img
                }
            },
            "body": {
                "text": body
            },
            "footer": {
                "text": footer
            },
            "action": accion
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
                        "type": "WORK"  # "<HOME|WORK>"
                    }
                ],
                "urls": [
                    {
                        "url": "https://www.instagram.com/santiagofiltros/",
                        "type": "WORK"
                    }
                ]
            }
            # PARA ENVIAR OTRO CONTACTO
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
        },
    })
    return data


async def listaDeOpciones_Message(number, body_text, header_text, footer_text, button_text, opciones):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": header_text
            },
            "body": {
                "text": body_text
            },
            "footer": {
                "text": footer_text
            },
            "action": {
                "button": button_text,
                "sections": opciones

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


def catalogo_Message():
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "56961227637",
        "type": "interactive",
        "interactive": {
            "type": "catalog_message",
            "body": {
                "text": "Descubre nuestra gama de filtros para vehículos 🚗: calidad y rendimiento para mantener tu motor en óptimas condiciones. ¡Echa un vistazo ahora!"
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
    return data

# Enviar varios mensajes


def preparar_mensajes(numero, mensajes):
    return [text_Message(numero, mensaje) for mensaje in mensajes]
def text_Message(number, text, messageId = None):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "context": {
        "message_id": messageId
    },
        "type": "text",
        "text": {
            "body": text
        }
    })
    return data


def mostrar_menu(number, messageId, body, footer, options, sed):
    replyButton_Data = buttonReply_Message(
        number, options, body, footer, "sed"+sed, messageId)
    # list_for.append(replyButton_Data)
    return replyButton_Data
    return data


async def enviar_mensaje_usuario(list_for):
    for item in list_for:
        await enviar_Mensaje_whatsapp(item)
        await sleep(3)


async def administrar_chatbot(text, number, messageId, name, timestamp):
    print(type(text))
    list_for = []
    lista_privada = ["hola", "admin"]
    if type(text) == dict:
        data_text = await procesar_orden(text)
        data = text_Message(number, data_text, messageId)
        data_img = ButtonImage_Message(number,
                                       body="Aqui te envio los datos de transferencia",
                                       footer="SF | Gracias por preferirnos ♥",
                                       options=["Transferencia", "Pago en Efectivo"], url_img="https://i.postimg.cc/PJPRZJBh/e35f9d3b-f59b-44ed-91e2-e6742799baad.png")
        list_for.append(data_img)
        list_for.append(data)

    else:
        text = text.lower()
        print(f"Mensaje del usuario {name}:", text)

        if text in ["hola", "buenos dias", "buenas noches", "buenas tardes", "ola", "hello"]:
            body = "Hola, ¡bienvenido a SF! 🌟 Soy tu asistente virtual Jack 24/7, listo para resolver tus dudas. Navega por nuestro menú para explorar productos, conocer más sobre SF 📊 y descubrir cómo iniciar tu negocio con nosotros 🚀."
            footer = "Equipo SF"
            options = ["Catalogo", "Información", "Tu Negocio"]
            data = mostrar_menu(number, messageId, body,
                                footer, options, sed="1")
            list_for.append(data)
        # CATALOGO
        elif text in "catalogo":
            body = "Buena elección para revisar nuestros productos, te dejo aquí unas opciones"
            footer = "Productos SF"
            options = ["Descargar PDF", "Lista de Productos", "Catalogo WSP"]
            data = mostrar_menu(number, messageId, body,
                                footer, options, sed="2")
            list_for.append(data)
        elif text in "descargar pdf":
            data = document_Message(number, str(
                sett.doc_pdf), "PDF de nuestros filtros", "Filtros - SF")
            list_for.append(data)
 
        elif text in "Catalogo WSP":
            data = catalgoWSP_Message(number)
            list_for.append(data)
            
        elif text in "lista de productos":
            lista_opciones = [
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

            data = listaDeOpciones_Message(number, body_text="Productos de calidad, dale a tus cliente lo mejor",
                                           header_text="Listado de Filtros", footer_text="SF | Calidad y Confianza", button_text="Ver ☑️", opciones=lista_opciones)
            list_for.append(data)

        # Información
        elif text in "información":
            body = "Quieres saber más de nosotros?, te dejo aquí unas opciones"
            footer = "Información SF"
            options = ["Ubicación?", "Redes Sociales", "Tienen pagina web?"]
            data = mostrar_menu(number, messageId, body,
                                footer, options, sed="2")
            list_for.append(data)
        elif text in "redes sociales":
            data = ButtonImage_Message(number,
                                       body="Te presento nuestras redes sociales, no olvides seguirnos para enterarte de ofertas y promociones del día",
                                       footer="SF | Redes Sociales - FIX",
                                       options=["Instagram", "Facebook", "TikTok"], url_img="https://dinahosting.com/blog/upload/2022/07/tamanos-imagenes-redes-sociales-2024_dinahosting.png")
            list_for.append(data)
        elif text in "ubicación?":
            data = location_Message(number, messageId)
            list_for.append(data)

        elif text in "tienen pagina web?":
            data = textUrl_Message(number)
            list_for.append(data)

        # TU NEGOCIO
        elif text in "tu negocio":
            body = "Emprende junto a nostros! 🤟, te dejo aquí unas opciones"
            footer = "Emprendiendo con SF"
            options = ["Contactar vendedor",
                       "Tu primer negocio",
                       "Consejos Utiles"]
            data = mostrar_menu(number, messageId, body,
                                footer, options, sed="3")
            list_for.append(data)
        elif text in "contactar vendedor":
            data = contact_Message(number)
            list_for.append(data)

        # TU PRIMER NEGOCIO
        elif text in "tu primer negocio":
            data_img = ButtonImage_Message(number,
                                           body="Tu primer negocio junto a SF | Confianza y Calidad",
                                           footer="SF | Gracias por preferirnos ♥",
                                           options=[
                                               "Soy Cliente", "Primera Compra", "Ayuda PDF"],
                                           url_img="https://i.postimg.cc/PJPRZJBh/e35f9d3b-f59b-44ed-91e2-e6742799baad.png")
            list_for.append(data_img)

        elif text in "soy cliente":
            pass
        elif text in "primera compra":
            mensajes = ["¡Estamos encantados de darte la bienvenida a nuestra comunidad de clientes! Es un placer tenerte con nosotros en tu primera compra. 😊",
                        "Queremos que sepas que ofrecemos una diversidad de opciones para asegurarnos de que encuentres exactamente lo que necesitas, adaptándonos a todo tipo de presupuestos. Ya sea que busques algo económico o estés buscando invertir en productos de calidad, tenemos lo justo para ti."
                        ]
            list_for.extend(preparar_mensajes(number, mensajes))
            lista_opciones = [
                {
                    "title": "¿Cuál es tu presupuesto?",
                    "rows": [
                        {
                            "id": "presupuesto1",
                            "title": "CLP 100.000 - 300.000",
                            # "description": "row-description-content"
                        },
                        {
                            "id": "presupuesto2",
                            "title": "CLP 300.001 - 500.000",
                            # "description": "row-description-content"
                        },
                        {
                            "id": "presupuesto3",
                            "title": "CLP 500.001 - 700.000",
                            # "description": "row-description-content"
                        },
                        {
                            "id": "presupuesto4",
                            "title": "CLP 700.001 - XXX.XXX",
                            # "description": "row-description-content"
                        }
                    ]
                }
            ]
            data = await listaDeOpciones_Message(number, header_text="Presupuestos PREDETERMINADOS 🤟",
                                                 body_text="Selecciona el rango de compra 🛒 que mejor se ajusta a tus necesidades y te facilitaremos un PDF 📄 detallado para tu consulta. Este documento está diseñado con filtros específicos 🔍 para adaptarse a las particularidades de tu negocio 🏭, asegurando que encuentres exactamente lo que buscas de manera eficiente 💼.",
                                                 footer_text="SF | Calidad y Confianza", button_text="Ver Presupuestos 😎", opciones=lista_opciones)
            list_for.append(data)

        elif text in "CLP 100.000 - 300.000":
            data = text_Message(number, "Descubre cómo tu negocio puede beneficiarse de nuestra selección de filtros con precios especiales al por mayor, ideales para pequeñas empresas o talleres que están comenzando. Al elegir esta opción, recibirás un PDF detallado con una propuesta de precios diseñada para optimizar tu inversión inicial.", messageId)
            list_for.append(data)
            
        elif text in "CLP 300.001 - 500.000":
            data = text_Message(number, "Para empresas en crecimiento, ofrecemos un rango de precios competitivos que se ajusta a tus necesidades de expansión. Seleccionando este nivel, te enviaremos un PDF con una estructura de precios al por mayor que te permitirá escalar tu negocio manteniendo un equilibrio entre calidad y coste.", messageId)
            list_for.append(data)
            
        elif text in "CLP 500.001 - 700.000":
            data = text_Message(number, "Empresas establecidas encontrarán en este rango una oportunidad para fortalecer su cadena de suministro con nuestros filtros de alto rendimiento a precios preferenciales. El PDF que recibirás como parte de esta opción refleja una estrategia de precios pensada para socios comprometidos con la calidad y la eficiencia.", messageId)
            list_for.append(data)
        
        elif text in "CLP 700.001 - XXX.XXX":
            data = text_Message(number, "Dirigido a líderes de la industria y grandes flotas, este rango ofrece el mejor valor con precios exclusivos al por mayor para pedidos de gran volumen. Al optar por esta categoría, el PDF proporcionado incluirá una oferta personalizada que reconoce y recompensa tu inversión y fidelidad a largo plazo con SF.", messageId)
            list_for.append(data)

        # OTROS MENSAJES
        elif text  in "gracias":
            data = text_Message(number, "Estamos para ayudarte 🤓", messageId)
            list_for.append(data)
            
        elif text  in ["chao", "hasta luego"]:
            data = text_Message(number, "Estamos para ayudarte 🤓", messageId)
            list_for.append(data)
                
        elif text in "ok":
            data = text_Message(number, "😎", messageId)
            list_for.append(data)

        elif text in "como es el local?":
            data = Image_Message(number)
            list_for.append(data)

        else:
            body = "Hola. ¿Quieres que te ayude con alguna de estas opciones?"
            footer = "Equipo SF"
            options = ["✅ productos", "📅 agendar cita"]
            list_for.append(body)
            replyButtonData = buttonReply_Message(
                number, options, body, footer, "sed7", messageId)
            list_for.append(replyButtonData)
    return await enviar_mensaje_usuario(list_for)
