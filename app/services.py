import httpx
import json
from config import settings as sett
from whatsapp_messaging import *
from asyncio import sleep


async def guardar_datos_db(data):
    try:
        # print(data)
        headers = {'Content-Type': 'application/json'}

        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8001/v1/user_wsp/register_user", headers=headers, data=data)

        if response.status_code == 200:
            return 'mensaje guardado', 200
        else:
            print('error al guardar mensaje', response.status_code)
    except Exception as e:
        return str(e), 403


async def enviar_Mensaje_whatsapp(data):
    try:
        # print(data)
        whatsapp_token = sett.wsp_token
        whatsapp_url = sett.wsp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}

        async with httpx.AsyncClient() as client:
            response = await client.post(whatsapp_url, headers=headers, data=data)
        print(response.status_code)
        if response.status_code == 200:
            print('mensaje guardado', 200)
            return 'mensaje guardado', 200
        else:
            print("mensaje no enviado", response)
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return str(e), 403


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
        print(text)
    elif typeMessage == 'location':
        text = "Ubicación"
    elif typeMessage == 'image':
        text = message['image']
    else:
        text = 'mensaje no reconocido'

    return text


async def bloquear_usuario(text, number, messageId, name, timestamp):
    list_for = []

    async def Enviar_Saludo_Bloqueo():
        body = "Disculpa🙏, parece que estoy un poco abrumado 🥱 por la cantidad de mensajes. Permíteme tomar un breve descanso de 30 segundos ⏳ para reorganizarme y estaré de vuelta contigo enseguida🏃💨. ¡Gracias por tu paciencia! 😊"
        data = await Enviar_MensajeIndividual_Message(number=number, messageId=messageId, text=body)
        return data
    if text:
        list_for.append(Enviar_Saludo_Bloqueo())

    return await enviar_mensaje_usuario(list_for)


async def enviar_mensaje_usuario(list_for):
    for item in list_for:
        await enviar_Mensaje_whatsapp(item)
        await sleep(1)


# Nuevo Forma
async def ObtenerTotalDeOrden_msg(number, data_orden, messageId):
    data = await Enviar_MensajeIndividual_Message(number, data_orden, messageId)
    return data


async def EnviarMetodosDePagos_img_options(number):
    body = "Aqui te envio los datos de transferencia"
    footer = "SF | Gracias por preferirnos ♥"
    options = ["Transferencia", "Pago en Efectivo", "3er Opcion"]
    # aca deberia consultar en la db, en la tabla proceso de pagos, columna imagen y hacer la consulta con la id o numero
    url_img = "https://i.postimg.cc/PJPRZJBh/e35f9d3b-f59b-44ed-91e2-e6742799baad.png"
    data = await ButtonImagenOpciones_Message(number, body=body, footer=footer, options=options, url_img=url_img)
    return data


async def Datos_para_descargarImagen(number, imagen_id, messageId):
    img_url = await ObtenerIdImagen(imagen_id)
    await descargar_imagen(img_url, number)
    data = await Enviar_MensajeIndividual_Message(number, "Gracias por el screeshot", messageId)
    return data


async def Descagar_pdf(number):
    try:
        link = str(sett.doc_pdf)
        caption = "PDF de nuestros filtros"
        filename = "Filtros - SF"

        data = await Enviar_Document_Message(number, link, caption, filename)
        return data
    except Exception as e:
        print(e)


async def Send_Catalogo_wsp(number):
    try:
        body = "Te presento nuestro catalogo"
        footer = "SF | santiagofiltros.cl"
        data = await Enviar_CatalgoSimpleWSP_Message(number, body, footer)
        return data
    except Exception as e:
        print(e)


async def RecibirUbicacion_Cliente(number):
    try:
        body = "Envianos tu dirección para ir a dejar tu pedido \n 👇"
        data = await Recibir_UbicacionCliente_Message(number, body)
        return data
    except Exception as e:
        print(e)


async def Enviar_Lista_Productos(number):
    try:
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
        body_text = "Productos de calidad, dale a tus cliente lo mejor"
        header_text = "Listado de Filtros"
        footer_text = "SF | Calidad y Confianza"
        button_text = "Ver ☑️"
        opciones = lista_opciones

        data = await Enviar_Lista_Opciones_Message(number, body_text, header_text, footer_text, button_text, opciones)
        return data
    except Exception as e:
        print(e)


async def Enviar_Menu_Saludo(number, messageId):
    body = "Hola, ¡bienvenido a SF! ❤️ Soy tu asistente virtual Jack 24/7. Navega por nuestro menú, conoce más sobre SF 😎 y descubre cómo iniciar tu negocio con nosotros 🚀."
    footer = "Equipo SF"
    options = ["Catalogo", "Información", "Ventas"]
    return await Enviar_Menu_Message(number, messageId, body, footer, options, sed="1")


