FROM node as build-deps
WORKDIR /usr/src/frontend
COPY package.json yarn.lock ./
RUN yarn add react-redux
RUN yarn
COPY . ./
RUN yarn build

FROM nginx:alpine
COPY --from=build-deps /usr/src/frontend/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]