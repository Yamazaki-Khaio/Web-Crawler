# Define a imagem base
FROM python:3.7.3-alpine3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /ap
# Instala as dependências do projeto
COPY requirements.txt ./

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte para dentro do contêiner
COPY . .

# Expõe a porta 3000 do contêiner
EXPOSE 3000

# Define o comando padrão que será executado quando o contêiner for iniciado
CMD [ "python" "crawler_atividade" ]
