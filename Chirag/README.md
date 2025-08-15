# Site Analysis Backend

A comprehensive backend service integrating **7 Bhuvan APIs** for geospatial analysis and location-based services. This system provides real-time access to India's official geospatial data through standardized API clients with comprehensive benchmarking and validation capabilities.

## 🚀 Features

- **Complete Bhuvan API Integration**: 7 fully operational API clients
- **Real-time Geospatial Data**: No simulated data - all live endpoints
- **Performance Benchmarking**: Comprehensive testing suite with metrics
- **Geographic Validation**: State boundary checking and coordinate validation
- **Robust Error Handling**: Content-type agnostic JSON parsing
- **Production Ready**: 100% success rate across all APIs

## 📊 API Performance (Latest Benchmark)

| API Service | Avg Response Time | Success Rate | Coverage |
|-------------|------------------|--------------|----------|
| Geoid API | 0.254s | 100% | Administrative boundaries |
| Postal & Hospital | 0.507s | 100% | Healthcare & postal services |
| Village Geocoding | 0.509s | 100% | Village-level geocoding |
| Village Reverse Geocoding | 0.513s | 100% | Coordinate to village mapping |
| LULC AOI Statistics | 0.582s | 100% | Land use/land cover analysis |
| Thematic Statistics | 0.773s | 100% | District-wise LULC data |
| Routing API | 2.602s | 100% | Turn-by-turn navigation |

**Overall Performance**: 32 API calls, 100% success rate, 0.546s average response time

## 🏗️ Project Structure

```
├── app.py                           # Main Flask application
├── benchmark_all_apis.py           # Comprehensive API benchmark suite
├── benchmark_tests.py              # Legacy benchmark tests
├── src/
│   ├── api/                        # Bhuvan API clients
│   │   ├── postal_hospital.py      # Postal & hospital services
│   │   ├── village_geocoding.py    # Village geocoding
│   │   ├── village_reverse_geocoding.py # Reverse geocoding
│   │   ├── lulc_aoi_wise.py        # LULC AOI-wise statistics
│   │   ├── routing.py              # Navigation routing
│   │   ├── thematic_statistics.py  # District LULC statistics
│   │   └── geoid.py                # Administrative boundaries
│   ├── config/
│   │   └── token_manager.py        # Centralized token management
│   ├── data/
│   │   ├── district_codes.json     # 500+ district code mappings
│   │   └── state_codes.json        # Complete state code mappings
│   └── utils/
│       ├── benchmark.py            # Benchmarking utilities
│       ├── data_analyzer.py        # Response analysis tools
│       └── validators.py           # Geographic validation
├── tests/                          # Unit tests
├── data/                           # API responses and benchmarks
└── .env.example                    # Environment configuration
```

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/chiraghontec/SiteAnalysis-Backend.git
   cd SiteAnalysis-Backend
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API tokens**
   ```bash
   cp .env.example .env
   # Edit .env with your Bhuvan API tokens
   ```

4. **Validate setup**
   ```bash
   python validate_tokens.py  # Verify all API tokens
   python benchmark_all_apis.py  # Run comprehensive benchmark
   ```

## 🔧 API Services

### 1. Postal & Hospital API
- **Purpose**: Find postal codes and nearby hospitals
- **Input**: Latitude, longitude
- **Output**: Postal codes, hospital locations, administrative info

### 2. Village Geocoding API
- **Purpose**: Convert village names to coordinates
- **Input**: Village name, state
- **Output**: Precise coordinates, administrative boundaries

### 3. Village Reverse Geocoding API
- **Purpose**: Get village information from coordinates
- **Input**: Latitude, longitude
- **Output**: Village name, administrative hierarchy

### 4. LULC AOI-wise Statistics API
- **Purpose**: Land use/land cover analysis for area of interest
- **Input**: Polygon coordinates, analysis parameters
- **Output**: Detailed LULC statistics, area calculations

### 5. Routing API
- **Purpose**: Navigation and route planning
- **Input**: Origin, destination coordinates
- **Output**: Turn-by-turn directions, distance, duration

### 6. Thematic Statistics API
- **Purpose**: District-wise LULC statistical data
- **Input**: District code, year
- **Output**: Comprehensive land use statistics

### 7. Geoid API
- **Purpose**: Administrative boundary identification
- **Input**: Latitude, longitude
- **Output**: State, district, block, village codes

## 🌐 Running the Application

Start the Flask application:
```bash
python app.py
```

The application will be available at http://localhost:5000

### Health Check
```bash
curl http://localhost:5000/health
```

## 🧪 Comprehensive Benchmark Testing

Run the complete benchmark suite:
```bash
python benchmark_all_apis.py
```

This comprehensive test:
- Tests all 7 APIs with multiple Indian cities
- Measures response times and success rates
- Validates data quality and structure
- Generates detailed performance reports
- Saves results with timestamps for tracking

### Legacy Benchmark Tests
```bash
python benchmark_tests.py benchmark
```

## 📋 API Endpoints

### Flask Application Endpoints

#### Thematic Statistics
- `POST /api/thematic-stats`
  - Request: `{"district": "Mumbai", "year": 2022}`
  - Response: District-wise LULC statistics

#### Routing
- `POST /api/routing`
  - Request: `{"origin": {"lat": 19.0760, "lng": 72.8777}, "destination": {"lat": 18.5204, "lng": 73.8567}}`
  - Response: Navigation directions with turn-by-turn guidance

#### Geoid
- `POST /api/geoid`
  - Request: `{"coordinates": {"lat": 19.0760, "lng": 72.8777}}`
  - Response: Administrative boundary codes

#### Village Geocoding
- `POST /api/village-geocoding`
  - Request: `{"village": "Andheri", "state": "Maharashtra"}`
  - Response: Village coordinates and boundaries

#### LULC Analysis
- `POST /api/lulc-aoi`
  - Request: `{"polygon": [...], "year": 2022}`
  - Response: Land use/land cover statistics

#### Health Check
- `GET /health`
  - Response: System status and API availability

## 📊 Data Storage & Reports

### Automatic Data Storage
- API responses stored in `data/` with timestamps
- Benchmark results in `benchmark_results_*.json`
- Geographic validation logs
- Performance metrics tracking

### Generated Reports
- **API Benchmark Report**: `data/reports/benchmark_report.html`
- **Performance Comparison**: `data/reports/api_comparison.html`
- **Geographic Coverage**: City-wise API testing results
- **Response Time Analysis**: Detailed timing statistics

## 🔍 Key Features

### Geographic Validation
- State boundary checking for routing requests
- Coordinate validation for all APIs
- Administrative hierarchy verification

### Error Handling
- Robust JSON parsing regardless of content-type headers
- Graceful degradation for API failures
- Comprehensive error logging and reporting

### Performance Monitoring
- Real-time response time tracking
- Success rate monitoring across all APIs
- Geographic coverage validation
- Data quality assessment

### Production Readiness
- 100% success rate across all APIs
- Centralized token management
- Environment-based configuration
- Comprehensive testing coverage

## 🚀 Production Deployment

The system is production-ready with:
- All APIs validated and operational
- Performance benchmarks established
- Error handling implemented
- Geographic validation in place
- Comprehensive monitoring capabilities

Use the benchmark results to set up monitoring thresholds and performance alerts in your production environment.
