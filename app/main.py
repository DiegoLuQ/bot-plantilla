from fastapi import FastAPI, Query, Request, HTTPException, Depends, Response, Cookie
from config import settings as sett
from fastapi.responses import PlainTextResponse
import services
import jwt
import time
from asyncio import sleep, create_task
from contextlib import asynccontextmanager

SECRET_KEY = sett.SECRET_KEY
BLOCK_DURATION_SECONDS = 15
# Diccionario para almacenar el recuento de solicitudes por número de celular
request_counts = {}

# Lista para almacenar los números de celular que han excedido el límite
exceeded_numbers = set()

# Límite de solicitudes por hora
MAX_REQUESTS_PER_MINUTE = 2

        
def generate_jwt(number):
    payload = {
        "number": number,
        "exp": time.time() + BLOCK_DURATION_SECONDS
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")    
    
# Función para verificar si un usuario está bloqueado
def is_blocked(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["exp"] > time.time()
    except jwt.ExpiredSignatureError:
        return False  # El token ha expirado, el usuario no está bloqueado
    except jwt.InvalidTokenError:
        return False  # Token inválido, el usuario no está bloqueado  

# Middleware para verificar si el usuario está bloqueado
async def check_blocked(request: Request, response: Response):
    token = request.cookies.get("token")
    body = await request.json()
    entry = body['entry'][0]
    changes = entry['changes'][0]
    value = changes['value']
    message = value['messages'][0]
    number = message['from']
    
    if token and is_blocked(token):
        request_counts[number] = 0
        raise HTTPException(status_code=403, detail="Usuario bloqueado")
    elif not token:
        print("token Eliminado")
        response.delete_cookie("token")  # Eliminar la cookie si no hay token
    else:
        print("token Eliminado")
        response.delete_cookie("token")  # Eliminar la cookie si el usuario ya no está bloqueado

async def check_request_counts():
    try:
        BLOCK_DURATION_MINUTES = 60
        while True:
            await sleep(BLOCK_DURATION_MINUTES* 60)
            print("Verificando Solicitudes",request_counts)
            # await sleep(20)
            # request_counts.clear()
            # print("Limpiando Solicitudes",request_counts)
    except Exception as e:
      print(e)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        # Inicializar el temporizador de desbloqueo para los números que ya están bloqueados
        print("Hola")
        
        create_task(check_request_counts())
            
        yield 
        
    finally:
        # Limpiar los temporizadores y desbloquear los números al finalizar el contexto
        print("Fin")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=94)

app = FastAPI(lifespan=app_lifespan)
    
async def rate_limit(request: Request):
    body = await request.json()
    print(body)
    entry = body['entry'][0]
    changes = entry['changes'][0]
    value = changes['value']
    message = value['messages'][0]
    if body:
        print(message)
        number = message['from']
        print(message['from'])
        request_count = request_counts.get(number, 0)

        # Inicializar token como None
        token = None
        
        # Verificar si se ha excedido el límite de solicitudes
        if request_count >= MAX_REQUESTS_PER_MINUTE:
            token = generate_jwt(number)      

        # Actualizar el recuento de solicitudes del número de number
        request_counts[number] = request_count + 1
        
        # Retornar el token generado
        return token

# @app.post('/whatsapp', dependencies=[Depends(rate_limit), Depends(check_blocked)])
@app.post('/whatsapp', dependencies=[Depends(check_blocked)])
async def recibir_mensaje(request:Request, response:Response, token: str = Depends(rate_limit)):
    try:
        # Verificar si el token está presente y no es None
        if token:
            # Configurar la cookie con el token
            response.set_cookie(key="token", value=token, expires=BLOCK_DURATION_SECONDS, httponly=True)
        
        body = await request.json()
        # print(body)
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        
        text = await services.obtener_Mensaje_whatsapp(message)
        timestamp = int(message['timestamp'])
        
        print("solicitudes",request_counts)
        if not is_blocked(token):
            await services.administrar_chatbot(text, number, messageId, name, timestamp)
        else:
            await services.bloquear_usuario(text, number, messageId, name, timestamp)
            
        return 'EVENT_RECEIVED'   
      
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def home():
    return {"hola":sett.token}

@app.get("/whatsapp")
async def verify_token(request: Request):
    access_token = sett.token
    # Acceder directamente a los parámetros de consulta del objeto request
    hub_verify_token = request.query_params.get("hub.verify_token")
    hub_challenge = request.query_params.get("hub.challenge")

    try:
        if hub_verify_token and hub_challenge and hub_verify_token == access_token:
            # Devolver el challenge directamente como texto plano
            return PlainTextResponse(content=hub_challenge, status_code=200)
        else:
            raise HTTPException(status_code=400, detail="Invalid request")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))