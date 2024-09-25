# Usar a imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements.txt e instalar as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar todos os arquivos do projeto para o container
COPY . .

# Expor a porta 5000 para acessar o Flask
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "app.py"]
