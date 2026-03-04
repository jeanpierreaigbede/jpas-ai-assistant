FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .

# URL API backend — nécessaire au build car NEXT_PUBLIC_* est inliné à la compilation
ARG NEXT_PUBLIC_API_BASE=https://jpas-ai-assistant.onrender.com
ENV NEXT_PUBLIC_API_BASE=$NEXT_PUBLIC_API_BASE

RUN npm run build && rm -rf node_modules && npm ci --omit=dev --ignore-scripts

# Render utilise $PORT — Next.js doit écouter dessus
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

EXPOSE 3000

CMD ["sh", "-c", "npx next start -p ${PORT:-3000}"]
