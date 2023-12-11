from chatbot import Chatbot

chatbot = Chatbot()

def test_start_chat():
    res = chatbot.start_chat()
    assert res['msg_from_chatbot'] is not None

def test_chatbot_response():
    res = chatbot.chatbot_response("Oi")
    assert res['msg_from_chatbot'] is not None
    assert res['intent'] == 'saudacao'
    assert float(res['probalitiy']) > 0,90


