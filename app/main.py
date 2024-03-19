from fastapi import FastAPI, Query, Request, HTTPException
from config import settings as sett
import services
import uvicorn
app = FastAPI()

@app.get("/")
def home():
    return {"hola":sett.token}

@app.get('/whatsapp')
def verify_token(hub_verify_token:str = Query(None, alias="hub.verify_token"), hub_challenge: str = Query(None, alias='hub.challenge')):
    print(sett.token)
    try:
      access_token = "475811994@4s-4.D455"
      if hub_verify_token is not None and hub_challenge is not None and hub_verify_token == access_token:
          print("pasaste")
          return {"challenge": hub_challenge}
      else:
          return 'Token incorrecto'
    except Exception as e:
      return e, 403
    
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