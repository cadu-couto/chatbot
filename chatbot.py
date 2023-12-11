import json
import pickle
import numpy as np
import random
from tensorflow.keras.models import load_model
import nltk


nltk.download('rslp')
stemmer = nltk.stem.RSLPStemmer()


class Chatbot:

    def __init__(self):
        self.model = load_model('data/chatbot_model.h5')
        self.intents = json.loads(open('data/intents.json').read())
        self.words = pickle.load(open('data/words.pkl','rb'))
        self.classes = pickle.load(open('data/classes.pkl','rb'))
        self.ignore_words = ['?', '!', ',', ';']


    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [stemmer.stem(w.lower()) for w in sentence_words if w not in self.ignore_words]
        sentence_words = sorted(list(set(sentence_words)))
        return sentence_words


    def bow(self, sentence, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(self.words)
        for s in sentence_words:
            for i,w in enumerate(self.words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return (np.array(bag))


    def predict_class(self, sentence):
        # filter out predictions below a threshold
        p = self.bow(sentence, show_details=False)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.75
        results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        # print(return_list)
        return return_list


    def getResponse(self, ints):
        tag = ints[0]['intent']
        list_of_intents = self.intents['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(self, msg):
        ints = self.predict_class(msg)
        res = {}
        if len(ints) > 0:
            res['msg_from_chatbot'] = self.getResponse(ints)
            res['intent'] = ints[0]['intent']
            res['probalitiy'] = ints[0]['probability']
        else:
            res['msg_from_chatbot'] = "Desculpe, não entendi!"
            res['intent'] = None
            res['probalitiy'] = None
        return res


    def start_chat(self):
        res = {}
        res['msg_from_chatbot'] = "Bem vindo a Farmárcia XYZ. Sou um Chatbot! Aqui estou vou conseguir responder algumas das suas dúvidas mais frequentes. Qual a sua dúvida?"
        res['intent'] = None
        res['probalitiy'] = None
        return res







