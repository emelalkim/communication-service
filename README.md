# Communication Microservice

This is a basic communication microservice built with Flask and SQLAlchemy. The microservice allows sending messages through multiple channels (e.g., email, SMS) and logs each message’s delivery status in a database. It provides endpoints for sending messages and viewing message logs, with optional filtering by date.

## Features

- **Message Sending**: `/sendMessage` endpoint to send messages via specified channels (currently supports mock email and SMS).
- **Message Logging**: Logs each message’s delivery status and timestamp in a SQLite database.
- **Message Retrieval**: `/messageLog` endpoint to retrieve message logs, with optional filtering by start and end dates.

## Technologies Used

- **Flask**: Web framework for building the microservice.
- **SQLAlchemy**: ORM for database interactions.
- **SQLite**: Database for local persistence.
- **pytest**: Testing framework for unit tests.

## Setup and Installation

### Prerequisites

- Python 3.9 or higher

### 1. Clone the Repository

```bash
git clone https://github.com/emelalkim/communication-microservice.git
cd communication-microservice
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Send a Message

- **URL**: `/sendMessage`
- **Method**: `POST`
- **Payload**:
  - `type`: The type of message (e.g., `"email"` or `"sms"`).
  - `recipient`: The recipient’s email or phone number.
  - `content`: The message content.
  
- **Example**:
  
  ```json
  {
    "type": "email",
    "recipient": "user@example.com",
    "content": "Hello, this is a test message."
  }
  ```

- **Response**:
  - `status`: Indicates success or failure of message delivery.
  - **Example**:
    ```json
    {
      "status": "Success"
    }
    ```

### 2. Retrieve Message Logs

- **URL**: `/messageLog`
- **Method**: `GET`
- **Query Parameters**:
  - `start`: (Optional) Start date for filtering logs, in `YYYY-MM-DD` format.
  - `end`: (Optional) End date for filtering logs, in `YYYY-MM-DD` format.

- **Response**:
  - A list of logged messages, each with:
    - `id`
    - `type`
    - `recipient`
    - `content`
    - `status`
    - `timestamp`

- **Example**:
  ```json
  [
    {
      "id": 1,
      "type": "email",
      "recipient": "user@example.com",
      "content": "Hello, this is a test message.",
      "status": "Success",
      "timestamp": "2024-11-05 12:34:56"
    }
  ]
  ```

## Testing

The project includes unit tests written with `pytest`. To run the tests:

```bash
pytest
```

Tests cover:
- Validation for `/sendMessage` payload.
- Filtering functionality for `/messageLog`.

## Project Structure

```plaintext
communication_service/
├── app/
│   ├── __init__.py        # Application factory and app initialization
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database setup and configuration
│   ├── mock_send.py       # Mock functions for message sending
│   └── models.py          # Message logging model
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Configuration settings for tests
│   └── test_app.py        # Unit tests for endpoints
├── Dockerfile             # Docker image creation file
├── pytest.ini             # Configuration for pytest
├── README.md              # Project README
├── requirements.txt       # Project dependencies
└── run.py                 # Entry point to run the application
```

## Dockerization

This project is containerized with Docker to simplify deployment and ensure a consistent environment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system.

### Building the Docker Image

To build the Docker image, navigate to the project root (`communication_service/`) and run the following command:

```bash
docker build -t communication_service .
```

This command will:
- Use the `Dockerfile` to create an image named `communication_service`.
- Install dependencies specified in `requirements.txt`.
- Set up the application to be ready for deployment in a production-like environment using `gunicorn`.

### Running the Docker Container

After building the image, you can run the application in a container using:

```bash
docker run \                                
  -p 5000:5000 -d \
  -v /local/path/to/db:/app/db \
  --name communication_service \
  communication_service
```

This command will:
- Start the container in detached mode (`-d`).
- Connect a docker volume for the database. Edit /local/path/to/db to point to a local directory where the database can be placed
- Map port `5000` on your local machine to port `5000` in the container, making the application accessible at `http://localhost:5000`.

### Stopping the Docker Container

To stop the running container, list the containers to find the container ID:

```bash
docker ps
```

Then, stop the container with:

```bash
docker stop <container_id>
```

### Testing in the Docker Environment

To run tests inside the Docker container, you can use the following command:

```bash
docker exec -it <container_id> pytest
```

This command will:
- Execute `pytest` within the running container, allowing you to verify functionality in the Docker environment.
