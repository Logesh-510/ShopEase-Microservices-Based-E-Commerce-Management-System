# ShopEase Product Service

An independent Product Management microservice built using FastAPI and Docker. It provides REST APIs to create, retrieve, update, delete, filter, and paginate product information.

## Technology Stack

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- Docker
- In-memory data storage

## Project Structure

```text
shopease-product-service/
│
├── app/
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   ├── models/
│   │   └── product_model.py
│   ├── routers/
│   │   └── product_routes.py
│   ├── schemas/
│   │   └── product_schema.py
│   └── services/
│       └── product_service.py
│
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Features

- Create, retrieve, update, and delete products.
- Retrieve all products.
- Filter products by category.
- Pagination using `skip` and `limit`.
- Pydantic request validation.
- HTTP exception handling.
- Automatic product ID generation.
- Temporary in-memory product storage.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/products/` | Create product |
| GET | `/api/products/` | List products |
| GET | `/api/products/{product_id}` | Get product by ID |
| PUT | `/api/products/{product_id}` | Update product |
| DELETE | `/api/products/{product_id}` | Delete product |

## Run Locally

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
uvicorn app.main:app --reload --port 8003
```

The service runs at:

`http://localhost:8003`

## Docker Deployment

### 1. Build the Docker image

```bash
docker build -t shopease-product-service .
```

### 2. Run the container

```bash
docker run -d --name shopease-product-container -p 8003:8003 shopease-product-service
```

### 3. Check the running container

```bash
docker ps
```

### 4. View container logs

```bash
docker logs shopease-product-container
```

## API Documentation

FastAPI provides interactive Swagger documentation.

Swagger UI:

`http://localhost:8003/docs`

ReDoc:

`http://localhost:8003/redoc`

These pages allow developers to explore the available API endpoints and their request and response schemas.

## Testing

API documentation is available through Swagger UI at `/docs`. The endpoints and validation schemas can be inspected there.

## Data Storage

This service uses temporary in-memory storage. Product data is cleared when the application restarts. No external database is used in this implementation.

## Author

ShopEase Product Service Project