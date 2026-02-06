FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY mcp_server.js ./

EXPOSE 3000

CMD ["node", "mcp_server.js"]
