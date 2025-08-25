# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cryptocurrency perpetual contract prediction system built with:
- **Backend**: FastAPI, SQLAlchemy, Redis
- **Frontend**: HTML/CSS/JavaScript with Chart.js
- **AI/ML**: Scikit-learn, Pandas, Numpy
- **Database**: SQLite (default) or PostgreSQL
- **Authentication**: JWT tokens with password hashing

## Key Features

1. **AI-driven price prediction** for cryptocurrency perpetual contracts
2. **User authentication and management** with membership levels
3. **Payment system** with order management and QR code payments
4. **Real-time market data** via WebSocket connections
5. **Rate limiting** to prevent API abuse
6. **Security features** including input validation and JWT authentication

## Project Structure

```
├── backend/                  # Backend service
│   ├── main.py              # Main FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── auth.py              # Authentication and JWT handling
│   ├── database.py          # Database configuration
│   ├── exchange_manager.py  # Market data management
│   ├── prediction_service.py # AI prediction service
│   ├── payment_service.py   # Payment processing
│   ├── rate_limiter.py      # API rate limiting
│   └── exchange_api.py      # Exchange API integrations
├── frontend/                # Frontend application (Vue.js)
├── static/                  # Static files
├── uploads/                 # Uploaded files (QR codes, payment proofs)
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── run_server.py           # Application startup script

NOTE: The frontend is primarily HTML/CSS/JavaScript files in the root directory, not in a dedicated frontend/ directory.
```

## Common Development Tasks

### Starting the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python run_server.py
```

The system will be available at:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:8080
- API Documentation: http://localhost:8000/docs

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic.py

# Run with coverage
pytest --cov=.
```

### Database Operations

The system uses SQLAlchemy ORM. Database models are defined in `backend/models.py`.

### API Development

Endpoints are defined in `backend/main.py`. Common patterns:
- Use Pydantic schemas for input validation
- Use JWT authentication with `get_current_user` dependency
- Apply rate limiting with `check_rate_limit`
- Follow RESTful conventions

### AI Prediction Service

The prediction service in `backend/prediction_service.py` combines:
1. Technical analysis predictions
2. AI model predictions (scikit-learn)
3. DEEPSEEK API integration (optional)

### Payment System

Payment processing is handled in `backend/payment_service.py`:
- Order creation and management
- QR code payment handling
- Payment proof upload and review
- Membership activation

## Security Considerations

1. **JWT Authentication**: All protected endpoints require valid JWT tokens
2. **Rate Limiting**: Implemented via middleware to prevent abuse
3. **Input Validation**: All API inputs are validated with Pydantic schemas
4. **Password Security**: Passwords are hashed with bcrypt
5. **Environment Variables**: Sensitive configuration stored in .env file

## Key Dependencies

- **FastAPI**: High-performance web framework
- **SQLAlchemy**: Database ORM
- **Redis**: Caching and session management
- **JWT**: Token-based authentication
- **Scikit-learn**: Machine learning algorithms
- **Pandas/Numpy**: Data processing
- **Chart.js**: Frontend charting library

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./crypto_prediction.db
REDIS_URL=redis://localhost:6379
DEEPSEEK_API_KEY=your-api-key-here  # Optional
```

## Testing Guidelines

1. **Unit Tests**: Located in `tests/` directory
2. **Security Tests**: Input validation, authentication, rate limiting
3. **Integration Tests**: API endpoint testing with TestClient
4. **Mock Services**: Use unittest.mock for external API calls

## Deployment Considerations

1. **Production Database**: Use PostgreSQL instead of SQLite
2. **Environment Configuration**: Set DEBUG=False and proper SECRET_KEY
3. **Reverse Proxy**: Use Nginx for production deployment
4. **Process Management**: Use Gunicorn or similar WSGI server
5. **SSL/TLS**: Enable HTTPS in production

## Common API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/prediction/predict` - Price prediction
- `GET /api/market/data/{symbol}` - Market data
- `POST /api/orders/create` - Create order
- `GET /health` - Health check

## Development Best Practices

1. **Code Style**: Follow PEP 8 standards
2. **Type Hints**: Use type annotations for all functions
3. **Error Handling**: Implement proper exception handling
4. **Logging**: Use Python logging module for debugging
5. **Documentation**: Keep API docs updated with changes

## Frontend Architecture

The frontend is a single-page application built with vanilla JavaScript and Chart.js:
- **Real-time charts** using WebSocket connections
- **Responsive design** for mobile and desktop
- **Modern UI** with tech-themed styling
- **Multiple pages** for dashboard, predictions, market data, membership, etc.

Key frontend components:
- Dashboard with real-time price displays
- AI prediction panels with multi-timeframe analysis
- Market data visualization
- User authentication and account management
- Payment and membership management
- Risk management tools

## WebSocket Integration

The system uses WebSocket connections for real-time data:
- Market data streaming from multiple exchanges
- Real-time price updates
- Prediction result notifications
- Connection management with automatic reconnection

## Exchange Integration

The system supports multiple cryptocurrency exchanges:
- **Binance**: Primary exchange with WebSocket streaming
- **OKX**: Secondary exchange support
- **Bybit**: Additional exchange support
- **Simulated data**: Fallback for development/testing

Exchange data is managed through the `ExchangeDataManager` which provides:
- Real-time market data aggregation
- Cross-exchange price comparison
- Funding rate and open interest data
- Data normalization across exchanges

## AI/ML Components

The prediction system includes multiple AI/ML components:
- **Technical analysis**: Traditional trading indicators
- **Machine learning models**: Scikit-learn based predictions
- **Deep learning**: Optional DEEPSEEK API integration
- **Ensemble methods**: Combination of multiple prediction models

Prediction service features:
- Multi-timeframe predictions (1m, 5m, 15m, 1h)
- Confidence scoring and probability estimates
- Directional predictions with target prices
- Model combination for improved accuracy

## Payment and Membership System

The system includes a complete payment and membership management system:
- **Multiple membership levels**: Trial, Basic, Pro, Premium
- **QR code payments**: Alipay and WeChat payment support
- **Order management**: Payment tracking and verification
- **Usage quotas**: Daily prediction limits per membership level
- **Subscription management**: Auto-renewal and expiration handling

## Risk Management

Advanced risk management features:
- **Position sizing**: Based on account balance and risk tolerance
- **Stop-loss mechanisms**: Automatic position closing
- **Risk metrics**: VaR, maximum drawdown, Sharpe ratio
- **Real-time monitoring**: Market condition alerts

## Backend Service Architecture

The backend is structured as a FastAPI application with the following key components:

### Core Services
1. **ExchangeDataManager** (`backend/exchange_manager.py`) - Manages real-time market data from multiple exchanges
2. **PredictionService** (`backend/prediction_service.py`) - Combines technical analysis, AI models, and DEEPSEEK API for predictions
3. **PaymentService** (`backend/payment_service.py`) - Handles orders, payments, and membership management
4. **AuthService** (`backend/auth.py`) - JWT-based authentication and authorization

### Database Layer
- **Models** (`backend/models.py`) - SQLAlchemy ORM models for all database entities
- **Schemas** (`backend/schemas.py`) - Pydantic validation schemas for API input/output
- **Database** (`backend/database.py`) - Database engine and session management

### API Layer
- **Main Application** (`backend/main.py`) - FastAPI application with all endpoints
- **Rate Limiter** (`backend/rate_limiter.py`) - API rate limiting middleware

## Frontend Components

The frontend consists of several HTML files that serve different purposes:
- `