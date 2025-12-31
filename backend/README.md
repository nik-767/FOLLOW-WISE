# FollowWise Backend

Backend API for FollowWise, an AI-powered sales follow-up automation tool for freelancers and small agencies.

## Features

- User authentication with JWT
- Lead management (CRUD operations)
- AI-powered follow-up email generation
- Email sending (with Gmail integration stubs)
- RESTful API design
- SQLite database (can be easily switched to PostgreSQL)

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: JWT
- **AI Integration**: Extensible AI provider interface (dummy implementation included)
- **Email**: Gmail API (stubbed for MVP)

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone [your-repository-url]
   cd followwise/backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `backend` directory with the following content:
   ```env
   # App settings
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Database (SQLite by default)
   DATABASE_URL=sqlite:///./followwise.db
   
   # For production, you might use PostgreSQL:
   # DATABASE_URL=postgresql://user:password@localhost:5432/followwise
   ```

5. **Initialize the database**
   ```bash
   python -m app.db.init_db
   ```

6. **Run the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user info

### Leads
- `GET /api/leads` - List all leads (with optional filtering)
- `POST /api/leads` - Create a new lead
- `GET /api/leads/{lead_id}` - Get a specific lead
- `PATCH /api/leads/{lead_id}` - Update a lead
- `DELETE /api/leads/{lead_id}` - Delete a lead

### Follow-ups
- `POST /api/leads/{lead_id}/generate-followups` - Generate AI follow-up suggestions
- `GET /api/leads/{lead_id}/followups` - Get follow-up suggestions for a lead
- `POST /api/leads/{lead_id}/send-email` - Send an email to a lead
- `GET /api/leads/{lead_id}/sent-emails` - Get sent emails for a lead

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/        # API route handlers
│   ├── core/                 # Core functionality (security, config)
│   ├── db/                   # Database configuration and models
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic models for request/response
│   ├── services/             # Business logic and external services
│   └── utils/                # Utility functions
├── tests/                    # Test files
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Testing

To run tests:

```bash
pytest
```

## Deployment

### Local Development
For local development, you can use the built-in Uvicorn server:
```bash
uvicorn app.main:app --reload
```

### Production
For production, you might want to use a production ASGI server like Gunicorn with Uvicorn workers:

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

### Docker
A `Dockerfile` and `docker-compose.yml` can be added for containerized deployment.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Secret key for JWT token signing | (required) |
| `ALGORITHM` | Algorithm for JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiry time | `30` |
| `DATABASE_URL` | Database connection URL | `sqlite:///./followwise.db` |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
