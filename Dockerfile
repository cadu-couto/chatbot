# Define a imagem base
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório /app
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia o conteúdo do diretório atual para o diretório /app
COPY . .

# Exponha a porta 5000
EXPOSE 5000

# Define o comando de execução da API
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]