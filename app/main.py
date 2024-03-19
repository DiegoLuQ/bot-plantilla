from fastapi import FastAPI, Query, Request, HTTPException
from config import settings as sett
import services
import uvicorn
app = FastAPI()

WEBHOOK_VERIFY_TOKEN = "415teahicnjukkaka"

@app.get("/")
def home():
    return {"hola":sett.token}

@app.get("/webhook")
def webhook(hub_mode: str = Query(default=None, alias="hub.mode"),
            hub_verify_token: str = Query(default=None, alias="hub.verify_token"),
            hub_challenge: str = Query(default=None, alias="hub.challenge")):
    # Comprueba que el modo y el token enviados son correctos
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        # Responde con el token de desafío de la solicitud
        return hub_challenge
    else:
        # Responde con '403 Forbidden' si los tokens de verificación no coinciden
        raise HTTPException(status_code=403, detail="Forbidden")
    
@app.post('/whatsapp')
async def recibir_mensaje(request:Request):
    try:
        body = await request.json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = await services.obtener_Mensaje_whatsapp(message)
        # print(body)
        timestamp = int(message['timestamp'])

        await services.administrar_chatbot(text, number, messageId, name, timestamp)
        
        
        return 'EVENT_RECEIVED'
      
    except Exception as e:
      return HTTPException(status_code=500, detail=str(e))


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=94)