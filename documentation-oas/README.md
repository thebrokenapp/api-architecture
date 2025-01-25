# Payments API Documentation

## Overview
The Payments API allows you to manage payment transactions, including creating, retrieving, updating, and deleting records. It uses SQLite as the primary database and Redis for caching to improve performance.

---

## Base URL
```
http://<host>:8001
```

---

## Endpoints

### 1. **API Status**
**Endpoint:** `/payments/apiStatus`
- **Method:** `GET`
- **Description:** Checks if the API is running.
- **Response:**
  ```json
  {
    "message": "Payments API is up!"
  }
  ```

---

### 2. **Create Payment**
**Endpoint:** `/payments`
- **Method:** `POST`
- **Description:** Creates a new payment transaction.
- **Request Body:**
  ```json
  {
    "user_name": "<string, min 5, max 30 characters>",
    "amount": <integer, greater than 0, less than 100000>,
    "payer_upi": "<string, min 5, max 30 characters>",
    "payee_upi": "<string, min 5, max 30 characters>",
    "note": "<optional string>"
  }
  ```
- **Response:**
  ```json
  {
    "message": "transaction created",
    "transaction_id": "<UUID>"
  }
  ```

---

### 3. **Get Payments for a User**
**Endpoint:** `/payments/<user_name>`
- **Method:** `GET`
- **Description:** Retrieves payments for a specific user, filtered by status and minimum amount.
- **Query Parameters:**
  - `status` (optional, default: `initiated`): Filter by transaction status.
  - `amount` (optional, default: `0`): Filter by minimum transaction amount.
- **Response:**
  ```json
  {
    "payment_list": [
      {
        "user_name": "<string>",
        "amount": <integer>,
        "status": "<string>",
        "payer_upi": "<string>",
        "payee_upi": "<string>",
        "note": "<string>",
        "timestamp": "<ISO 8601 UTC timestamp>"
      }
    ]
  }
  ```

---

### 4. **Get Payment by Transaction ID**
**Endpoint:** `/payments/transaction/<transaction_id>`
- **Method:** `GET`
- **Description:** Retrieves a payment by its transaction ID, with Redis caching.
- **Response:**
  ```json
  {
    "transaction_id": "<UUID>",
    "user_name": "<string>",
    "amount": <integer>,
    "status": "<string>",
    "payer_upi": "<string>",
    "payee_upi": "<string>",
    "note": "<string>",
    "timestamp": "<ISO 8601 UTC timestamp>"
  }
  ```

---

### 5. **Update Payment Status**
**Endpoint:** `/payments/<transaction_id>`
- **Method:** `PATCH`
- **Description:** Updates the status of a specific transaction.
- **Request Body:**
  ```json
  {
    "status": "<string>"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Transaction updated"
  }
  ```
- **Error Response:**
  ```json
  {
    "message": "Transaction not found"
  }
  ```

---

### 6. **Delete Payment**
**Endpoint:** `/payments/<transaction_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific transaction by its ID.
- **Response:**
  ```json
  {
    "message": "Transaction deleted!"
  }
  ```
- **Error Response:**
  ```json
  {
    "message": "Transaction not found"
  }
  ```

---

### 7. **Get All Payments**
**Endpoint:** `/payments`
- **Method:** `GET`
- **Description:** Retrieves all payment records with pagination.
- **Query Parameters:**
  - `page` (optional, default: `1`): Page number.
  - `size` (optional, default: `3`): Number of records per page.
- **Response:**
  ```json
  {
    "payments": [
      {
        "transaction_id": "<UUID>",
        "user_name": "<string>",
        "amount": <integer>,
        "status": "<string>",
        "payer_upi": "<string>",
        "payee_upi": "<string>",
        "note": "<string>",
        "timestamp": "<ISO 8601 UTC timestamp>"
      }
    ],
    "page": <integer>
  }
  ```

---

## Error Handling
### 1. **404 Not Found**
- **Response:**
  ```json
  {
    "error": "Resource Not Found!"
  }
  ```

### 2. **405 Method Not Allowed**
- **Response:**
  ```json
  {
    "error": "This method is not allowed"
  }
  ```

---

## Database Schema
### `payments` Table
| Column          | Type          | Description                           |
|-----------------|---------------|---------------------------------------|
| `transaction_id`| TEXT (UUID)   | Unique identifier for the transaction |
| `user_name`     | TEXT          | Name of the user                      |
| `amount`        | INTEGER       | Payment amount                        |
| `status`        | TEXT          | Transaction status                    |
| `payer_upi`     | TEXT          | Payer UPI ID                          |
| `payee_upi`     | TEXT          | Payee UPI ID                          |
| `note`          | TEXT          | Optional transaction note             |
| `timestamp`     | DATETIME      | Transaction timestamp                 |

---

## Redis Caching
- Transaction data is cached in Redis using the `transaction_id` as the key.
- Cache is invalidated on updates or deletions.

---

## Running the Application
- Start the server:
  ```bash
  python app.py
  ```
- Default host: `0.0.0.0`
- Default port: `8001`

---

## Dependencies
- Flask
- Flask-Pydantic
- SQLite3
- Redis
- Pydantic

---

## Notes
- Ensure Redis is running on `localhost:6379`.
- SQLite database (`upi.db`) must be pre-configured with the `payments` table.

