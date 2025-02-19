# Flask URL Shortener API

This project consists of two Flask-based microservices: an authentication service (AuthService) for user management and JWT authentication, and a URL shortener service (URLShortenerService) that allows users to shorten, retrieve, update, and delete URLs securely. JWT authentication ensures that only authorized users can manage their URLs.

## Setup Instructions

### 1️. Clone the Repository

```sh
git clone https://github.com/ahmetkarapinar/WebServicesAssignment2.git
```

### 2️. Set Up a Virtual Environment

```sh
python -m venv .venv  # Create virtual environment
source .venv/Scripts/activate  # Activate it (Windows)
source venv/bin/activate # Activate it (macOS/Linux)
```

### 3️. Install Dependencies

```sh
pip install -r requirements.txt
pip install psycopg2-binary
pip install validators
```

### 4. Start the DB with Docker Compose

```sh
docker-compose up --build -d
```

## Running the Flask API Locally

```sh
python run.py
```

AuthService (Authentication & JWT Management) → Accessible at http://127.0.0.1:5001/
URLShortenerService (URL Shortening & Management) → Accessible at http://127.0.0.1:5000/

## Code Sources

URL validator: https://yozachar.github.io/pyvalidators/stable/api/url/

We used the source code below to come up with the shortening algorithm.
Shortening algorithm: https://play.golang.com/p/DmFYZXWdzDU

This JWT implementation was manually written, taking inspiration from Stack Overflow but modified to match our requirements.
Adam DS, "Python manually create jwt token without library", Stack Overflow, Oct 29, 2021. Available: https://stackoverflow.com/questions/68274543/python-manually-create-jwt-token-without-library.

## 📌 API Endpoints

## 🚀 API Endpoints

### AuthService (`http://127.0.0.1:5001/`)

| **Method** | **Endpoint**       | **Description**                  |
| ---------- | ------------------ | -------------------------------- |
| `POST`     | `/users`           | Register a new user              |
| `POST`     | `/users/login`     | Authenticate user & return JWT   |
| `PUT`      | `/users`           | Update user password             |
| `POST`     | `/users/validate`  | Validate JWT from other services |
| `GET`      | `/users/protected` | Protected route                  |

---

### URLShortenerService (`http://127.0.0.1:5000/`)

| **Method** | **Endpoint** | **Description**                 |
| ---------- | ------------ | ------------------------------- |
| `POST`     | `/`          | Create a short URL              |
| `GET`      | `/`          | Retrieve all URL pairs          |
| `GET`      | `/<id>`      | Retrieve full URL from short ID |
| `PUT`      | `/<id>`      | Update an existing short URL    |
| `DELETE`   | `/<id>`      | Delete a short URL              |
