from pydantic import BaseModel



class MsgSchema(BaseModel):
    msg: str = "Messangem para o Chatbot em sk"