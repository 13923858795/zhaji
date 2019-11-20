# build stage
FROM node:10 as build-stage
WORKDIR /app
COPY . /app
RUN npm install --registry=https://registry.npm.taobao.org
# RUN npm install 
RUN npm run build


# production stage
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
EXPOSE 8000
CMD nginx -g "daemon off;"
npm