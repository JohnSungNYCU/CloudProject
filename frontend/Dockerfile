FROM node:14.18.2-alpine


# Set the working directory for the frontend
WORKDIR /app
RUN apk update && apk add netcat-openbsd
# Copy package.json and install dependencies
COPY package.json /app
# Copy the frontend code and install Node.js dependencies
RUN npm install
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
COPY . /app

# Build the Vue app
RUN npm run build

# Expose the port the app runs on
EXPOSE 8080
# Command to run your app
# CMD ["npm", "run", "dev"]


