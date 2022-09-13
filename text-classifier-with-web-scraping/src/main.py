# Projeto 1 - Classificação de Texto com Aprendizagem Supervisionada

# Pacotes
import os
from dotenv import load_dotenv

import re
import praw

## Carregando os Dados

# Lista de temas que usaremos para buscas no Reddit. 
# Essas serão as classes que usaremos como variável target
assuntos = ['datascience', 'machinelearning', 'physics', 'astrology', 'conspiracy']

# Função para carregar os dados-----------------------------------------------------
def carrega_dados():
    # Carrega as variáveis de ambiente
    load_dotenv()

    # Primeiro extraímos os dados do Reddit acessando via API
    api_reddit = praw.Reddit(client_id = os.getenv('ID'), 
    	                     client_secret = os.getenv('CLIENT_SECRET'),
                             password = os.getenv('PASSWORD'),
                             user_agent = os.getenv('USER_AGENT'),
                             username = os.getenv('USERNAME'))

    # Contamos o número de caracteres usando expressões regulares
    char_count = lambda post: len(re.sub('\W|\d', '', post.selftext))

    # Definimos a condição para filtrar os posts (retornaremos somente posts com 100 ou mais caracteres)
    mask = lambda post: char_count(post) >= 100

    # Listas para os resultados
    data = []
    labels = []

    # Loop
    for i, assunto in enumerate(assuntos):

        # Extrai os posts
        subreddit_data = api_reddit.subreddit(assunto).new(limit = 1000)

        # Filtra os posts que não satisfazem nossa condição
        posts = [post.selftext for post in filter(mask, subreddit_data)]

        # Adiciona posts e labels às listas
        data.extend(posts)
        labels.extend([i] * len(posts))

        # Print
        print(f"Número de posts do assunto r/{assunto}: {len(posts)}",
              f"\nUm dos posts extraídos: {posts[0][:600]}...\n",
              "_" * 80 + '\n')
    
    return data, labels