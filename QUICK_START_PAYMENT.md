# Quick Start Guide - Payment API

## What Was Done

✅ **payment.py has been completely updated:**
- Converted from Flask to FastAPI
- Switched database from PostgreSQL to Supabase
- Added "/" endpoint for the payment form
- All data is now saved to Supabase `transactions` table
- Admin dashboard and download functionality preserved

---

## 🚀 Getting Started

### Step 1: Verify Supabase Credentials
Ensure your `.env` file has:
```
SUPABASE_URL=https://ruxiswyfpkbatnzcbvog.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 2: Create the Supabase Table (if needed)
Go to your Supabase SQL editor and run:
```sql
CREATE TABLE transactions (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  receiver TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Enable RLS
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable access for service role" ON transactions
  FOR ALL USING (true) WITH CHECK (true);
```

### Step 3: Start the Payment API
```bash
cd /home/aime/ITEME
python3 -m uvicorn payment:app --port 5000 --host 0.0.0.0
```

### Step 4: Access the Application
- **Payment Form:** http://localhost:5000/
- **Admin Dashboard:** http://localhost:5000/admin
- **Swagger API Docs:** http://localhost:5000/docs

---

## 📍 Key Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Payment form |
| POST | `/api/submit` | Submit payment |
| GET | `/admin` | Admin dashboard (password: iteme2026) |
| GET | `/api/admin/data` | Fetch transactions (JSON) |
| GET | `/api/admin/download` | Download transactions (CSV/Excel/PDF/DOCX) |

---

## 🔑 Admin Password

Default: **`iteme2026`**

Can be changed via environment variable:
```bash
export ADMIN_PASSWORD="your-new-password"
```

---

## 📊 Sample Payment Data

After submitting the form, data appears in Supabase as:
```json
{
  "id": 1,
  "name": "John Doe",
  "date": "2026-01-22",
  "amount": "100.50",
  "receiver": "ITEME",
  "created_at": "2026-01-22T14:30:00+00:00"
}
```

---

## 🧪 Quick Test

### Test 1: Access Payment Form
```bash
curl http://localhost:5000/
# Should return HTML form
```

### Test 2: Submit Payment
```bash
curl -X POST http://localhost:5000/api/submit \
  -F "name=Test User" \
  -F "date=2026-01-22" \
  -F "amount=99.99" \
  -F "receiver=ITEME Charity"

# Expected: {"status": "success", "message": "Data saved successfully!"}
```

### Test 3: Access Admin Dashboard
```bash
# Open in browser (will prompt for password)
http://localhost:5000/admin

# Enter password: iteme2026
```

### Test 4: Get Admin Data (JSON)
```bash
PASS=$(echo -n "iteme2026" | base64)
curl "http://localhost:5000/api/admin/data?pwd=$PASS"

# Should return JSON array of all transactions
```

---

## 📁 Modified Files

- ✅ `/home/aime/ITEME/payment.py` - Main application file (updated)
- 📄 `/home/aime/ITEME/PAYMENT_UPDATE.md` - Detailed update summary (created)
- 📄 `/home/aime/ITEME/PAYMENT_API_README.md` - Complete API documentation (created)

---

## ⚠️ Important Notes

1. **Password Encoding:** When sending password via API, use Base64:
   ```javascript
   const password = "iteme2026";
   const encoded = btoa(password);  // Base64 encode
   fetch(`/api/admin/data?pwd=${encoded}`)
   ```

2. **Form Submission:** Uses FormData (multipart), not JSON
   ```javascript
   const formData = new FormData();
   formData.append('name', 'John Doe');
   fetch('/api/submit', { method: 'POST', body: formData })
   ```

3. **Supabase Storage:** All payments are stored in Supabase (cloud-based)
   - More reliable than local PostgreSQL
   - Automatic backups
   - Can be accessed from anywhere

4. **Admin Trust Status:** The Trust/Untrusted button saves to browser localStorage only
   - Not persisted to database
   - Resets when browser cache is cleared

---

## 🔗 Integration with main.py

If you want to run payment.py alongside main.py:

**Option A: Separate Ports**
```bash
# Terminal 1
python3 -m uvicorn main:app --port 8000

# Terminal 2
python3 -m uvicorn payment:app --port 5000
```

**Option B: Mount as Sub-app** (in main.py)
```python
from payment import app as payment_app

# Add after existing routes
app.mount("/payment", payment_app)

# Then access at: /payment/
# - GET http://localhost:8000/payment/
# - GET http://localhost:8000/payment/admin
# - POST http://localhost:8000/payment/api/submit
```

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'supabase'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "SUPABASE_URL is not set"
**Solution:** Check `.env` file is in `/home/aime/ITEME/` with correct credentials

### Issue: Table doesn't exist
**Solution:** Create table in Supabase SQL editor (see Step 2 above)

### Issue: 401 Unauthorized on admin
**Solution:** 
- Default password is `iteme2026`
- Must be Base64 encoded in URL
- Check ADMIN_PASSWORD environment variable

### Issue: Files won't download
**Solution:** Ensure required packages installed:
```bash
pip install openpyxl reportlab python-docx
```

---

## 📚 Documentation Files

Created during update:
1. **PAYMENT_UPDATE.md** - This file with quick start guide
2. **PAYMENT_API_README.md** - Comprehensive API documentation with all endpoints

Read these for more details:
- All endpoint parameters and responses
- Database schema documentation
- Security considerations
- Testing examples
- Error handling guide

---

## ✅ Verification

The payment.py file has been verified:
- ✓ FastAPI imports work
- ✓ Supabase client imports work
- ✓ All routes are registered
- ✓ No Flask/PostgreSQL dependencies
- ✓ FormData submission ready
- ✓ Admin authentication ready

You're ready to use the payment API!

---

**Next Action:** Run `python3 -m uvicorn payment:app --port 5000` and test the endpoints!