async def Enviar_Menu_Catalogo(number, messageId):
    body = "Buena elección para revisar nuestros productos, te dejo aquí unas opciones"
    footer = "Productos SF"
    options = ["🗒️ Descargar PDF", "🤟 Lista de Productos", "😎 Catalogo WSP"]
    return await Enviar_Menu_Message(number, messageId, body, footer, options, sed="2")


async def Enviar_Menu_Informacion(number, messageId):
    body = "Quieres saber más de nosotros?, te dejo aquí unas opciones"
    footer = "Información SF"
    options = ["Ubicación?", "Redes Sociales", "Tienen pagina web?"]
    return await Enviar_Menu_Message(number, messageId, body, footer, options, sed="3")


async def Enviar_Menu_Ventas(number, messageId):
    body = "Emprende junto a nostros! 🤟, te dejo aquí unas opciones"
    footer = "Emprendiendo con SF"
    options = ["Contactar vendedor",
               "Tu primer negocio",
               "Consejos Utiles"]
    data = await Enviar_Menu_Message(number, messageId, body, footer, options, sed="3")
    return data


async def Enviar_Mensaje_ButtonImagen(number):
    body = "Te presento nuestras redes sociales, no olvides seguirnos para enterarte de ofertas y promociones del día"
    footer = "SF | Redes Sociales - FIX"
    options = ["Instagram", "Facebook", "TikTok"]
    url_img = "https://dinahosting.com/blog/upload/2022/07/tamanos-imagenes-redes-sociales-2024_dinahosting.png"
    data = await ButtonImagenOpciones_Message(number, body, footer, options, url_img)
    return data
        
async def Enviar_Menu_PrimerNegocio(number):
    body = "Tu primer negocio junto a SF | Confianza y Calidad"
    footer = "SF | Gracias por preferirnos ♥"
    options = ["Soy Cliente", "Primera Compra", "Ayuda PDF"]
    url_img = "https://i.postimg.cc/PJPRZJBh/e35f9d3b-f59b-44ed-91e2-e6742799baad.png"
    data = await ButtonImagenOpciones_Message(number, body, footer, options, url_img)
    return data

async def Enviar_MiUbicacion(number, messageId):
    try:
        data = await Ubicacion_Empresa_Message(number, messageId)
        return data
    except Exception as e:
        print(e)


async def Mensaje_Contactar_Vendedor(number):
    data = await ButtonContact_Message(number)
    return data


async def Enviar_TienenPaginaWeb(number):
    try:
        data = await Enviar_URLTexto_Message(number)
        return data
    except Exception as e:
        print(e)

async def Mensaje_Primera_Compra(number):

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
    header_text = "Presupuestos PREDETERMINADOS 🤟"
    body_text = "Selecciona el rango de compra 🛒 que mejor se ajusta a tus necesidades y te facilitaremos un PDF 📄 detallado para tu consulta. Este documento está diseñado con filtros específicos 🔍 para adaptarse a las particularidades de tu negocio 🏭, asegurando que encuentres exactamente lo que buscas de manera eficiente 💼."
    footer_text = "SF | Calidad y Confianza"
    button_text = "Ver Presupuestos 😎"
    opciones = lista_opciones
    data = await Enviar_Lista_Opciones_Message(number, body_text=body_text, header_text=header_text, footer_text=footer_text, button_text=button_text,opciones=opciones)
    return data

async def SinContext(number, messageId):     
    body = "No tengo ese comando en mi sistema, dime como puedo ayudarte?"
    footer = "Equipo SF | santiagofiltros.cl"
    options = ["Catalogo", "Información", "Tu Negocio"]
    data = await ButtonOpciones_Responder_msg(number, options, body, footer, "sed7", messageId)
    return data

async def Enviar_Imagenes(number):
    link = "https://i.postimg.cc/4xzJdjY2/Personal-Portafolio.jpg"
    caption = "Enviamos esta imagen para su conocimiento"
    data = await Enviar_Imagen_MSG(number, link, caption)
    return data

async def Mensaje_Rapido(number, messageId, mensaje=None):
    return await Enviar_MensajeIndividual_Message(number, mensaje, messageId)

