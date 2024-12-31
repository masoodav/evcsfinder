# Stage 1: Base image for development
FROM node:18-alpine as base

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Install nodemon globally
RUN npm install -g nodemon

# Copy the application code
COPY . .

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Stage 2: Development image with nodemon
FROM base as development

# Use nodemon to start the React app with polling
CMD ["nodemon", "-L", "--watch", "src", "--watch", "public", "--ext", "js,jsx", "--exec", "npm start"]

# Stage 3: Build the React app
FROM base as build

# Copy application code and install dependencies (again, if needed)
COPY . .
RUN npm run build

# Stage 4: Production image with nginx
FROM nginx:alpine

# Copy the React build output to the nginx directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose the app ports
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
