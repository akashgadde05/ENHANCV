# Deployment Guide

## Local Development

### Quick Start
```bash
git clone https://github.com/akashgadde05/ENHANCV.git
cd ENHANCV
python start.py
```

### Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run the application
python run.py
```

## Production Deployment

### Using Gunicorn (Recommended)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables
```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DEBUG=False
SECRET_KEY=your_production_secret_key
```

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Set environment variables
heroku config:set GROQ_API_KEY=your_api_key
heroku config:set GROQ_MODEL=llama-3.3-70b-versatile
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Vercel Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## Configuration

### Required Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_MODEL`: Model to use (default: llama-3.3-70b-versatile)

### Optional Environment Variables
- `DEBUG`: Enable debug mode (default: True)
- `SECRET_KEY`: Flask secret key (auto-generated if not set)
- `PORT`: Port to run on (default: 5000)

## Monitoring & Maintenance

### Health Checks
```bash
# System health check
python check_system.py

# Complete system test
python test_complete_system.py

# API test
python test_groq.py
```

### Logs
- Application logs are printed to stdout
- Use log aggregation services in production
- Monitor API usage and rate limits

### Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Test after updates
python test_complete_system.py
```
