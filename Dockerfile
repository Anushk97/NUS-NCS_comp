# Stage 1: Build the React app
FROM node:14 AS build-stage

# Set working directory
WORKDIR /usr/src/app

# Copy app dependencies
COPY package*.json ./
RUN npm install

# Copy app source
COPY . .

# Build the app
RUN npm run build

# Stage 2: Set up the Python app
FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built React app from the previous stage
COPY --from=build-stage /usr/src/app/dist /app/static

# Copy Python app source
COPY . .

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port
EXPOSE 8080

# Command to run the app
CMD ["/usr/bin/supervisord"]
