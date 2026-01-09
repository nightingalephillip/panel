# OSINT Dashboard

A modular OSINT investigation platform with case management.

## Status
🚧 Under Development - Phase 1 Complete

## Tech Stack
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, Zustand, React Query
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic
- **Database:** PostgreSQL 15
- **Infrastructure:** Docker, Docker Compose

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nightingalephillip/panel.git
cd panel
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start the development environment:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development

The dev environment has hot-reload enabled:
- Frontend changes in `frontend/src/` auto-refresh
- Backend changes in `backend/app/` auto-reload

### Database Migrations

```bash
# Enter the backend container
docker-compose exec backend bash

# Create a new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head
```

## Project Structure

```
panel/
├── frontend/          # React + TypeScript + Vite
│   └── src/
│       ├── modules/   # Feature modules (auth, cases, etc.)
│       ├── shared/    # Shared components, hooks, utils
│       └── layouts/   # Page layouts
├── backend/           # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── modules/   # Feature modules
│   │   └── core/      # Shared backend code
│   └── alembic/       # Database migrations
└── db/                # Database init scripts
```
