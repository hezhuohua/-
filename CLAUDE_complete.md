- `demo.html` - Demonstration version with simulated data
- Various test and diagnostic HTML files for specific features

Key JavaScript components:
- Real-time data visualization with Chart.js
- WebSocket connection management
- User authentication and session handling
- Payment processing workflows
- Responsive UI components for mobile and desktop
- Interactive trading dashboards

## System Architecture Overview

The system follows a modular architecture with clear separation of concerns:

### Data Layer
- **Market Data Providers**: Real-time data from Binance, OKX, Bybit
- **Database**: SQLite/PostgreSQL for user data, orders, predictions
- **Caching**: Redis for session management and temporary data

### Business Logic Layer
- **Prediction Engine**: Combines technical analysis and AI models
- **Risk Management**: Position sizing, stop-loss mechanisms
- **Payment Processing**: Order management, QR code payments
- **User Management**: Authentication, membership levels, quotas

### API Layer
- **RESTful API**: FastAPI endpoints for all system functionality
- **WebSocket API**: Real-time data streaming
- **Rate Limiting**: Middleware to prevent abuse
- **Security**: JWT authentication, input validation

### Presentation Layer
- **Web Interface**: Responsive HTML/CSS/JavaScript frontend
- **Mobile Support**: Optimized for mobile devices
- **Real-time Updates**: WebSocket-driven UI updates

## Development Workflow

### Code Organization
- Backend code in `backend/` directory
- Frontend code in root directory (HTML/CSS/JS files)
- Tests in `tests/` directory
- Static assets in `static/` directory
- Uploads in `uploads/` directory

### Version Control
- Git for version control
- Feature branches for new development
- Pull requests for code review
- Semantic versioning for releases

### Testing Strategy
- Unit tests for individual components
- Integration tests for API endpoints
- End-to-end tests for critical user flows
- Performance tests for prediction service
- Security tests for authentication and authorization

## Deployment Architecture

### Development Environment
- Local development with SQLite database
- Built-in FastAPI development server
- Hot reloading for frontend development

### Production Environment
- PostgreSQL database for production
- Gunicorn for WSGI server
- Nginx as reverse proxy
- Redis for caching and session management
- SSL/TLS for secure connections

### Containerization
- Docker support for containerized deployment
- Docker Compose for multi-container setups
- Environment-specific configuration files

## Monitoring and Maintenance

### Logging
- Structured logging with Python logging module
- Log levels for different environments
- Log rotation for production systems

### Performance Monitoring
- Response time monitoring
- Database query performance
- Prediction service latency
- WebSocket connection health

### Error Handling
- Centralized error handling
- Error reporting and alerting
- Graceful degradation for non-critical failures
- User-friendly error messages

## Future Enhancements

### AI/ML Improvements
- Advanced machine learning models
- Deep learning integration
- Ensemble methods for improved accuracy
- Real-time model retraining

### Trading Features
- Advanced order types
- Portfolio management
- Backtesting capabilities
- Strategy optimization

### User Experience
- Mobile app development
- Advanced charting features
- Social trading features
- Community features

This CLAUDE.md file provides comprehensive guidance for working with this cryptocurrency perpetual contract prediction system. It covers the architecture, development workflow, deployment considerations, and future enhancement opportunities.