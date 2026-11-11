# ShopEase – User Management Microservice

**A FastAPI-based User Management Microservice for the ShopEase E-Commerce Platform**

## 1. Project Overview

The ShopEase User Management Service is an independent microservice responsible for managing customer profiles and delivery addresses within the ShopEase e-commerce application.

It follows a **Microservices Architecture** and **Database Per Service** design pattern, ensuring independent development, deployment, scalability, and database ownership.

The service integrates with the Authentication Service to validate JWT access tokens and securely identify authenticated users.

## 2. Key Features

- Create and manage customer profiles.
- Retrieve authenticated user profile information.
- Update profile details.
- Deactivate user profiles.
- Create, retrieve, update, and delete delivery addresses.
- Support HOME, WORK, and OTHER address types.
- Manage default delivery addresses.
- Validate incoming requests using Pydantic.
- Secure API endpoints using JWT authentication.
- Communicate with the Authentication Service using HTTPX.
- Maintain an independent MySQL database.
- Manage database migrations using Alembic.
- Containerize the application using Docker.

## 3. Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python 3.13 |
| Backend Framework | FastAPI |
| Database | MySQL 8 |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| Data Validation | Pydantic |
| Authentication | JWT |
| HTTP Communication | HTTPX |
| API Documentation | Swagger UI |
| Testing | Pytest |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Version Control | Git and GitHub |

## 4. Microservices Architecture

ShopEase follows a microservices architecture where each service handles a specific business responsibility.

| Microservice | Responsibility | Port | Database |
|---|---|---:|---|
| Product Service | Product management | 8001 | shopease_product_db |
| Authentication Service | Registration, login and JWT authentication | 8002 | shopease_auth_db |
| User Service | User profiles and address management | 8003 | shopease_user_db |

### Service Communication

- The Authentication Service manages user credentials and JWT token generation.
- The User Service manages customer profile and address information.
- The User Service communicates with the Authentication Service to verify JWT tokens.
- Each microservice maintains its own database.
- Services do not directly access another service's database.

## 5. Project Structure

```text
shopease-user-service/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   └── address_model.py
│   │
│   ├── routers/
│   │   ├── user_routes.py
│   │   └── address_routes.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── address_schema.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── address_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_address_schema.py
│   └── test_address_service.py
│
├── .dockerignore
├── .env.example
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 6. Database Design

The User Service uses its own MySQL database:

**Database Name:** `shopease_user_db`

### Users Table

Stores customer profile information.

| Column | Description |
|---|---|
| id | Primary key |
| auth_user_id | Authentication Service user ID |
| full_name | Customer full name |
| phone_number | Contact number |
| date_of_birth | Date of birth |
| gender | Gender |
| profile_image | Profile image reference |
| is_active | Account profile status |
| created_at | Record creation timestamp |
| updated_at | Last update timestamp |

### Addresses Table

Stores customer delivery address information.

| Column | Description |
|---|---|
| id | Primary key |
| user_id | Foreign key referencing users |
| address_type | HOME, WORK, or OTHER |
| full_name | Recipient name |
| phone_number | Contact number |
| address_line_1 | Primary address |
| address_line_2 | Additional address details |
| city | City |
| state | State |
| country | Country |
| postal_code | Postal code |
| is_default | Default address indicator |
| created_at | Record creation timestamp |

Each user can maintain multiple delivery addresses.

## 7. API Endpoints

**Base URL:** `http://127.0.0.1:8003`

**API Base Path:** `/api/v1/users`

### User Profile APIs

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/users/profile` | Create user profile |
| GET | `/api/v1/users/profile` | Retrieve user profile |
| PUT | `/api/v1/users/profile` | Update user profile |
| PATCH | `/api/v1/users/profile/deactivate` | Deactivate user profile |

### Address Management APIs

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/users/addresses` | Create new address |
| GET | `/api/v1/users/addresses` | Retrieve all user addresses |
| GET | `/api/v1/users/addresses/{address_id}` | Retrieve a specific address |
| PUT | `/api/v1/users/addresses/{address_id}` | Update address |
| DELETE | `/api/v1/users/addresses/{address_id}` | Delete address |
| PATCH | `/api/v1/users/addresses/{address_id}/default` | Set default address |

