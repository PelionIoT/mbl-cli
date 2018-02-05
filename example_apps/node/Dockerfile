FROM arm32v6/alpine:3.6

ENV NODE_VERSION 6.12.3

RUN apk add --no-cache nodejs nodejs-npm curl libgcc libstdc++ libuv libcrypto1.0 libssl1.0

WORKDIR .

COPY package.json package.json

RUN npm install

COPY . .

CMD ["node", "server.js"]
