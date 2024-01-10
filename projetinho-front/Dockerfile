# Use a imagem oficial do Node.js
FROM node:14

# Crie e configure o diretório de trabalho
WORKDIR /app

# Copie os arquivos necessários
COPY package*.json ./

# Instale as dependências
RUN npm install

# Copie os arquivos restantes
COPY . .

# Exponha a porta que o aplicativo React irá usar
EXPOSE 3000

# Comando para iniciar o aplicativo React
CMD ["npm", "start"]
