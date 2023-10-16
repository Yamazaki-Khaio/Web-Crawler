from pymongo import MongoClient
import tweepy # Biblioteca para interagir com a API do Twitter
import requests # Biblioteca para realizar requisições HTTP
import io # Biblioteca para trabalhar com arquivos
from PIL import Image # Biblioteca para trabalhar com imagens

# Configurar a autenticação do Twitter (substitua com suas próprias chaves)
consumer_key = "2kh1nI6dmDLmYsgmwTBePnYX0"
consumer_secret = "VTmCb7stMvsC1sOUxTB6OyCJXNI9mho7mR1Pg7oRivg4mfYArR"
access_token = "1713899892307824640-KtvZcKt2LEqKJSSkEWU4vaLYBBPsZ0"
access_token_secret = "eNJXYf4LSpy2LVAFiUA7966TeoGyU65djOHmsj6wsDDS8"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Função para postar informações no Twitter
def postar_no_twitter(titulo, categoria, artwork):
    try:
        response = requests.get(artwork)
        image_data = io.BytesIO(response.content)
        image = Image.open(image_data)
        image.save("movie_artwork.jpg")

        tweet_text = f"Confira o filme '{titulo}' da categoria '{categoria}' na Netflix! #Netflix #Filmes"

        api.update_with_media("movie_artwork.jpg", status=tweet_text)

        print("Tweet postado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao postar no Twitter: {e}")

if __name__ == "__main":
    # Chamar a função para postar no Twitter para cada filme no banco de dados
    client = MongoClient("localhost", 27017)  # Conecta ao MongoDB local
    db = client["netflix_catalog"]  # Nome do banco de dados
    collection = db["movies"]  # Nome da coleção

    for filme in collection.find():
        titulo = filme["titulo"]
        categoria = filme["categoria"]
        artwork = filme["artwork"]
        postar_no_twitter(titulo, categoria, artwork)
