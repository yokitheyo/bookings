# Hotel Booking System

A modern, scalable hotel booking system built with FastAPI, featuring a comprehensive set of features for managing hotels, rooms, bookings, and user accounts.

## Features

- **User Management**
  - User registration and authentication
  - Role-based access control
  - User profile management

- **Hotel Management**
  - Hotel listing and details
  - Room management
  - Availability tracking

- **Booking System**
  - Room reservation
  - Booking management
  - Availability checking

- **Admin Panel**
  - Comprehensive admin interface
  - User management
  - Hotel and room management
  - Booking oversight

- **Monitoring & Metrics**
  - Prometheus integration
  - Grafana dashboards
  - Performance monitoring

- **Additional Features**
  - Image upload and management
  - API versioning
  - Redis caching
  - CORS support
  - Static file serving

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Monitoring**: Prometheus + Grafana
- **Task Queue**: Celery
- **Admin Panel**: SQLAdmin
- **Testing**: Pytest
- **Containerization**: Docker

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL
- Redis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yokitheyo/bookings.git
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env-example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

### Production Mode (with Docker)

```bash
docker-compose up -d
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Monitoring

- Prometheus metrics: `http://localhost:8000/metrics`
- Grafana dashboard: `http://localhost:3000`

## Testing

Run tests with:
```bash
pytest
```

## Project Structure

```
├── app/
│   ├── admin/          # Admin panel components
│   ├── bookings/       # Booking management
│   ├── core/           # Core functionality
│   ├── hotels/         # Hotel management
│   ├── images/         # Image handling
│   ├── middleware/     # Custom middleware
│   ├── prometheus/     # Monitoring
│   ├── static/         # Static files
│   ├── templates/      # HTML templates
│   ├── users/          # User management
│   ├── config.py       # Configuration
│   ├── database.py     # Database setup
│   └── main.py         # Application entry point
├── docker/             # Docker configuration
├── migrations/         # Database migrations
├── tests/             # Test suite
├── .env-example       # Environment variables template
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile         # Docker build configuration
└── requirements.txt   # Python dependencies
```
