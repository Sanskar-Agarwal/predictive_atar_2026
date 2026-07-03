# Use a modern Node LTS runtime as a parent image (node:14 is too old for this
# project's dependencies, e.g. react-scripts 5 / pdfjs-dist 4.x)
FROM node:20

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Bundle app source
COPY . .

# Dev server needs to bind to all interfaces to be reachable from outside the
# container via the port mapping (it defaults to localhost-only otherwise).
ENV HOST=0.0.0.0
# CRA's file watcher doesn't always pick up changes on Docker's default
# filesystem event mechanism — polling is the standard workaround.
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 2026

CMD ["npm", "start"]
