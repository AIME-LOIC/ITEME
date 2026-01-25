# Supabase Database Setup Guide

## Create the "payments" Table (Separate from Arrivals)

This table stores payment records independently from student arrival tracking.

### SQL Schema

Run this in your Supabase SQL Editor:

```sql
-- Create payments table (separate from arrival data)
CREATE TABLE IF NOT EXISTS payments (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  receiver TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at DESC);

-- Enable Row Level Security
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- Allow service role to access all data
CREATE POLICY "Enable service role access" ON payments
  FOR ALL 
  USING (true)
  WITH CHECK (true);
```

## Create the "arrival" Table (Separate from Payments)

This table tracks student attendance, separate from payment records.

### SQL Schema

```sql
-- Create arrival table (separate from payment data)
CREATE TABLE IF NOT EXISTS arrival (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  student_name TEXT NOT NULL,
  class_name TEXT NOT NULL,
  status TEXT DEFAULT 'waiting',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_arrival_created_at ON arrival(created_at DESC);

-- Enable Row Level Security
ALTER TABLE arrival ENABLE ROW LEVEL SECURITY;

-- Allow service role to access all data
CREATE POLICY "Enable service role access" ON arrival
  FOR ALL 
  USING (true)
  WITH CHECK (true);
```

---

## Table Structure

### payments table
| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-incrementing primary key |
| `name` | TEXT | Payer's full name |
| `date` | DATE | Payment date |
| `amount` | DECIMAL(10,2) | Payment amount in dollars |
| `receiver` | TEXT | Receiver/beneficiary name |
| `created_at` | TIMESTAMP | Auto-generated timestamp |

### arrival table
| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-incrementing primary key |
| `student_name` | TEXT | Student's full name |
| `class_name` | TEXT | Class/grade name |
| `status` | TEXT | Status (waiting/active) |
| `created_at` | TIMESTAMP | Auto-generated timestamp |

---

## Why Separate Tables?

✅ **Data Organization:** Payments and attendance are independent systems
✅ **Security:** Can apply different access rules to each table
✅ **Performance:** Faster queries when tables are smaller
✅ **Scalability:** Easy to manage and backup separately
✅ **Clarity:** Clear separation of concerns (payments ≠ attendance)

---

## Testing Your Setup

### 1. Check if tables exist:
```sql
SELECT tablename FROM pg_tables WHERE schemaname='public';
```

### 2. Insert test payment:
```sql
INSERT INTO payments (name, date, amount, receiver)
VALUES ('Test User', '2026-01-22', 100.00, 'ITEME')
RETURNING *;
```

### 3. Insert test arrival:
```sql
INSERT INTO arrival (student_name, class_name, status)
VALUES ('John Doe', 'Grade 10', 'waiting')
RETURNING *;
```

### 4. Verify data:
```sql
SELECT * FROM payments;
SELECT * FROM arrival;
```

---

## API Usage

### Payment Endpoints
- `GET /` - Payment submission form
- `POST /api/submit` - Submit payment
- `GET /admin` - Payment admin dashboard
- `GET /api/admin/data?pwd=<encoded>` - Get payment records (JSON)
- `GET /api/admin/download?pwd=<encoded>&format=csv` - Download payments

### Arrival Endpoints
- `POST /arrival` - Submit arrival
- `GET /arrival/admin` - Arrival dashboard
- `POST /activate/{student_id}` - Activate student

---

## Supabase Configuration

Ensure your `.env` file contains:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
ADMIN_PASSWORD=iteme2026
```

---

## Fixed Issues

✅ Fixed Supabase query syntax (removed `.select()` after `.insert()`)
✅ Changed table name from "transactions" to "payments"
✅ Improved error handling with fallback messages
✅ Created separate "payments" table independent from "arrival"

