# Step 1: Build React app
FROM node:18 as react-build

# Set working directory
WORKDIR /app

# Copy React app source code
COPY ./react-app/package*.json ./

# Install dependencies and build React app
RUN npm install

COPY ./react-app/ ./

RUN npm run build

# Step 2: Set up Nginx and Gradio app
FROM python:3.9-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx jq

# Set working directory for Gradio app
WORKDIR /app

# Copy Gradio app source code
COPY ./gradio-app/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy React build to the Nginx directory
COPY --from=react-build /app/dist /usr/share/nginx/html

# Copy Nginx configuration file
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

COPY ./start.sh /start.sh

# Expose port for Nginx (default 80)
EXPOSE 80
EXPOSE 8080

# Start Nginx and Gradio app
# CMD service nginx start && python app.py

CMD ["/start.sh"]
