from fastapi import FastAPI, Query, Request, HTTPException
from config import settings as sett
import services
import uvicorn
app = FastAPI()

@app.get("/")
def home():
    return {"hola":sett.token}

@app.get('/webhook')
def verify_token(hub_verify_token:str = Query(None, alias="hub.verify_token"), hub_challenge: str = Query(None, alias='hub.challenge')):
    try:
      access_token = sett.token
      if hub_verify_token == access_token and hub_challenge:
          return hub_challenge
      else:
          return 'Token incorrecto'
    except Exception as e:
      return e, 403
    
@app.post('/webhook')
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=52)