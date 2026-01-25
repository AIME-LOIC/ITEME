# ITEME Quick Reference

## 🚀 Start the Application
```bash
cd /home/aime/ITEME
./start.sh
```

Or manually:
```bash
source installed/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📍 Main Endpoints

### Arrival Tracking
- **Form:** http://localhost:8000/
- **Submit:** POST `/arrival`
- **Admin:** http://localhost:8000/arrival/admin

### Payment Management  
- **Form:** http://localhost:8000/payment/
- **Submit:** POST `/payment/api/submit`
- **Admin:** http://localhost:8000/payment/admin (password: `iteme2026`)

### API Documentation
- **Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📦 Database Tables

### Supabase Setup Required:

**Table 1: arrival**
```sql
CREATE TABLE arrival (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  student_name TEXT NOT NULL,
  class_name TEXT NOT NULL,
  status TEXT DEFAULT 'waiting',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Table 2: transactions**
```sql
CREATE TABLE transactions (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  receiver TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Admin Access

**Payment Admin:**
- Default password: `iteme2026`
- Change via `.env`: `ADMIN_PASSWORD=your_password`

---

## 🧪 Quick Test Commands

### Test Payment Submission
```bash
curl -X POST http://localhost:8000/payment/api/submit \
  -F "name=Test User" \
  -F "date=2026-01-22" \
  -F "amount=100.00" \
  -F "receiver=ITEME"
```

### Test Arrival Submission
```bash
curl -X POST http://localhost:8000/arrival \
  -d "student_name=John Doe&class_name=Grade 10"
```

### Fetch Payment Data (Admin)
```bash
PASS=$(echo -n "iteme2026" | base64)
curl "http://localhost:8000/payment/api/admin/data?pwd=$PASS"
```

### Download Payments as CSV
```bash
PASS=$(echo -n "iteme2026" | base64)
curl "http://localhost:8000/payment/api/admin/download?pwd=$PASS&format=csv" -o data.csv
```

---

## 📂 File Structure
```
/home/aime/ITEME/
├── main.py                    # Main FastAPI app
├── payment.py                 # Payment module (integrated)
├── config.py                  # Supabase config
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── start.sh                   # Startup script
├── SETUP_COMPLETE.md          # Full documentation
├── PAYMENT_API_README.md      # Payment API docs
├── templates/                 # HTML templates
└── installed/                 # Virtual environment
```

---

## ✅ What Was Done

1. ✅ Converted `payment.py` from Flask to FastAPI
2. ✅ Migrated database from PostgreSQL to Supabase
3. ✅ Added `GET /` endpoint to payment module
4. ✅ Integrated payment app into main app (`/payment/*`)
5. ✅ Created comprehensive documentation
6. ✅ Created automated startup script

---

## 🎯 Key Routes Summary

| Path | Method | Purpose |
|------|--------|---------|
| `/` | GET | Arrival form |
| `/arrival` | POST | Submit arrival |
| `/arrival/admin` | GET | Arrival dashboard |
| `/activate/{id}` | POST | Activate student |
| `/payment/` | GET | Payment form |
| `/payment/api/submit` | POST | Submit payment |
| `/payment/admin` | GET | Payment dashboard |
| `/payment/api/admin/data` | GET | Get payment JSON |
| `/payment/api/admin/download` | GET | Download payments |
| `/docs` | GET | API documentation |

---

## 🔧 Troubleshooting

**Port 8000 already in use:**
```bash
uvicorn main:app --port 8001
```

**Virtual environment issues:**
```bash
rm -rf installed
python3 -m venv installed
source installed/bin/activate
pip install -r requirements.txt
```

**Supabase connection error:**
- Check `.env` file has correct credentials
- Verify tables exist in Supabase dashboard

**Dependency errors:**
```bash
pip install --upgrade -r requirements.txt
```

---

Made with ❤️ for ITEME
