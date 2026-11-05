# ShopEase Authentication Microservice

## Overview
An independent authentication microservice built using FastAPI, Python, MySQL 8, SQLAlchemy, Alembic and JWT.

## Technology Stack
- Python 3.13
- FastAPI
- MySQL 8
- SQLAlchemy ORM
- Alembic
- Pydantic
- JWT (python-jose)
- Passlib and bcrypt
- Docker and Docker Compose

## Architecture
- Routers: Authentication API endpoints.
- Schemas: Request and response validation.
- Models: Database table definitions.
- Services: Authentication business logic.
- Core: Application settings and security utilities.
- Database: SQLAlchemy connection management.
- Alembic: Database migrations.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/register | Register a user |
| POST | /api/auth/login | Login and issue JWT |
| GET | /api/auth/me | Retrieve current user |
| POST | /api/auth/verify-token | Verify JWT |
| POST | /api/auth/change-password | Change password |
| GET | /health | Service health |

## Database
Database: shopease_auth_db

Table: users

- id
- full_name
- email
- password_hash
- role
- is_active
- created_at
- updated_at

## Environment Configuration
Sensitive configuration is stored in .env.
Never commit .env to GitHub.

## Docker Deployment

Build and start:

```powershell
docker compose up --build -d
```

Stop containers:

```powershell
docker compose down
```

MySQL uses a named Docker volume for persistent storage.

## Security Features
- bcrypt password hashing
- JWT authentication
- Configurable token expiry
- Unique email constraint
- Protected endpoints
- Inactive account restrictions
- Environment-based secrets
- Password confirmation and complexity validation

## Scope
This authentication microservice independently owns its database. Integration with other ShopEase microservices is planned for a later phase.
