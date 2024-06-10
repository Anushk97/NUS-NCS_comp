# Step 1: Build React app
FROM node:16 as react-build

# Set working directory
WORKDIR /app

# Copy React app source code
COPY ./react-app/package*.json ./
COPY ./react-app/ ./

# Install dependencies and build React app
RUN npm install
RUN npm run build

# Step 2: Build Gradio app
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Gradio app source code
COPY ./gradio-app/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy React build to the Gradio app directory
COPY --from=react-build /app/build ./static

# Expose port for Gradio
EXPOSE 7860

# Run Gradio app
CMD ["python", "app.py"]
