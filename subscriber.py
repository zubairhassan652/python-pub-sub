# subscriber.py
import redis
import threading

# Redis connection details (same as publisher)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_CHANNEL = 'my_channel'

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    print("Subscriber connected to Redis.")
except redis.ConnectionError as e:
    print(f"Subscriber connection error: {e}")
    exit(1)


def process_message(message):
    print(f"Subscriber {threading.current_thread().name} received: {message['data'].decode()}") # Decode from bytes

def subscribe():
    pubsub = r.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)

    for message in pubsub.listen():
        if message['type'] == 'message':  # Only process actual messages
            process_message(message)


if __name__ == "__main__":
    num_subscribers = 3  # Number of subscriber threads
    threads = []

    for i in range(num_subscribers):
        thread = threading.Thread(target=subscribe, name=f"Subscriber-{i+1}")
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join() # Keep the main thread alive