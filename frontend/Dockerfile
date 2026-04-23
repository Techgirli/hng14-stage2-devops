FROM node:18-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY package*.json .
RUN npm ci --only=production

COPY . .
RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:3000/ || exit 1

EXPOSE 3000
CMD ["node", "app.js"]
