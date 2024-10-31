#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[*] Starting CTF Challenge Setup${NC}"

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[-] Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}[-] Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Generate random secrets for production
JWT_SECRET=$(openssl rand -hex 32)
ADMIN_TOKEN=$(openssl rand -hex 32)
SERVICE_AUTH_SECRET=$(openssl rand -hex 32)
ADMIN_PASSWORD=$(openssl rand -base64 12)

# Create .env file
cat > ../.env << EOL
JWT_SECRET=${JWT_SECRET}
ADMIN_TOKEN=${ADMIN_TOKEN}
SERVICE_AUTH_SECRET=${SERVICE_AUTH_SECRET}
ADMIN_PASSWORD=${ADMIN_PASSWORD}
FLAG=CTF{http2_smuggl1ng_1s_fun_2024}
EOL

echo -e "${GREEN}[+] Generated secure environment variables${NC}"

# Check if localhost is in /etc/hosts
if ! grep -q "localhost" /etc/hosts; then
    echo -e "${YELLOW}[!] Please add the following line to your /etc/hosts:${NC}"
    echo "127.0.0.1 localhost"
    read -p "Press enter to continue..."
fi

# Pull and build images
echo -e "${GREEN}[*] Building Docker images...${NC}"
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml build

# Start the challenge
echo -e "${GREEN}[*] Starting services...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo -e "${YELLOW}[*] Waiting for services to start...${NC}"
sleep 10

# Check if services are running
echo -e "${GREEN}[*] Checking service status...${NC}"
if docker-compose -f docker-compose.prod.yml ps | grep -q "Exit"; then
    echo -e "${RED}[-] Some services failed to start. Please check the logs.${NC}"
    exit 1
fi

# Print challenge information
echo -e "\n${GREEN}=== Challenge Information ===${NC}"
echo -e "Challenge URL: ${YELLOW}https://localhost${NC}"
echo -e "\nTest Accounts:"
echo -e "  Regular User:"
echo -e "    Username: ${YELLOW}alice${NC}"
echo -e "    Password: ${YELLOW}user1_pass${NC}"
echo -e "\nAdmin credentials are set in the environment."
echo -e "\n${GREEN}[+] Setup complete! Good luck!${NC}\n"

# Print helpful commands
echo -e "${YELLOW}Helpful commands:${NC}"
echo "  - View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  - Stop challenge: docker-compose -f docker-compose.prod.yml down"
echo "  - Restart challenge: docker-compose -f docker-compose.prod.yml restart"