### Health Check

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service welcome endpoint |
| GET | `/health` | Service health status |

## 8. Authentication and Security

The User Service uses JWT-based authentication through the Authentication Service.

### Authentication Flow

1. The user logs in through the Authentication Service.
2. The Authentication Service generates a JWT access token.
3. The client sends the token in the Authorization header.
4. The User Service forwards the token to the Authentication Service for verification.
5. The Authentication Service validates the token.
6. The User Service retrieves the corresponding user profile using the verified user ID.

**Authorization Header:**

```http
Authorization: Bearer <access_token>
```

The User Service does not store user passwords or independently generate authentication tokens.

## 9. Installation and Setup

### Prerequisites

- Python 3.13 or compatible version
- MySQL 8
- Docker Desktop
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Logesh-510/ShopEase-Microservices-Based-E-Commerce-Management-System.git
```

### Step 2: Navigate to the User Service

```bash
cd ShopEase-Microservices-Based-E-Commerce-Management-System/shopease-user-service
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Configure the following variables:

```env
APP_NAME=ShopEase User Management Service
APP_ENV=development

DB_HOST=localhost
DB_PORT=3306
DB_NAME=shopease_user_db
DB_USER=your_database_user
DB_PASSWORD=your_database_password

AUTH_SERVICE_URL=http://127.0.0.1:8002
AUTH_VERIFY_TIMEOUT_SECONDS=5
```

Replace the database credentials with your local configuration.

**Security:** Never commit the actual `.env` file or expose passwords, JWT secrets, or access tokens.

## 10. Database Migration

Create the database in MySQL if it does not already exist:

```sql
CREATE DATABASE shopease_user_db;
```

Apply database migrations:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

## 11. Running the Application

Start the User Service:

```bash
uvicorn app.main:app --reload --port 8003
```

The application will run at:

- **Service URL:** http://127.0.0.1:8003
- **Health Check:** http://127.0.0.1:8003/health
- **Swagger Documentation:** http://127.0.0.1:8003/docs
- **OpenAPI Schema:** http://127.0.0.1:8003/openapi.json

## 12. Docker Deployment

Build the Docker image:

```bash
docker compose build
```

Apply database migrations:

```bash
docker compose run --rm user-service alembic upgrade head
```

Start the service:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs --tail 30 user-service
```

Stop the service:

```bash
docker compose down
```

The Docker configuration connects to the existing MySQL and Authentication Service instances through `host.docker.internal`.

## 13. Testing

The project uses Pytest for automated testing.

Run all tests:

```bash
pytest -q
```

### Testing Coverage

- Address schema validation.
- Invalid address data rejection.
- Phone number validation.
- Address creation and retrieval.
- Address ownership validation.
- Default address management.
- Address update and deletion behavior.

### Test Results

**21 automated tests passed successfully.**

Additional manual API verification covered profile CRUD, JWT authentication, address management, MySQL connectivity, and Docker health checks.

## 14. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created successfully |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |
| 500 | Internal server error |
| 502 | Invalid upstream response |
| 503 | Dependent service unavailable |

## 15. Future Enhancements

- API Gateway integration.
- Centralized logging and monitoring.
- Distributed tracing.
- Improved concurrent default-address management.
- Expanded integration and profile service tests.
- Notification Service integration.
- User profile image storage integration.

## 16. Project Objective

This microservice was developed as part of the ShopEase Microservices-Based E-Commerce Management System to demonstrate practical implementation of:

- Microservices architecture.
- RESTful API development.
- Database-per-service architecture.
- SQLAlchemy ORM integration.
- JWT authentication and service-to-service communication.
- Database migration management.
- Automated testing.
- Docker-based deployment.

---

- **Project:** ShopEase – Microservices-Based E-Commerce Management System
- **Module:** User Management Service
- **Developer:** Logesh S M
- **Repository:** [ShopEase GitHub Repository](https://github.com/Logesh-510/ShopEase-Microservices-Based-E-Commerce-Management-System)