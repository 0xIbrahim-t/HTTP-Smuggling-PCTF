# Build stage
FROM node:18-slim as build

# Increase Node's memory limit
ENV NODE_OPTIONS=--max-old-space-size=4096

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

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

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "build", "-l", "3000"]