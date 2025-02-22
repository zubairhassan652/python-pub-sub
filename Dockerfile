# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the application code
COPY publisher_app.py /app/
COPY subscriber.py /app/

# Copy requirements.txt (if you have one)
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install Redis (if not already in your base image)
RUN apt-get update && apt-get install -y redis-server

# Expose the Flask port (5000) and Redis port (6379)
EXPOSE 5000
EXPOSE 6379

# ... other instructions

RUN apt-get update && apt-get install -y tmux

CMD ["/bin/bash", "-c", "tmux new-session -d 'service redis-server start && python publisher_app.py' && tmux split-window -v 'python subscriber.py' && tmux attach-session -t 0"]

# COPY start_app.sh /app/

# RUN chmod +x /app/start_app.sh

# CMD ["./start_app.sh"]

# Start Redis in the background
# CMD ["/bin/sh", "-c", "service redis-server start && python publisher_app.py & python subscriber.py"]
# CMD service redis-server start && python publisher_app.py && python subscriber.py
# CMD service redis-server start && gunicorn --bind 0.0.0.0:5000 publisher_app:app && python subscriber.py

# or if you want to run subscriber in different container
# CMD service redis-server start && gunicorn --bind 0.0.0.0:5000 publisher_app:app