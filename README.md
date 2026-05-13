# Rating Microservice

## Table of Contents
- [Rating Microservice](#rating-microservice)
   * [Overview](#overview)
   * [Data Model](#data-model)
   * [Features](#features)
   * [Setup](#setup)
   
- [API Usage](#api-usage)
   * [POST /ratings](#post-ratings)
   * [GET /ratings](#get-ratings)
   * [DELETE /ratings](#delete-ratings)

## Overview
A minimal generic rating microservice built with FastAPI and SQLite.

It supports multiple applications by storing ratings under:
- app_id
- entity_id
- user_id

Each user can only have one rating per entity per app. New submissions overwrite existing ones (upsert behavior).

## Data Model

Each rating record:
- app_id (string)
- entity_id (string)
- user_id (string)
- rating (integer)
- comment (optional string)

Primary key:
(app_id, entity_id, user_id)

## Features
- Upsert rating (create or overwrite automatically)
- Fetch all ratings for an entity
- Delete a specific user rating
- SQLite storage (no external DB required)


## Setup

### Install dependencies
```bash
pip install -r requirements.txt
```

# API Usage

## POST /ratings
Creates or updates a rating (upsert). If a rating already exists for the same `app_id`, `entity_id`, or `user_id`, it is overwritten.

### Route
```HTTP
POST /ratings
```

### Example Request
```Bash
curl -X POST http://127.0.0.1:8000/ratings \
-H "Content-Type: application/json" \
-d '{
  "app_id": "book_club",
  "entity_id": "harry_potter_1",
  "user_id": "user123",
  "rating": 5,
  "comment": "Excellent book"
}'
```

### Example Response
```JSON
{
  "status":"upserted"
}
```

## GET /ratings
Retrieves all ratings for a specific entity within the database.

### Route
```HTTP
GET /ratings?app_id={app_id}&entity_id={entity_id}
```

### Example Request
```Bash
curl "http://127.0.0.1:8000/ratings?app_id=book_club&entity_id=harry_potter_1"
```

### Example Response
```JSON
{
  "app_id": "book_club",
  "entity_id": "harry_potter_1",
  "ratings": [
    ["user123", 5, "Excellent book"],
    ["user456", 4, "Good read"]
  ]
}
```

## DELETE /ratings
Retrieves all ratings for a specific entity within the database.

### Route
```HTTP
DELETE /ratings?app_id={app_id}&entity_id={entity_id}&user_id={user_id}
```

### Example Request
```Bash
curl -X DELETE "http://127.0.0.1:8000/ratings?app_id=book_club&entity_id=harry_potter_1&user_id=user123"
```

### Example Response
```JSON
{
  "status": "deleted"
}
```