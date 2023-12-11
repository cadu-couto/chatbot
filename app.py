from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from logger import logger
from flask_cors import CORS
from schemas import *
from chatbot import Chatbot


info = Info(title="MVP - Chatbot", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Documentação: Swagger")
start_msg_tag = Tag(name="Inicia Chatbot", description="Inicia uma conversa com o Chatbot")
send_msg_tag = Tag(name="Enviar Messagem", description="Envia uma messagem para o Chatbot")


chatbot = Chatbot()

# Rota home
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi/swagger')

# inicia Chatbot
@app.post('/chatbot/start', summary="Inicia uma converda com o Chatbot", tags=[start_msg_tag])
def start_chatbot():
    try:
        res = chatbot.start_chat()
    except Exception as e:
        logger.warning(f"Erro na API '{e}'")
        return {"message": f'Erro modelo: {e}'}, 400

    return res, 200


# envia um pergunta para chatbot
@app.post('/chatbot/send_msg', summary="Envia uma pergunta para o Chatbot", tags=[send_msg_tag])
def send_msg(form: MsgSchema):
    try:
        res = chatbot.chatbot_response(form.msg)
    except Exception as e:
        logger.warning(f"Erro na API '{e}'")
        return {"message": f'Erro modelo: {e}'}, 400

    return res, 200
