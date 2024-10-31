# Build stage
FROM node:18-slim as build

# Set npm to use public DNS
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# Set npm config to use specific registry and DNS cache timeout
RUN npm config set registry https://registry.npmjs.org/ && \
    npm config set dns-timeout 30000 && \
    npm config set retries 10

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with specific registry
RUN npm install --legacy-peer-deps --registry=https://registry.npmjs.org/ || \
    (sleep 5 && npm install --legacy-peer-deps --registry=https://registry.npmjs.org/)

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-slim

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built files from build stage
COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]