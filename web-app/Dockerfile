FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build && rm -rf node_modules && npm ci --omit=dev --ignore-scripts

# Render utilise $PORT — Next.js doit écouter dessus
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

EXPOSE 3000

CMD ["sh", "-c", "next start -p ${PORT:-3000}"]
