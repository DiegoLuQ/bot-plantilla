import os
import json
import httpx
from config import settings as sett
from uuid import uuid4
import asyncio

async def ObtenerIdImagen(image_id):
    url = f"https://graph.facebook.com/v19.0/{image_id}"
    whatsapp_token = sett.wsp_token
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {whatsapp_token}"}
        response = await client.get(url, headers=headers)
        data_json = response.json()
        imagen_url = data_json['url']
        return imagen_url


async def descargar_imagen(url, number):
    print(url)
    whatsapp_token = sett.wsp_token
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {whatsapp_token}"}
        # la url es la url que obtenemos del json de ObtenerIdImagen
        response = await client.get(url, headers=headers)
        # Guardar la imagen en un archivo local
        nombre_archivo = f"{number}_{uuid4()}.jpg"
        ruta_carpeta = os.path.join("imagenes")
        # Crear la carpeta si no existe
        os.makedirs(ruta_carpeta, exist_ok=True)
        # Guardar la imagen en la carpeta
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        with open(ruta_completa, "wb") as f:
            f.write(response.content)


async def sumar_total_pedido(product_items):
    total = 0
    for item in product_items:
        total += item['item_price'] * item['quantity']
    return total


async def procesar_orden(order):
    total_pedido = await sumar_total_pedido(order['product_items'])
    return f'Orden recibida. Total del pedido: {total_pedido} {order["product_items"][0]["currency"]}'


async def sendImage_Message(number, link, caption):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "image",
        "image": {
            "link": link,
            "caption": caption
        }
    })
    return data

async def buttonReply_Message(number, options, body, footer, sedd, messageId):
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


async def ButtonImage_Message(number, body, footer, options, url_img):
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


async def contact_Message(number):
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


async def textUrl_Message(number):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "to": number,
        "text": {
            "preview_url": True,
            "body": "Claro que si!, Visitanos en https://santiagofiltros.cl para ayudarte en tu negocio, no dudes en llamarnos!"
        }
    })
    return data


async def document_Message(number, url, caption, filename):
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


async def location_Message(number, messageId):
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


async def ClientLocation_Message(number, body):

    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "type": "interactive",
        "to": number,
        "interactive": {
            "type": "location_request_message",
            "body": {
                "text": body
            },
            "action": {
                "name": "send_location"
            }
        }
    })

    return data

async def catalogo_Message():
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


async def catalgoWSP_Message(number, body, footer):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "catalog_message",
                "body": {
                    "text": body
                },
                "action": {
                    "name": "catalog_message",
                    "parameters": {
                        "thumbnail_product_retailer_id": "svtr266tw9"
                    }
                },
                "footer": {
                    "text": footer
                }
            }
        }
    )
    return data


async def preparar_mensajes(numero, messageId):
    mensajes = ["¡Estamos encantados de darte la bienvenida a nuestra comunidad de clientes! Es un placer tenerte con nosotros en tu primera compra. 😊",
                        "Queremos que sepas que ofrecemos una diversidad de opciones para asegurarnos de que encuentres exactamente lo que necesitas, adaptándonos a todo tipo de presupuestos. Ya sea que busques algo económico o estés buscando invertir en productos de calidad, tenemos lo justo para ti."
                        ]
    tasks = [await text_Message(numero, mensaje, messageId) for mensaje in mensajes]
    return tasks

async def text_Message(number, text, messageId=None):
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
        },

    })
    return data


async def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data
    # {'object': 'whatsapp_business_account', 'entry': [{'id': '131989103328203',
    # 'changes': [{'value': {'messaging_product': 'whatsapp',
    # 'metadata': {'display_phone_number': '56934888609', 'phone_number_id': '130513470143872'},
    # 'contacts': [{'profile': {'name': 'JD'}, 'wa_id': '56961227637'}],
    # 'messages': [{'from': '56961227637', 'id': 'wamid.HBgLNTY5NjEyMjc2MzcVAgASGBQzQTU1QTc1REZCMkM0RTlGREE5NAA=',
    # 'timestamp': '1711930371', 'type': 'sticker',
    # 'sticker': {'mime_type': 'image/webp',
    # 'sha256': 'uwXVoi2i4wLtzkMQAP7ySI3p7MNqzU+PM/RWn1GBwO0=',
    # 'id': '381731608015965',
    # 'animated': False}
    # }]}, 'field': 'messages'}]}]}


async def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    # elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    # elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    # elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id


async def mostrar_menu(number, messageId, body, footer, options, sed):
    replyButton_Data = await buttonReply_Message(
        number, options, body, footer, "sed"+sed, messageId)
    return replyButton_Data

async def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data
