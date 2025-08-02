# Backend - Site Analysis Platform

Django REST API backend for the Site Analysis Platform.

## Overview

This is a Django-based REST API that provides environmental site analysis capabilities, including vegetation analysis, terrain data, climate conditions, and geospatial data processing.

## Tech Stack

- **Django 5.2.3** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database with PostGIS extension
- **GeoDjango** - Geospatial data handling
- **Python 3.9+** - Programming language

## Features

- 🗺️ **Geospatial Analysis** - PostGIS-powered location analysis
- 🌱 **Vegetation Data** - Automated vegetation and terrain analysis
- 🌤️ **Climate API** - Weather and climate data integration
- 📊 **Data Processing** - Environmental data analysis
- 🔐 **Secure API** - Authentication and authorization
- 📁 **File Processing** - KML file upload and processing

## Getting Started

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 12+ with PostGIS extension
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@localhost:5432/site_analysis
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

4. **Set up PostgreSQL with PostGIS:**
   ```sql
   CREATE DATABASE site_analysis;
   CREATE USER site_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE site_analysis TO site_user;
   
   -- Connect to the database and enable PostGIS
   \c site_analysis
   CREATE EXTENSION postgis;
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Site Analysis
- `GET /api/site-analysis/` - List site analysis data
- `POST /api/site-analysis/` - Create new site analysis
- `GET /api/site-analysis/{id}/` - Retrieve specific analysis

### Climate Data
- `POST /api/climate-data/` - Get climate data for coordinates
- `GET /api/climate-data/{id}/` - Retrieve stored climate data

### Vegetation Analysis
- `POST /api/vegetation-analysis/` - Analyze vegetation for site
- `GET /api/vegetation-analysis/{id}/` - Get vegetation analysis results

### File Upload
- `POST /api/upload-kml/` - Upload and process KML files

### Health Check
- `GET /api/health/` - API health status

## Project Structure

```
backend/
├── site_analysis_backend/   # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI config
│   └── asgi.py            # ASGI config
├── environmental_analysis/ # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # App URL patterns
│   └── utils.py           # Utility functions
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## Database Models

### SiteAnalysis
- Location coordinates
- Analysis timestamp
- Vegetation data
- Terrain information
- Climate conditions

### ClimateData
- Temperature records
- Humidity data
- Precipitation
- Wind conditions

### VegetationAnalysis
- Vegetation types
- Coverage percentages
- Terrain slope data
- Water body information

## API Authentication

The API supports multiple authentication methods:

- **Session Authentication** - For web interface
- **Token Authentication** - For API clients
- **JWT Authentication** - For mobile apps (optional)

## Testing

Run the test suite:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test environmental_analysis
```

## Development

### Code Quality
```bash
# Format code
black .
isort .

# Check code quality
flake8 .
```

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush
```

### Django Admin
Access the admin interface at `http://localhost:8000/admin/` using your superuser credentials.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost` |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs for CORS | `http://localhost:3000` |

## Deployment

### Production Settings
- Set `DEBUG=False`
- Configure proper `SECRET_KEY`
- Set up production database
- Configure static file serving
- Set up HTTPS

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Performance

- **Database indexing** - Proper indexes on geographic fields
- **Query optimization** - Use select_related and prefetch_related
- **Caching** - Redis for caching (production)
- **Pagination** - Paginated API responses

## Security

- **CORS configuration** - Proper cross-origin settings
- **Input validation** - Serializer validation
- **SQL injection protection** - Django ORM
- **Authentication** - Multiple auth methods
- **Rate limiting** - API throttling

## Monitoring

- **Logging** - Comprehensive application logging
- **Health checks** - API health endpoint
- **Error tracking** - Sentry integration (optional)

## Contributing

1. Follow PEP 8 style guidelines
2. Write comprehensive tests
3. Document API changes
4. Use meaningful commit messages
5. Create detailed pull requests

## Troubleshooting

### Common Issues

**PostgreSQL connection errors:**
- Check database credentials
- Ensure PostgreSQL service is running
- Verify PostGIS extension is installed

**Migration errors:**
```bash
python manage.py migrate --fake-initial
```

**Permission errors:**
```bash
chmod +x manage.py
```
