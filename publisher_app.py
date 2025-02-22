# publisher_app.py (using Flask)
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Redis connection details (same as before)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_CHANNEL = 'my_channel'

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    print("Publisher app connected to Redis.")
except redis.ConnectionError as e:
    print(f"Publisher app connection error: {e}")
    exit(1)


def publish_event(event_data):
    try:
        message = f"Event: {event_data}"
        r.publish(REDIS_CHANNEL, message)
        print(f"Published: {message}")
        return True  # Indicate success
    except redis.RedisError as e:
        print(f"Publishing error: {e}")
        return False # Indicate failure


@app.route('/publish', methods=['POST'])
def publish_endpoint():
    try:
        data = request.get_json()  # Get event data from the request body
        if not data:
            return jsonify({"error": "No event data provided"}), 400

        event_type = data.get('type')
        event_data = data.get('data')

        if not event_type or not event_data:
            return jsonify({"error": "Missing 'type' or 'data' in event data"}), 400

        event = {"type": event_type, "data": event_data}

        if publish_event(event):
            return jsonify({"message": "Event published successfully"}), 200
        else:
            return jsonify({"error": "Failed to publish event"}), 500

    except Exception as e:
        print(f"Error in publish_endpoint: {e}")
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run Flask app on port 5000