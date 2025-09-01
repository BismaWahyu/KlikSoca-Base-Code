# Flask CRUD API with MongoDB and Socket.IO

This is a simple CRUD API built with Flask, using MongoDB as the database and Socket.IO for real-time broadcasting of changes to all connected clients.

## Accessing the API Documentation (Swagger UI)

Once the backend server is running, you can access the Swagger UI to view the API documentation and test the endpoints.

-   **URL:** [http://localhost:5000/docs](http://localhost:5000/docs)

## How to Run the Application

This project is divided into two parts: a Flask backend and a Vue.js frontend. You need to run both simultaneously.

### Backend (Flask)

1.  **Navigate to the backend directory:**

    ```bash
    cd backend

    ```

2.  **Using virtual environment (depends on your OS):**

    ````bash
    workon kliksoca
    ```

    ````

3.  **Install the Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The backend server will start on `http://localhost:5000`.

### Frontend (Vue.js)

1.  **Open a new terminal window.**

2.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

3.  **Install the Node.js dependencies:**

    ```bash
    npm install
    ```

4.  **Run the Vue.js development server:**

    ```bash
    npm run dev
    ```

    The frontend development server will start on a port, typically `http://localhost:5173`.

5.  **Open your browser** and navigate to the address provided by the frontend server (e.g., `http://localhost:5173`) to use the application.

## REST API Endpoints

### 1. Create a New User

-   **Endpoint:** `POST /users`
-   **Description:** Creates a new user in the database.

**Example Request Body (JSON):**

```json
{
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

**Example Success Response (201 Created):**

```json
{
    "message": "User created successfully!",
    "id": "63a5a5a5a5a5a5a5a5a5a5a5"
}
```

### 2. Get All Users

-   **Endpoint:** `GET /users`
-   **Description:** Retrieves a list of all users from the database.

**Example Success Response (200 OK):**

```json
[
    {
        "id": "63a5a5a5a5a5a5a5a5a5a5a5",
        "name": "John Doe",
        "email": "john.doe@example.com"
    },
    {
        "id": "63a5a5a5a5a5a5a5a5a5a5a6",
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
]
```

### 3. Get a Single User by ID

-   **Endpoint:** `GET /users/<id>`
-   **Description:** Retrieves a single user by their unique ID.

**Example Success Response (200 OK):**

```json
{
    "id": "63a5a5a5a5a5a5a5a5a5a5a5",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

**Example Error Response (404 Not Found):**

```json
{
    "message": "User not found!"
}
```

### 4. Update a User

-   **Endpoint:** `PUT /users/<id>`
-   **Description:** Updates an existing user's information.

**Example Request Body (JSON):**

```json
{
    "name": "John Doe Updated",
    "email": "john.doe.updated@example.com"
}
```

**Example Success Response (200 OK):**

```json
{
    "message": "User updated successfully!"
}
```

**Example Error Response (404 Not Found):**

```json
{
    "message": "User not found!"
}
```

### 5. Delete a User

-   **Endpoint:** `DELETE /users/<id>`
-   **Description:** Deletes a user from the database.

**Example Success Response (200 OK):**

```json
{
    "message": "User deleted successfully!"
}
```

**Example Error Response (404 Not Found):**

```json
{
    "message": "User not found!"
}
```

## Socket.IO Events

The application uses Socket.IO to broadcast changes to all connected clients. Here is the flow of events:

-   `connect`: Triggered when a new client connects to the server.
-   `disconnect`: Triggered when a client disconnects from the server.
-   `new_user`: Broadcasted when a new user is created via the `POST /users` endpoint. The message contains the new user's data.
-   `updated_user`: Broadcasted when a user is updated via the `PUT /users/<id>` endpoint. The message contains the updated user's data.
-   `deleted_user`: Broadcasted when a user is deleted via the `DELETE /users/<id>` endpoint. The message contains the ID of the deleted user.

## MongoDB Connection Configuration

The MongoDB connection is configured in the `app.py` file. You can modify the connection string to point to your MongoDB instance.

```python
# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_db']
collection = db['users']
```

In this example, the application connects to a MongoDB instance running on `localhost` at port `27017` and uses a database named `flask_db` and a collection named `users`.
