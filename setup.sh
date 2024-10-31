curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

source ~/.bashrc

nvm install v18.12.0

nvm use v18.12.0

cd frontend; npm install --legacy-peer-deps; cd ..

docker-compose up -d