## Setup and Running

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <your_repository_url>
    cd <your_project_directory>
    ```

2.  **Create `requirements.txt`:**

    Ensure you have a `requirements.txt` file listing all Python dependencies. If not, create one:

    ```bash
    pip freeze > requirements.txt
    ```

3.  **Build the Docker Image:**

    ```bash
    docker build -t my-app .
    ```

4.  **Run the Docker Container:**

    ```bash
    docker run -p 5000:5000 -t my-app
    ```

    The `-t` flag is crucial for `tmux` to work correctly.

5.  **Access the Flask App:**

    Open your web browser and navigate to `http://localhost:5000`.

6.  **Publish Events:**

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

7.  **View Publisher and Subscriber Output:**

    When the container starts, you will be attached to a `tmux` session.

    * The top pane will display the output of the Flask application (publisher).
    * The bottom pane will display the output of the Redis subscriber.

    Use `tmux` commands to interact with the panes:

    * `Ctrl+b %`: Split the current pane vertically.
    * `Ctrl+b <arrow keys>`: Switch between panes.
    * `Ctrl+b c`: Create a new window.
    * `Ctrl+b d`: Detach from the `tmux` session.

8.  **Stop the Container:**

    Press `Ctrl+C` in the terminal where the container is running, or use `docker stop <container_id>`.
