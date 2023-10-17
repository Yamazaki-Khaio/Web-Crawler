from pymongo import MongoClient
import time
import tweepy
import gdown


# Dados do tweet 
def postar_no_twitter(movie_data, oauth, client_auth):
    try:   
        image_url = movie_data["Artwork"]
        print(image_url)
        media = None
        if image_url != "":
            path = "tmp/{}.jpg".format(str(movie_data["Titulo"]))
            gdown.download(image_url, path)
            media = oauth.media_upload(filename=path)
         
        # Criar o texto do tweet        
        tweet_text = f"Confira o filme: {movie_data['Titulo']}\n\nCategoria: {movie_data['Categoria']}\n\n na Netflix! #Netflix #Filmes"

        # Making the request
        if media is not None:
            client_auth.create_tweet(text=tweet_text, media_ids=[media.media_id])
                 
        else:
            client_auth.create_tweet(text=tweet_text)
            
        return True
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
      
if __name__ == "__main__":
    # Configurar as chaves de autenticação do Twitter
    consumer_key = "lWmZUe28m81gMDxHaTpW4fJ44"
    consumer_secret = "EnKMGBKK6ze5cSWQtzbQZryhfqICodUQpWdwFCfKWqLGlVo3q1"
    access_token = "1713899892307824640-Ez4ByaxscdtWA0S9et3uENeNtA6l0Y"
    access_token_secret = "vu1HFnycaC9b88JElg7KFB3YSDGB40Dz7TaFHmOFkrnFl"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAPcuqgEAAAAAf5%2Fojwadayv5xMSbzq9tvtBCKcg%3D2pjKaYBnx1gHNvvpKiZ0fNDwuyuANxi8f8aPr6JmsxwXEcq7e4"

    
    client_auth = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    oauth = tweepy.API(auth)
    
    

    # Conectar ao MongoDB
    cliente = MongoClient("localhost", 27017)
    db = cliente["netflix_catalog"]
    collection = db["movies"]


    for filme in collection.find():
        movie_data = {
            "Titulo": filme["titulo"],
            "Categoria": filme["categoria"],
            "Artwork": filme["artwork"]
        }
        postar_no_twitter(movie_data, oauth, client_auth)
        time.sleep(300)  # Esperar 5 minutos entre as postagens
