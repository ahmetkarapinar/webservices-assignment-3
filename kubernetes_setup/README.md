# Flask URL Shortener API

This project consists of two Flask-based microservices: an authentication service (AuthService) for user management and JWT authentication, and a URL shortener service (URLShortenerService) that allows users to shorten, retrieve, update, and delete URLs securely. JWT authentication ensures that only authorized users can manage their URLs.

AuthService (Authentication & JWT Management) → Accessible at http://145.100.130.60:30001/

URLShortenerService (URL Shortening & Management) → Accessible at http://145.100.130.60:30002/

## Code Sources

URL validator: https://yozachar.github.io/pyvalidators/stable/api/url/

We used the source code below to come up with the shortening algorithm.
Shortening algorithm: https://play.golang.com/p/DmFYZXWdzDU

This JWT implementation was manually written, taking inspiration from Stack Overflow but modified to match our requirements.
Adam DS, "Python manually create jwt token without library", Stack Overflow, Oct 29, 2021. Available: https://stackoverflow.com/questions/68274543/python-manually-create-jwt-token-without-library.

## API Endpoints

### AuthService (`http://145.100.130.60:30001/`)

| **Method** | **Endpoint**       | **Description**                  |
| ---------- | ------------------ | -------------------------------- |
| `POST`     | `/users`           | Register a new user              |
| `POST`     | `/users/login`     | Authenticate user & return JWT   |
| `PUT`      | `/users`           | Update user password             |
| `POST`     | `/users/validate`  | Validate JWT from other services |
| `GET`      | `/users/protected` | Protected route                  |

---

### URLShortenerService (`http://145.100.130.60:30002/`)

| **Method** | **Endpoint** | **Description**                 |
| ---------- | ------------ | ------------------------------- |
| `POST`     | `/`          | Create a short URL              |
| `GET`      | `/`          | Retrieve all URL pairs          |
| `GET`      | `/<id>`      | Retrieve full URL from short ID |
| `PUT`      | `/<id>`      | Update an existing short URL    |
| `DELETE`   | `/<id>`      | Delete a short URL              |
