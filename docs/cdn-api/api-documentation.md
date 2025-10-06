# Pipe CDN API Documentation

This document provides a comprehensive overview of the Pipe CDN API, currently based on the Pipe Network CDN Devnet deployment on Solana Devnet.

## Authentication
Most endpoints require two parameters:
- `user_id`: Unique user identifier
- `user_app_key`: User's application key

## API Categories

### Account Management APIs

#### Create User
- **Endpoint**: `/createUser`
- **Method**: POST
- **Request Body**: 
  ```json
  { "username": "string" }
  ```
- **Response**: 
  ```json
  { 
    "user_id": "string", 
    "user_app_key": "string", 
    "solana_pubkey": "string" 
  }
  ```

#### Rotate App Key
- **Endpoint**: `/rotateAppKey`
- **Method**: POST
- **Authentication**: Required
- **Request Body**:
  ```json
  { 
    "user_id": "string", 
    "user_app_key": "string" 
  }
  ```
- **Response**:
  ```json
  { 
    "user_id": "string", 
    "new_user_app_key": "string" 
  }
  ```

### File Management APIs

#### Upload File
- **Endpoint**: `/upload`
- **Method**: POST
- **Authentication**: Required
- **Query Parameters**:
  - `user_id`
  - `user_app_key`
  - `file_name`
  - `epochs` (optional)
- **Body**: File content as multipart/form-data
- **Response**: Uploaded filename

#### Download File
- **Endpoint**: `/download`
- **Method**: GET
- **Authentication**: Required
- **Query Parameters**:
  - `user_id`
  - `user_app_key`
  - `file_name`
- **Response**: File content with headers

### Wallet and Payments APIs

#### Check SOL Balance
- **Endpoint**: `/checkBalance`
- **Method**: GET
- **Authentication**: Required
- **Query Parameters**:
  - `user_id`
  - `user_app_key`
- **Response**: Balance information