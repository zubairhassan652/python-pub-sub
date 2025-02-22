# publisher.py
import redis
import time
import random

# Redis connection details
REDIS_HOST = 'localhost'  # Replace with your Redis host
REDIS_PORT = 6379       # Replace with your Redis port
REDIS_CHANNEL = 'my_channel'

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    print("Publisher connected to Redis.")
except redis.ConnectionError as e:
    print(f"Publisher connection error: {e}")
    exit(1)

def publish_event(event_data):
    try:
        message = f"Event: {event_data}"
        r.publish(REDIS_CHANNEL, message)
        print(f"Published: {message}")
    except redis.RedisError as e:
        print(f"Publishing error: {e}")

if __name__ == "__main__":
    while True:
        event_type = random.choice(["UserLoggedIn", "ProductViewed", "OrderPlaced"])
        event_data = {"type": event_type, "data": {"user_id": random.randint(1, 100), "value": random.random()}}

        publish_event(event_data)
        time.sleep(2)  # Publish every 2 seconds