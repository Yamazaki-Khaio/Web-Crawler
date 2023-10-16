import base64
from pymongo import MongoClient
import time

from requests_oauthlib import OAuth1Session, OAuth2Session

# Configurar as chaves de autenticação do Twitter
consumer_key = "lWmZUe28m81gMDxHaTpW4fJ44"
consumer_secret = "EnKMGBKK6ze5cSWQtzbQZryhfqICodUQpWdwFCfKWqLGlVo3q1"
access_token = "1713899892307824640-Ez4ByaxscdtWA0S9et3uENeNtA6l0Y"
access_token_secret = "vu1HFnycaC9b88JElg7KFB3YSDGB40Dz7TaFHmOFkrnFl"
client_id = "eUxYMlRWOWtXSGhHc2tGTTlWalk6MTpjaQ"
client = "vertjWh1IqHDWHaBUw71ZNcOgfb2Ipa6PyuWnWrxvtEL2PpeX2"

# Dados do tweet 
def postar_no_twitter(movie_data, oauth):
    try:        
        artwork_base64 = movie_data["Artwork"] # Imagem em base64
        #converter para pn
        artwork_base64 = artwork_base64.replace("data:image/jpeg;base64,", "")
    
        tweet_text = f"Confira o filme: '{movie_data['Titulo']}' \n Categoria '{movie_data['Categoria']}' \n' na Netflix! #Netfl/ix #Filmes"

        # Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json={"text": tweet_text},
            )
        if response.status_code == 200:
            print(f"Tweet postado com sucesso para '{movie_data['Titulo']}'")
        else:
            raise Exception(
                "A solicitação retornou um erro: {} {}".format(response.status_code, response.text)
            )

    except Exception as e:
        print(f"Ocorreu um erro ao postar no Twitter: {e}")

if __name__ == "__main__":
    # Conectar ao MongoDB
    cliente = MongoClient("localhost", 27017)
    db = cliente["netflix_catalog"]
    collection = db["movies"]

    # Configurar a sessão OAuth2
    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
)

    for filme in collection.find():
        movie_data = {
            "Titulo": filme["titulo"],
            "Categoria": filme["categoria"],
            "Artwork": filme["artwork"]
        }
        postar_no_twitter(movie_data, oauth)
        time.sleep(300)  # Esperar 5 minutos entre as postagens
