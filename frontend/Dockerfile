FROM node:14.18.2-alpine


# Set the working directory for the frontend
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json /app
RUN npm install

# Copy the frontend code and install Node.js dependencies
COPY . /app

# Build the Vue app
RUN npm run build

# Expose the port the app runs on
EXPOSE 8080
# Command to run your app
CMD ["npm", "run", "dev"]


