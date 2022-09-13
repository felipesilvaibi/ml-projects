# Projeto 1 - Classificação de Texto com Aprendizagem Supervisionada

# Pacotes
import os
from dotenv import load_dotenv

import re
import praw
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

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

## Divisão em Dados de Treino e Teste

# Variáveis de controle
TEST_SIZE = .2
RANDOM_STATE = 0


# Função para split dos dados
def split_data():

    print(f"Split {100 * TEST_SIZE}% dos dados para teste e avaliação do modelo...")
    
    # Split dos dados
    X_treino, X_teste, y_treino, y_teste = train_test_split(data, 
                                                            labels, 
                                                            test_size = TEST_SIZE, 
                                                            random_state = RANDOM_STATE)

    print(f"{len(y_teste)} amostras de teste.")
    
    return X_treino, X_teste, y_treino, y_teste

## Pré-Processamento de Dados e Extração de Atributos

# - Remove símbolos, números e strings semelhantes a url com pré-processador personalizado
# - Vetoriza texto usando o termo frequência inversa de frequência de documento
# - Reduz para valores principais usando decomposição de valor singular
# - Particiona dados e rótulos em conjuntos de treinamento / validação

# Variáveis de controle
MIN_DOC_FREQ = 1
N_COMPONENTS = 1000
N_ITER = 30

# Função para o pipeline de pré-processamento
def preprocessing_pipeline():
    
    # Remove caracteres não "alfabéticos"
    pattern = r'\W|\d|http.*\s+|www.*\s+'
    preprocessor = lambda text: re.sub(pattern, ' ', text)

    # Vetorização TF-IDF
    vectorizer = TfidfVectorizer(preprocessor = preprocessor, stop_words = 'english', min_df = MIN_DOC_FREQ)

    # Reduzindo a dimensionalidade da matriz TF-IDF 
    decomposition = TruncatedSVD(n_components = N_COMPONENTS, n_iter = N_ITER)
    
    # Pipeline
    pipeline = [('tfidf', vectorizer), ('svd', decomposition)]

    return pipeline
