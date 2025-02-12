# Flask URL Shortener API

This is a simple **Flask-based REST API** for shortening URLs.

## Setup Instructions

### 1️. Clone the Repository

```sh
git clone https://github.com/aditya-130/WebServicesAssignment1.git
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

API is accesible at **http://127.0.0.1:5000/**.

## Code Sources

URL validator: https://yozachar.github.io/pyvalidators/stable/api/url/

We used the source code below to come up with the shortening algorithm.
Shortening algorithm: https://play.golang.com/p/DmFYZXWdzDU

## 📌 API Endpoints

| **Method** | **Endpoint** | **Description**                 |
| ---------- | ------------ | ------------------------------- |
| `POST`     | `/`          | Create a short URL              |
| `GET`      | `/`          | Retrieve all URL pairs          |
| `GET`      | `/<id>`      | Retrieve full URL from short ID |
| `PUT`      | `/<id>`      | Update an existing short URL    |
| `DELETE`   | `/<id>`      | Delete a short URL              |

