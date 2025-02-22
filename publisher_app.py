# publisher_app.py (using Flask)
import sys
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import redis
import subprocess
import threading
import queue

app = Flask(__name__)
socketio = SocketIO(app)


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



# ... (Redis connection details and publish_event function - same as before)

output_queue = queue.Queue()

def capture_subscriber_output(output_queue):
    python_path = sys.executable
    print(f"Using Python interpreter: {python_path}") #Add this line
    try:
        # python_path = sys.executable  # Get the path to the current Python interpreter
        process = subprocess.Popen(
            [python_path, "subscriber.py"],  # Use the virtual environment's Python
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    except Exception as e:
        print(f"Error starting subscriber process: {e}")
        return
    
    def read_output():
        print("read_output thread started")
        try: # Add try catch block to catch any errors.
            for line in process.stdout:
                print(f"Read line: {line.strip()}")
                output_queue.put(line.strip())
                socketio.emit('subscriber_output', {'data': line.strip()})
                print(f"Emitted line: {line.strip()}")
            print("read_output loop finished") #Check if the loop ever finishes.
        except Exception as e:
            print(f"Error in read_output: {e}") #Check for any errors.
        print("read_output thread finished")
        process.wait()


    thread = threading.Thread(target=read_output)
    thread.daemon = True
    print(f"Starting thread....")
    thread.start()

capture_subscriber_output(output_queue)


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


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)  # Run Flask app on port 5000
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)