## Modelo de Classificação de Texto com Dados Extraídos do Reddit (via web scraping)

***

**Pre requisitos:**

1. Criar conta no Reddit
2. Criar app de dev no Reddit (<https://www.reddit.com/prefs/apps>)
3. Criar um arquivo **.env** na raiz do projeto, e adicionar as seguintes variáveis no mesmo:
```
ID="reddit_api_id"
CLIENT_SECRET="reddit_api_secret"
PASSWORD="reddit_user_password"
USER_AGENT="any_one_text"
USERNAME="reddit_user_name"
```

**Execução:**

1. Executar `poetry shell` para iniciar o ambiente virtual
2. Executar `python3 src/main.py` para realizar a extração dos dados do reddit e o treinamento dos modelos conforme os dados extraídos