import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


# URL da Netflix
netflix_url = "https://www.netflix.com/br/browse/genre/34399"

client = MongoClient("localhost", 27017)  # Conecta ao MongoDB local
  # Conecta ao MongoDB local
db = client["netflix_catalog"]  # Nome do banco de dados
collection = db["movies"]  # Nome da coleção

# Função para fazer a solicitação e analisar a página da Netflix
def crawl_netflix_catalog():
    try:
        # Fazer uma solicitação GET para a página da Netflix
        response = requests.get(netflix_url)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Analisar o conteúdo HTML da página usando BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar todos os elementos que contêm informações de filmes
            movie_elements = soup.find_all('section', class_='nm-collections-row')

            # Iterar pelos elementos e extrair títulos e artwork
            for movie in movie_elements:
                # Extraindo o
                categoria = movie.find('h2',  class_='nm-collections-row-name').text
                title = movie.find('span', class_='nm-collections-title-name').text

                # Extraindo a URL da artwork (imagem)
                artwork_url = movie.find('img', class_='nm-collections-title-img')['src']
                url_filme = movie.find('a', class_="nm-collections-title nm-collections-link")['href']
                print(url_filme)    
              
                # Exibindo o título e a URL da artwork
                print("Categoria:", categoria)
                print("Título:", title)
                print("Artwork:", artwork_url)
                print("\n")

                # Inserir os dados no MongoDB
                movie_data = {
                    "categoria": categoria,
                    "titulo": title,
                    "artwork": artwork_url,
                    "link": url_filme,
                }
                result = collection.insert_one(movie_data)
                print(result)
                if result != None:
                    print("Dados inseridos com sucesso no MongoDB.")

        else:
            print("Falha ao acessar a página da Netflix")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Função para buscar dados no MongoDB
def buscar_filme_por_titulo(titulo):
    try:
        # Realizar a busca no MongoDB
        movie = collection.find_one({"titulo": titulo})

        if movie:
            print("Dados encontrados:")
            print("Categoria:", movie["categoria"])
            print("Título:", movie["titulo"])
            print("Artwork:", movie["artwork"])
        else:
            print("Filme não encontrado no catálogo.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chamar a função para iniciar o web crawler e inserir os dados no MongoDB
crawl_netflix_catalog()

# Chamar a função de busca por título
