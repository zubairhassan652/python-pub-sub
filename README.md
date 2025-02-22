## Setup and Running

1.  **Clone the repository (if applicable):**

    ```bash
    git clone https://github.com/zubairhassan652/python-pub-sub
    ```
    Switch to directory
    ```
    cd python-pub-sub
    ```

2.  **Build the Docker Image:**
    ```bash
    docker build -t my-app .
    ```
    If you are using `windows subsystem for linux` and and facing network issue use below command

    ```bash
    docker build -t my-app --network=host .
    ```

3.  **Run the Docker Container:**

    ```bash
    docker run -p 5000:5000 -t my-app
    ```

    The `-t` flag is crucial for `tmux` to work correctly.

4.  **Access the Flask App:**

    Open your web browser and navigate to `http://localhost:5000`.

5.  **Publish Events:**

    Use the form on the web page to publish events, or send POST requests to `http://localhost:5000/publish` using `curl` or Postman:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
        "type": "UserLoggedIn",
        "data": {
            "user_id": 123,
            "username": "john_doe"
        }
    }' http://localhost:5000/publish
    ```

6.  **View Publisher and Subscriber Output:**

    When the container starts, you will be attached to a `tmux` session.

    * The top pane will display the output of the Flask application (publisher).
    * The bottom pane will display the output of the Redis subscriber.

    Use `tmux` commands to interact with the panes:

    * `Ctrl+b %`: Split the current pane vertically.
    * `Ctrl+b <arrow keys>`: Switch between panes.
    * `Ctrl+b c`: Create a new window.
    * `Ctrl+b d`: Detach from the `tmux` session.

7.  **Stop the Container:**

    Press `Ctrl+C` in the terminal where the container is running, or use `docker stop <container_id>`.
