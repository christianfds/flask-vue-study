# build stage
FROM node:lts-alpine as build-stage

WORKDIR /app

ARG vite_api_url
ENV VITE_API_URL $vite_api_url

COPY package*.json ./
COPY yarn.lock ./

# RUN npm install --global yarn
RUN yarn install
COPY . .
RUN yarn run build 

# FROM nginx as production-stage

# ARG vite_api_url
# ENV VITE_API_URL $vite_api_url

# RUN mkdir /app
# COPY --from=build-stage /app/dist /app
# COPY nginx.conf /etc/nginx/nginx.conf

# CMD ["nginx", "-g", "daemon off;"]
CMD ["yarn", "run", "dev", "--host"]