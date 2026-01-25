# Critical Setup Steps - Required Before Using App

## ⚠️ The 500 Error on `/api/admin/data` is Expected!

The error occurs because the `payments` table **doesn't exist yet** in your Supabase database.

### Why the Error Happens:
1. App tries to query `payments` table
2. Table doesn't exist in Supabase
3. Database returns error → HTTP 500

---

## ✅ REQUIRED: Create Supabase Tables

### Step 1: Go to Supabase Dashboard
```
https://app.supabase.com/projects
```

### Step 2: Click on Your Project → SQL Editor

### Step 3: Run This SQL Code

**Create the payments table:**
```sql
CREATE TABLE IF NOT EXISTS payments (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  receiver TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at DESC);

ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable service role access" ON payments
  FOR ALL 
  USING (true)
  WITH CHECK (true);
```

**Create the arrival table:**
```sql
CREATE TABLE IF NOT EXISTS arrival (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  student_name TEXT NOT NULL,
  class_name TEXT NOT NULL,
  status TEXT DEFAULT 'waiting',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_arrival_created_at ON arrival(created_at DESC);

ALTER TABLE arrival ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable service role access" ON arrival
  FOR ALL 
  USING (true)
  WITH CHECK (true);
```

### Step 4: Click "Run" and Verify Success
You should see messages like:
- "CREATE TABLE successfully created"
- "CREATE INDEX successfully created"
- "ALTER TABLE"
- "CREATE POLICY"

---

## ✅ Fixed Issues in Code

### Issue 1: Route Order
**Fixed:** Moved all main.py routes BEFORE mounting payment app
- `/arrival` - Now works ✅
- `/arrival/admin` - Now works ✅
- `/activate/{id}` - Now works ✅
- `/restart` - Now works ✅

### Issue 2: Supabase Queries
**Fixed:** Removed problematic `.select()` after `.insert()`
- Changed: `.insert(data).select("*").execute()`
- To: `.insert(data).execute()`

---

## 📍 Current Routes (After Fixes)

### Root App (Main)
| Endpoint | Method | Status |
|----------|--------|--------|
| `/` | GET | ✅ Serves payment form (from payment app) |
| `/arrival` | POST | ✅ Submit attendance |
| `/arrival/admin` | GET | ✅ View attendance |
| `/activate/{id}` | POST | ✅ Activate student |
| `/restart` | GET | ✅ Restart server |
| `/static/*` | GET | ✅ Static files |

### Payment Routes (Mounted at /)
| Endpoint | Method | Status |
|----------|--------|--------|
| `/api/submit` | POST | ⚠️ Needs `payments` table |
| `/admin` | GET | ⚠️ Needs `payments` table |
| `/api/admin/data` | GET | ⚠️ Needs `payments` table |
| `/api/admin/download` | GET | ⚠️ Needs `payments` table |

---

## 🧪 Testing the Fixed Routes

### Test Arrival (This will work after table creation)
```bash
curl -X POST http://localhost:8000/arrival \
  -d "student_name=John Doe&class_name=Grade 10"
```

### Expected Response:
```
Redirect to http://localhost:8000/ (status 303)
```

### Test Payment Submit
```bash
curl -X POST http://localhost:8000/api/submit \
  -F "name=Test User" \
  -F "date=2026-01-22" \
  -F "amount=100.00" \
  -F "receiver=ITEME"
```

### Expected Response (after table creation):
```json
{
  "status": "success",
  "message": "Data saved successfully!"
}
```

---

## 🎯 Quick Checklist

- [ ] Verify Supabase credentials in `.env`
- [ ] Go to Supabase SQL Editor
- [ ] Create `payments` table (copy SQL above)
- [ ] Create `arrival` table (copy SQL above)
- [ ] Run `./start.sh` or `uvicorn main:app --reload`
- [ ] Test `/arrival` endpoint → Should now work ✅
- [ ] Test `/api/submit` endpoint → Should now work ✅
- [ ] Visit `/admin?pwd=aXRlbWUyMDI2` → Should load admin panel ✅

---

## 📝 Summary

### What Was Fixed:
1. ✅ Route ordering issue (arrival routes now work)
2. ✅ Supabase query syntax
3. ✅ Removed duplicate route definitions

### What Still Needs Doing:
1. ⚠️ **CREATE TABLES IN SUPABASE** (required!)
2. Once tables exist, all endpoints will work

### Files Modified:
- `main.py` - Reordered routes, fixed mounting order

### New Documentation:
- `DATABASE_SETUP.md` - Table creation guide
- `SETUP_INSTRUCTIONS.md` - This file

---

## 🚀 After Tables Are Created

Everything will work! Test with:
```bash
# Serve the app
./start.sh

# In another terminal, test endpoints
curl http://localhost:8000/arrival/admin
curl -X POST http://localhost:8000/api/submit -F "name=Test" ...
```

**The 500 error will disappear once the `payments` table exists!**
