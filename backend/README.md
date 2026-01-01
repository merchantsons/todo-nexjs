# Evolution of Todo - Backend API

FastAPI backend for Evolution of Todo Phase II.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Initialize database:
```bash
python init_db.py
```

4. Run development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

