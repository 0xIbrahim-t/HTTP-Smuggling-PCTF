FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy other project files
COPY . .

# Build the project
RUN npm run build

# Install serve to run the built project
RUN npm install -g serve

# Start the service
CMD ["serve", "-s", "build", "-l", "3000"]