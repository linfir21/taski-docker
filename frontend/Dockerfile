FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

# CMD убран — команда в docker-compose.yml