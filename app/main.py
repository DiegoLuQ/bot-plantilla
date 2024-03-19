from fastapi import FastAPI, Query, Request, HTTPException
from config import settings as sett
import services
import uvicorn
app = FastAPI()

@app.get("/")
def home():
    return {"hola":sett.token}

@app.get('/whatsapp')
async def verify_token(request: Request):
    try:
        access_token = "asd7s7s8a5s4d8asd5diego"
        # FastAPI no tiene un objeto request.args directamente, pero puedes acceder a los parámetros de consulta
        # de la siguiente manera:
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        if token == access_token and challenge != None and token != None:
            return challenge
        else:
            return 'Token incorrecto'
        
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