async def administrar_chatbot(text, number, messageId, name, timestamp):
    # print(type(text))
    list_for = []
    lista_privada = ["hola", "admin"]

    if 'product_items' in text:
        data_orden = await procesar_orden(text)
        list_for.append(await EnviarMetodosDePagos_img_options(number))
        list_for.append(await ObtenerTotalDeOrden_msg(number, data_orden, messageId))

    elif 'mime_type' in text:
        imagen_id = text['id']
        # enviamos la id obtenenida del json
        list_for.append(await Datos_para_descargarImagen(imagen_id, number, messageId))

    else:
        text = text.lower()
        payload = json.dumps({
            "wsp_name": name,
            "wsp_number": number,
            "wsp_timestamp": timestamp,
            "wsp_text": text,
            "wsp_messageid": messageId
        })
        print(f"Mensaje del usuario {name}:", text)
        if text in "hola":

            # await guardar_datos_db(payload)
            list_for.append(await Enviar_Menu_Saludo(number, messageId))
        elif "img_send" in text: #enviamos una imagen
            list_for.append(await Enviar_Imagenes(number))

        # CATALOGO
        elif "catalogo" in text:
            list_for.append(await Enviar_Menu_Catalogo(number, messageId))
        elif "descargar pdf" in text:
            list_for.append(await Descagar_pdf(number))
        elif "catalogo wsp" in text:
            list_for.append(await Send_Catalogo_wsp(number))
        elif "enviar ubicación" in text:
            list_for.append(await RecibirUbicacion_Cliente(number))
        elif "lista de productos" in text:
            list_for.append(await Enviar_Lista_Productos(number))
        # CREAR LOS ENLACES QUE LLEVEN AL USUARIO A BUSCAR LOS FILTROS www.santiagofitlros.cl/filtros/filtros-de-aire
        # Información
        elif text in "información":
            list_for.append(await Enviar_Menu_Informacion(number, messageId))
        elif text in "redes sociales":
            list_for.append(await Enviar_Mensaje_ButtonImagen(number))
        elif text in "ubicación?":
            list_for.append(await Enviar_MiUbicacion(number, messageId))
        elif text in "tienen pagina web?":
            list_for.append(await Enviar_TienenPaginaWeb(number))
        # TU NEGOCIO
        elif text in "ventas":
            list_for.append(await Enviar_Menu_Ventas(number, messageId))
        elif text in "contactar vendedor":
            list_for.append(await Mensaje_Contactar_Vendedor(number))

        # TU PRIMER NEGOCIO
        elif text in "tu primer negocio":
            list_for.append(await Enviar_Menu_PrimerNegocio(number))

        elif text in "soy cliente":
            pass

        elif text in "primera compra":
            tasks = await Enviar_VariosMensajes_Message(number, messageId)
            data = await Mensaje_Primera_Compra(number)
            
            for task in tasks:
                list_for.append(task)
            list_for.append(data)

        elif text in "CLP 100.000 - 300.000":
            
            list_for.append(await Mensaje_Rapido(number, messageId, "Descubre cómo tu negocio puede beneficiarse de nuestra selección de filtros con precios especiales al por mayor, ideales para pequeñas empresas o talleres que están comenzando. Al elegir esta opción, recibirás un PDF detallado con una propuesta de precios diseñada para optimizar tu inversión inicial."))

        elif text in "CLP 300.001 - 500.000":
            list_for.append(await Mensaje_Rapido(number,messageId, "Para empresas en crecimiento, ofrecemos un rango de precios competitivos que se ajusta a tus necesidades de expansión. Seleccionando este nivel, te enviaremos un PDF con una estructura de precios al por mayor que te permitirá escalar tu negocio manteniendo un equilibrio entre calidad y coste."))

        elif text in "CLP 500.001 - 700.000":
            list_for.append(await Mensaje_Rapido(number,messageId, "Empresas establecidas encontrarán en este rango una oportunidad para fortalecer su cadena de suministro con nuestros filtros de alto rendimiento a precios preferenciales. El PDF que recibirás como parte de esta opción refleja una estrategia de precios pensada para socios comprometidos con la calidad y la eficiencia."))

        elif text in "CLP 700.001 - XXX.XXX":
            list_for.append(await Mensaje_Rapido(number, messageId, "Dirigido a líderes de la industria y grandes flotas, este rango ofrece el mejor valor con precios exclusivos al por mayor para pedidos de gran volumen. Al optar por esta categoría, el PDF proporcionado incluirá una oferta personalizada que reconoce y recompensa tu inversión y fidelidad a largo plazo con SF."))

        # OTROS MENSAJES
        elif text in "gracias":
            list_for.append(await Mensaje_Rapido(number, messageId, "Estamos para ayudarte 🤓", ))

        elif text in ["chao", "hasta luego"]:
            list_for.append(await Mensaje_Rapido(number, messageId, "Estamos para ayudarte 🤓", ))

        elif text in "ok":
            list_for.append(await Mensaje_Rapido(number, messageId, "😎"))

        elif text in "como es el local?":
            
            list_for.append(await Enviar_Imagenes)

        else:                
            list_for.append(await SinContext(number, messageId))

    return await enviar_mensaje_usuario(list_for)
