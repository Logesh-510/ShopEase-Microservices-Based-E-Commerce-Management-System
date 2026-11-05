# ShopEase – Microservices-Based E-Commerce Management System

**An Enterprise-Level E-Commerce Backend Application Built Using Microservices Architecture**

## Project Overview

ShopEase is a microservices-based e-commerce management system developed to demonstrate the design and implementation of independent backend services.

The application separates core business functionalities into individual microservices. Each service is responsible for its own business logic, API endpoints, database operations, and deployment configuration.

The current implementation consists of two independent microservices:

- **Product Service** – Handles product creation, retrieval, updating, and deactivation.
- **Authentication Service** – Handles user registration, login, JWT authentication, token verification, and password management.

The project is designed with scalability, modularity, maintainability, and independent service deployment in mind.

## Project Objectives

- Understand and implement microservices architecture.
- Develop independent RESTful APIs using FastAPI.
- Implement database-per-service architecture.
- Integrate MySQL with SQLAlchemy ORM.
- Implement secure authentication using JWT.
- Manage database schema changes using Alembic.
- Containerize services using Docker.
- Maintain project version control using Git and GitHub.

## System Architecture

```text
                 ShopEase E-Commerce System
                           |
             +-------------+-------------+
             |                           |
      Product Service             Authentication Service
             |                           |
        FastAPI API                  FastAPI API
             |                           |
        SQLAlchemy                  SQLAlchemy
             |                           |
      MySQL Database               MySQL Database
             |                           |
    shopease_product_db           shopease_auth_db
```

Each microservice owns and manages its respective database independently.

## Repository Structure

```text
ShopEase-Microservices-Based-E-Commerce-Management-System/
│
├── shopease-product-service/
│   ├── app/
│   ├── screenshots/
│   ├── database_shopease.sql
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── shopease-auth-service/
│   ├── app/
│   ├── alembic/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── README.md
└── .gitignore
```

## Microservices Details

### 1. Product Service

**Purpose:** Manages product-related operations in the ShopEase e-commerce platform.

**Key Features:**
- Create new products.
- Retrieve individual product details.
- Retrieve the product list.
- Update existing product information.
- Validate product data.
- Deactivate products using soft deletion.
- Maintain independent product database ownership.

**Technologies:**
- Python
- FastAPI
- MySQL
- SQLAlchemy ORM
- Pydantic
- Docker

**API Base Path:** `/api/v1/products`

**Development Port:** `8001`

### 2. Authentication Service

**Purpose:** Manages user identity, authentication, and secure access to the application.

**Key Features:**
- User registration.
- Email uniqueness validation.
- Password hashing using bcrypt.
- User login.
- JWT access-token generation.
- JWT token verification.
- Protected current-user endpoint.
- Password change functionality.
- User active/inactive status management.
- Database schema management using Alembic.

**Technologies:**
- Python
- FastAPI
- MySQL
- SQLAlchemy ORM
- Alembic
- Pydantic
- JWT
- Passlib and bcrypt
- Docker

**API Endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate a user |
| GET | `/api/auth/me` | Retrieve authenticated user details |
| POST | `/api/auth/verify-token` | Verify JWT access token |
| POST | `/api/auth/change-password` | Change user password |

**Development Port:** `8002`

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | MySQL 8 |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| Data Validation | Pydantic |
| Authentication | JWT |
| Password Security | bcrypt |
| API Documentation | Swagger UI |
| API Client | Postman |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Version Control | Git and GitHub |

## Database Architecture

ShopEase follows the **Database Per Service** architectural pattern.

- Product Service independently manages `shopease_product_db`.
- Authentication Service independently manages `shopease_auth_db`.
- Each service maintains its own database connection and data operations.
- Services do not directly share database tables.

This approach reduces database coupling and allows independent service development and deployment.

## Docker Deployment

Docker is used to containerize the microservices and their database dependencies.

The Authentication Service includes:
- Dedicated MySQL 8 container.
- Dedicated Authentication Service container.
- Docker Compose configuration.
- MySQL health check.
- Persistent named database volume.
- Environment-based configuration.

To start the Authentication Service:

```powershell
cd shopease-auth-service
docker compose up -d --build
```

Refer to each service's individual README for its setup and deployment instructions.

## Environment Configuration

Application secrets and database credentials are maintained using environment variables.

The repository provides `.env.example` templates where applicable.

Actual `.env` files are excluded from Git to protect sensitive information.

Before deployment, configure the required environment variables using the respective service documentation.

## API Documentation

FastAPI automatically provides interactive API documentation through Swagger UI.

Once a service is running, access its documentation using:

- Product Service: `http://localhost:8001/docs`
- Authentication Service: `http://localhost:8002/docs`

## Future Enhancements

The following capabilities can be introduced as the platform evolves:

- API Gateway integration.
- Service-to-service communication.
- Order Management Service.
- Payment Service.
- Inventory Management Service.
- Centralized logging and monitoring.
- Distributed tracing.
- Service discovery.

## Project Author

**Logesh S M**

## GitHub Repository

[ShopEase – Microservices-Based E-Commerce Management System](https://github.com/Logesh-510/ShopEase-Microservices-Based-E-Commerce-Management-System)

---

*Developed as an enterprise-level backend and microservices architecture learning project.*
