# Usa imagem base leve do Python
FROM python:3.12-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia primeiro o arquivo de dependências para aproveitar o cache do Docker
COPY requirements.txt .

# Instala bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos do projeto para dentro do container
COPY . .

# Comando para rodar o script principal
CMD ["python", "analysis_1.py"]
