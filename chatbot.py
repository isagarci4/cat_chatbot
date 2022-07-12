from operator import index
from data_cat import *
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

app = Flask(__name__)

#print("Olá, eu sou o Cat Chatbot. Quais são suas perguntas miau?:") 
#while(True): 
#    query = input().lower() 
#    if query not in ['tchau', 'adeus', 'cuide-se']: 
#        print("Cat Chatbot: ", end="") 
#        print(chatbot_answer(query)) 
#        cat_sentences.remove(query) 
#    else: 
#        print("Até a próxima!") 
#        break

bot = ChatBot('chatbot', read_only=False,
    logic_adapters=[
        
        {
            'import_path':'chatterbot.logic.BestMatch',
            'default_response':'Descupe, eu não tenho uma resposta :(',
            'maximum_similarity_threshould': 0.9
        }
        
        ])


trainer = ListTrainer(bot)
trainer.train(cat_sentences)


#Flask
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/get')
def get_chatbot_response():
    userText = request.args.get('userMessage')
    return str(bot.get_response(userText))

if __name__ == '__main__':
    app.run(debug=True)