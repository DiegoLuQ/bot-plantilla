from fastapi import FastAPI, Query, Request, HTTPException
from config import settings as sett
from fastapi.responses import PlainTextResponse
import services
import uvicorn
app = FastAPI()

WEBHOOK_VERIFY_TOKEN = "415teahicnjukkaka"

@app.get("/")
def home():
    return {"hola":sett.token}

@app.get("/whatsapp")
async def verify_token(request: Request):
    access_token = "asd7s7s8a5s4d8asd5"
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