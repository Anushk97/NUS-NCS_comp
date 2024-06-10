#!/bin/sh

# Start Nginx in the background
service nginx start

export OPENAI_API_KEY=$(cat /app/gradio-app/.config.json | jq -r '.OPENAI_API_KEY')

# Start the Gradio app
python /app/app.py
