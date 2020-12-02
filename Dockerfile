FROM node:lts-alpine as client

# faz da pasta 'app' o diretório atual de trabalho
WORKDIR /app

RUN apk add python3 make g++; 

# copia os arquivos 'package.json' e 'package-lock.json' (se disponível)
COPY ./client/web/app/package*.json ./

# instala dependências do projeto
RUN npm install; \
    npm audit fix --force;

# copia arquivos e pastas para o diretório atual de trabalho (pasta 'app')
COPY ./client/web/app /app

RUN npm run build

FROM nginx

RUN rm -rf /etc/nginx/conf.d/*

COPY ./server/proxy/prod/nginx.conf /etc/nginx/
COPY ./server/proxy/prod/conf.d /etc/nginx/conf.d
COPY --from=client /app/build /usr/usr/share/nginx/html

CMD [ "nginx", "-g", "daemon off;" ]