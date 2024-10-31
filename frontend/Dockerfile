# Build stage
FROM node:18-slim as build

WORKDIR /app

# Copy package files
# COPY package*.json ./

# Basic install without extra flags
# RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-slim

WORKDIR /app

# Simple serve installation
RUN npm install -g serve

# Copy built files from build stage
COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]