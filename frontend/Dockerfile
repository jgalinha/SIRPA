# Node image to donwload from docker
FROM node:16.13.0-bullseye

# Setting working dir inside image
WORKDIR /code

# Copy package file to isntall app dependency's
COPY package.json package.json
COPY package-lock.json package-lock.json

# Run npm install inside container
RUN npm install

# Copy all project folders from local to containter
COPY . .

CMD ["npm", "run", "start"]
