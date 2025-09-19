# Configuration Management System

This document explains the new configuration system that replaces hardcoded URLs and ports throughout the application.

## Backend Configuration

### Files Created:
- `backend/config.py` - Main configuration class with environment-specific settings
- `backend/.env` - Development environment variables
- `backend/.env.production` - Production environment variables  
- `backend/requirements.txt` - Updated Python dependencies

### Key Features:
- **Environment-based configuration**: Different settings for development, production, and testing
- **Centralized CSV file paths**: All data file paths managed in one place
- **Configurable server settings**: Host, port, debug mode, CORS origins
- **Environment variable support**: Uses python-dotenv for .env file loading

### Usage:
```python
from config import get_config
config = get_config()  # Gets config based on FLASK_ENV
app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
```

### Configuration Classes:
- `Config` - Base configuration class
- `DevelopmentConfig` - Development settings (127.0.0.1:5002, debug=True)
- `ProductionConfig` - Production settings (0.0.0.0:5000, debug=False)
- `TestingConfig` - Testing settings (127.0.0.1:5003, debug=True)

## Frontend Configuration

### Files Created:
- `frontend/src/config/config.js` - Main configuration module
- `frontend/.env.development` - Development environment variables
- `frontend/.env.production` - Production environment variables
- `frontend/.env.test` - Testing environment variables

### Key Features:
- **Environment-based API URLs**: Automatically switches between dev/prod endpoints
- **Centralized endpoint definitions**: All API endpoints defined in one place
- **Helper functions**: `getApiUrl()`, `getFullApiUrl()`, `isDebugEnabled()`
- **UI configuration**: File upload limits, timeouts, pagination settings

### Usage:
```javascript
import { getApiUrl, isDebugEnabled } from '../config/config';

// Get API URL for a specific endpoint
const response = await fetch(getApiUrl('suppliers'));

// Check if debug mode is enabled
if (isDebugEnabled()) {
  console.log('Debug info...');
}
```

### API Endpoints Configured:
- `suppliers` → `/api/suppliers`
- `fuelTypes` → `/api/fuel_types`
- `vehicleAndSize` → `/api/vehicle_and_size`
- `computeGhgEmissions` → `/api/compute_ghg_emissions`
- All lookup endpoints (region, scope, units, etc.)

## Environment Variables

### Backend (.env):
```bash
FLASK_ENV=development
FLASK_HOST=127.0.0.1
FLASK_PORT=5002
FLASK_DEBUG=True
CORS_ORIGINS=*
```

### Frontend (.env.development):
```bash
REACT_APP_API_BASE_URL=http://127.0.0.1:5002
REACT_APP_ENV=development
REACT_APP_DEBUG=true
```

## Benefits

1. **No More Hardcoded URLs**: All URLs and ports are now configurable
2. **Environment Flexibility**: Easy switching between development and production
3. **Centralized Management**: All configuration in dedicated files
4. **Better Security**: Sensitive settings can be kept in environment variables
5. **Easier Deployment**: Simple environment variable changes for different environments
6. **Maintainability**: Single place to update API endpoints or server settings

## Migration Completed

### Backend Changes:
- ✅ All CSV file paths now use `config.get_csv_path()`
- ✅ Server startup uses `config.HOST`, `config.PORT`, `config.DEBUG`
- ✅ CORS origins configurable via `config.CORS_ORIGINS`

### Frontend Changes:
- ✅ All hardcoded `http://127.0.0.1:5002` URLs replaced with `getApiUrl()`
- ✅ API endpoints centralized in configuration
- ✅ Environment-specific settings implemented

## Future Enhancements

1. **Database Configuration**: Add database connection strings to config
2. **Logging Configuration**: Configure logging levels per environment
3. **Cache Settings**: Add caching configuration options
4. **Security Settings**: JWT secrets, API keys, etc.
5. **Performance Tuning**: Timeout settings, connection pools, etc.

## Development Workflow

### Starting the Application:

**Backend**:
```bash
cd backend
# Uses .env file automatically
python app.py
```

**Frontend**:
```bash
cd frontend
# Uses .env.development automatically in development
npm start
```

### Switching Environments:

**Backend**:
```bash
export FLASK_ENV=production  # or set in .env file
python app.py
```

**Frontend**:
```bash
npm run build  # Uses .env.production
```

This configuration system provides a robust foundation for managing application settings across different environments while maintaining clean, maintainable code.
