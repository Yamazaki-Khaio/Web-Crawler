#imports
import requests
from bs4 import BeautifulSoup

# URL da Netflix
netflix_url = "https://www.netflix.com/br/browse/genre/34399"

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
            #print(movie_elements)

            # Iterar pelos elementos e extrair títulos e artwork
            for movie in movie_elements:
                # Extraindo o 
                categoria = movie.find('h2',  class_ = 'nm-collections-row-name').text
                title = movie.find('span', class_='nm-collections-title-name').text
                

                # Extraindo a URL da artwork (imagem)
                artwork = movie.find('img', class_='nm-collections-title-img')['src']

                # Exibindo o título e a URL da artwork
                print("Categoria:", categoria)
                print("Título:", title)
                print("Artwork:", artwork)
                print("\n")

        else:
            print("Falha ao acessar a página da Netflix")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chamar a função para iniciar o web crawler
crawl_netflix_catalog()
