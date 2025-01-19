# URL Shortener API

This API allows users to create shortened URLs, retrieve original URLs using the shortened version, and access analytics about URL usage. Built with FastAPI, it supports features like password protection, expiration, and logging access details.

## Table of Contents

- [Features](#features)
- [Endpoints](#endpoints)
  - [Shorten URL](#shorten-url)
  - [Redirect to Original URL](#redirect-to-original-url)
  - [Analytics](#analytics)
- [Request and Response Models](#request-and-response-models)
- [Error Handling](#error-handling)
- [Setup Instructions](#setup-instructions)

---

## Features

- Shorten any URL with an optional password and expiry time.
- Retrieve the original URL using the shortened URL.
- Protect shortened URLs with a password.
- Track access logs for analytics.
- Expiry-based URL invalidation.

---

## Endpoints

### Shorten URL

**URL:** `api/v1/url_shortener/shorten`

**Method:** `POST`

**Description:** Create a shortened version of a given URL with an optional password and expiry time.

**Request Body:**

```json
{
  "url": "https://example.com",
  "password": "myPassword123",
  "expiry_hours": 24
}
```

**Response:**

- **Success:**

```json
{
  "message": "Updated Successfully",
  "success": true,
  "data": "https://short.ly/<shortened_url>"
}
```

- **Failure:**

```json
{
  "message": "<error message>",
  "success": false,
  "data": null
}
```

---

### Redirect to Original URL

**URL:** `api/v1/url_shortener/`

**Method:** `GET`

**Description:** Retrieve the original URL using the shortened URL.

**Query Parameters:**

- `short_url` (string, required): The shortened URL.
- `password` (string, optional): Password if the URL is protected.

**Response:**

- **Success:**

```json
{
  "message": "URL found",
  "success": true,
  "data": "https://example.com"
}
```

- **Failure:**

```json
{
  "message": "<error message>",
  "success": false
}
```

---

### Analytics

**URL:** `api/v1/url_shortener/analytics/`

**Method:** `GET`

**Description:** Retrieve analytics for a shortened URL, including access logs.

**Query Parameters:**

- `short_url` (string, required): The shortened URL.

**Response:**

- **Success:**

```json
{
  "message": "Data found",
  "success": true,
  "data": {
    "log_count": 5,
    "logs": [
      {
        "short_url": "https://short.ly/<shortened_url>",
        "timestamp": "2023-01-01T12:00:00",
        "ip_address": "192.168.1.1"
      }
    ]
  }
}
```

- **Failure:**

```json
{
  "message": "Data not found",
  "success": false,
  "data": null
}
```

---

## Request and Response Models

### Request Models

1. **Shorten URL Request:**

```json
{
  "url": "string",
  "password": "string",
  "expiry_hours": "integer"
}
```

2. **Redirect Request:**

Query parameters:

- `short_url`: string
- `password`: string (optional)

3. **Analytics Request:**

Query parameters:

- `short_url`: string

### Response Models

1. **Success Response:**

```json
{
  "message": "string",
  "success": true,
  "data": "object or string"
}
```

2. **Failure Response:**

```json
{
  "message": "string",
  "success": false,
  "data": null
}
```

---

## Error Handling

- **Invalid Password:** Returned when the password provided does not match.
- **URL Expired:** Returned if the expiration time has passed.
- **Short URL Not Found:** Returned when the shortened URL does not exist.
- **Database Errors:** Handled gracefully with error messages in the response.

---

## Setup Instructions

1. **Install Dependencies:**

   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the Server:**

   ```bash
   uvicorn app.main:app --reload --port 3002
   ```


