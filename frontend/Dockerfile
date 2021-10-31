# Docker image to run SIRPA frontend app in development
# Projecto Integrado
# Lic. Eng. Informática
# ESTIG - IPBEJA

# Node image to donwload from docker
FROM node:16.13.0-bullseye as dev

# Setting working dir inside image
WORKDIR /app

# Copy package file to isntall app dependency's
COPY package.json package.json
COPY package-lock.json package-lock.json

# Run npm install inside container
RUN npm install

# Copy all project folders from local to containter
COPY . .

# CMD to run when the container runs
CMD ["npm", "run", "start"]
