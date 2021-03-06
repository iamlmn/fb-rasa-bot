# Extend the official Rasa SDK image
FROM rasa/rasa_sdk:latest

# Add a custom system library (e.g. git)
RUN apt-get update && \
    apt-get install -y git

# Add a custom python library (e.g. jupyter)
RUN pip install --no-cache-dir jupyter