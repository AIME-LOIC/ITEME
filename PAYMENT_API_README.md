# Payment API Documentation

## Overview
The `payment.py` module has been updated to:
1. ✅ Use **FastAPI** (instead of Flask) for consistency with main.py
2. ✅ Save payment data to **Supabase** (instead of PostgreSQL)
3. ✅ Add a "/" endpoint that serves the payment form
4. ✅ Maintain all existing admin and download functionality

## Supabase Table Structure

The payment data is stored in a Supabase table named **`transactions`** with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-incrementing primary key |
| `name` | TEXT | Full name of the payer |
| `date` | DATE | Payment date |
| `amount` | DECIMAL(10,2) | Payment amount |
| `receiver` | TEXT | Name of the payment receiver |
| `created_at` | TIMESTAMP | Auto-generated timestamp |

### Creating the Supabase Table

If you haven't created the table yet, run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE transactions (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  receiver TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security (RLS)
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Allow service role to access all data
CREATE POLICY "Enable access for service role" ON transactions
  FOR ALL USING (true)
  WITH CHECK (true);
```

## Endpoints

### Public Endpoints

#### `GET /`
Serves the payment submission form (HTML).

**Response:**
- HTML page with payment form

---

#### `POST /api/submit`
Submits payment data to be saved in Supabase.

**Request:**
```
Content-Type: application/x-www-form-urlencoded

Parameters:
- name (string): Full name
- date (string): Date in YYYY-MM-DD format
- amount (string): Payment amount
- receiver (string): Receiver name
```

**Response (Success - 201):**
```json
{
  "status": "success",
  "message": "Data saved successfully!"
}
```

**Response (Error - 400/500):**
```json
{
  "status": "error",
  "message": "Error description"
}
```

---

### Admin Endpoints

#### `GET /admin`
Serves the admin dashboard (password-protected).

**Query Parameters:**
- `pwd` (string, optional): Base64-encoded admin password

**Response:**
- HTML admin panel if password is correct
- Login page if password is missing/incorrect (401)

---

#### `GET /api/admin/data`
Fetches all transaction records in JSON format.

**Query Parameters:**
- `pwd` (string, required): Base64-encoded admin password

**Response (Success - 200):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "date": "2026-01-22",
    "amount": "100.00",
    "receiver": "ITEME",
    "created_at": "2026-01-22T10:30:00+00:00"
  },
  ...
]
```

**Response (Error - 401):**
```json
{"detail": "Unauthorized"}
```

---

#### `GET /api/admin/download`
Downloads all transaction records in multiple formats.

**Query Parameters:**
- `pwd` (string, required): Base64-encoded admin password
- `format` (string, optional): Download format
  - `csv` - Comma-separated values (default)
  - `excel` - Excel spreadsheet (.xlsx)
  - `pdf` - PDF document
  - `docx` - Word document (.docx)

**Response:**
- File download with appropriate MIME type

**Required Libraries:**
- CSV: Built-in
- Excel: `openpyxl`
- PDF: `reportlab`
- DOCX: `python-docx`

---

## Authentication

### Admin Password
The admin panel is protected by a password stored in the environment variable `ADMIN_PASSWORD` (default: `iteme2026`).

### Password Encoding
For API requests, the password must be Base64-encoded in the URL:

**Example:**
```python
import base64
password = "iteme2026"
encoded = base64.b64encode(password.encode()).decode()
url = f"/api/admin/data?pwd={encoded}"
```

---

## Integration with Main App

To integrate payment.py endpoints with main.py, use FastAPI's app mounting:

```python
# In main.py
from fastapi import FastAPI
from payment import app as payment_app

app = FastAPI()
# ... other routes ...

# Mount payment app at /payment path
app.mount("/payment", payment_app)
```

Then access payment endpoints at:
- `GET /payment/` - Payment form
- `POST /payment/api/submit` - Submit payment
- `GET /payment/admin` - Admin dashboard
- etc.

---

## Usage Example

### JavaScript Frontend
```javascript
// Submit payment form
const formData = new FormData();
formData.append('name', 'John Doe');
formData.append('date', '2026-01-22');
formData.append('amount', '100.00');
formData.append('receiver', 'ITEME');

const response = await fetch('/api/submit', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

### Fetch Admin Data (Python)
```python
import requests
import base64

password = "iteme2026"
encoded = base64.b64encode(password.encode()).decode()
url = f"http://localhost:8000/api/admin/data?pwd={encoded}"

response = requests.get(url)
data = response.json()
print(data)
```

---

## Running the Payment API

### Standalone Mode
```bash
cd /home/aime/ITEME
source installed/bin/activate
uvicorn payment:app --port 5000
```

### With Supabase
Ensure your `.env` file contains:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_PASSWORD` | `iteme2026` | Admin panel password |
| `SUPABASE_URL` | Required | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Required | Service role key for database access |

---

## Error Handling

All endpoints return appropriate HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request / Bad format |
| 401 | Unauthorized (wrong password) |
| 500 | Server error |

---

## Differences from Previous Version

| Feature | Old (Flask + PostgreSQL) | New (FastAPI + Supabase) |
|---------|--------------------------|-------------------------|
| Framework | Flask | FastAPI |
| Database | PostgreSQL | Supabase (PostgreSQL managed) |
| Database Connection | Direct psycopg2 | Supabase Python SDK |
| Request Handling | JSON Content-Type | Form-encoded |
| Form Validation | Manual | FastAPI built-in |
| "/" Endpoint | ✅ Yes | ✅ Yes |
| Admin Dashboard | ✅ Yes | ✅ Yes |
| Download Formats | CSV, Excel, PDF, DOCX | CSV, Excel, PDF, DOCX |

---

## Testing

### Test the "/" endpoint
```bash
curl http://localhost:8000/
```

### Test Form Submission
```bash
curl -X POST http://localhost:8000/api/submit \
  -F "name=Test User" \
  -F "date=2026-01-22" \
  -F "amount=50.00" \
  -F "receiver=ITEME"
```

### Test Admin Access
```bash
# Get password in base64
ENCODED_PWD=$(echo -n "iteme2026" | base64)

# Fetch admin data
curl "http://localhost:8000/api/admin/data?pwd=$ENCODED_PWD"

# Download as CSV
curl "http://localhost:8000/api/admin/download?pwd=$ENCODED_PWD&format=csv" -o transactions.csv
```

---

## Next Steps

1. ✅ Create the `transactions` table in Supabase
2. ✅ Start the payment API server
3. ✅ Test the endpoints
4. (Optional) Integrate with main.py using app mounting
5. (Optional) Add the transaction table to your Supabase dashboard for manual management
