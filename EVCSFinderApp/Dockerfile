# Base image for development
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Set build-time argument and environment variable
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Copy the application code
COPY . .

# Install development dependencies (like nodemon)
RUN npm install --save-dev nodemon

# Use nodemon to start the React app
CMD ["npx", "nodemon", "-L", "--watch", "src", "--watch", "public", "--ext", "js,jsx,css", "--exec", "npm start"]
