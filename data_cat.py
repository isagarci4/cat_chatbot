from multiprocessing.connection import answer_challenge
import bs4 as bs
import urllib.request
import re
import nltk
from numpy import vectorize

#Abre a página de dados da web do gato
cat_data = urllib.request.urlopen('https://pt.wikipedia.org/wiki/Gato').read()

#Encontre todo o html do paragrafo da pagina web
cat_data_paragraphs = bs.BeautifulSoup(cat_data, 'lxml').find_all('p')

#Criando o corpus de todos os parágrafos da página web
cat_text = ''

#Criando corpus de texto inferior de paragrafos cat
for p in cat_data_paragraphs:
    cat_text += p.text.lower()

#Limpando o texto
cat_text = re.sub(r'\s+', ' ',re.sub(r'\[[0-9]*\]', ' ', cat_text))

#Lista de frases
cat_sentences = nltk.sent_tokenize(cat_text)

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def chatbot_answer(user_query):
    
    #Anexa a consulta á lista de frases
    cat_sentences.append(user_query)
    
    #Cria o vetor de frases com base na lista
    vectorizer = TfidfVectorizer()
    sentences_vectors = vectorizer.fit_transform(cat_sentences) 
    
    #Mede a similaridade do cosseno e pegue o segundo índice mais próximo porque o primeiro índice é a consulta do usuário
    vector_values = cosine_similarity(sentences_vectors[-1], sentences_vectors)
    answer = cat_sentences[vector_values.argsort()[0][-2]]
    
    #Verificação final para certificar-se de que há resultados presentes. Se todo o resultado for 0, significa que o texto inserido por nós não foi capturado no corpus
    input_check = vector_values.flatten()
    input_check.sort()
    
    if input_check[-2] == 0:
        return "Por favor, tente novamente"
    else:
        return answer