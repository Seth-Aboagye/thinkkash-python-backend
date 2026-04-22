# Thinkkash Python Backend (FastAPI)

A Python backend starter for Thinkkash using:
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT auth
- Role-based access
- Wallets
- Videos
- Projects
- Suppliers
- Investors
- Adverts
- Settlements
- Admin approval flows

## Run locally

1. Create virtual environment
```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
# or
source .venv/bin/activate  # Mac/Linux
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create PostgreSQL database
```sql
CREATE DATABASE thinkkash_py;
```

4. Copy `.env.example` to `.env` and edit values.

5. Start server
```bash
uvicorn app.main:app --reload
```

6. Open docs
- http://127.0.0.1:8000/docs

## Notes
This is a strong backend foundation. For production, add:
- Alembic migrations
- real OTP provider
- Cloudinary/S3 uploads
- Stripe integration
- refresh tokens
- audit logs
- async background jobs
