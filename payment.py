import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Note: In a production environment, these would be environment variables.
# Using standard PostgreSQL environment variables or defaults.
DB_CONFIG = {
    "dbname": os.environ.get("POSTGRES_DB", "postgres"),
    "user": os.environ.get("POSTGRES_USER", "postgres"),
    "password": os.environ.get("POSTGRES_PASSWORD", "password"),
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": os.environ.get("POSTGRES_PORT", "5432"),
}

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def init_db():
    """Initializes the database schema."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            date DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            receiver TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Initialize the DB on startup
try:
    init_db()
except Exception as e:
    print(f"Database initialization failed: {e}")

# --- API ROUTES ---

@app.route('/api/submit', methods=['POST'])
def submit_data():
    """Endpoint to save form data to PostgreSQL."""
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (name, date, amount, receiver) VALUES (%s, %s, %s, %s)",
            (data['name'], data['date'], data['amount'], data['receiver'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": "Data saved successfully!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/admin/data', methods=['GET'])
def get_data():
    """Endpoint for the admin panel to fetch all records."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM transactions ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- FRONTEND ROUTE ---

@app.route('/')
def index():
    """Serves the combined frontend HTML."""
    return render_template_string(HTML_TEMPLATE)

# --- HTML/CSS/JS ASSETS ---

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transaction Manager</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .nav-link.active { border-bottom: 2px solid #3b82f6; color: #3b82f6; }
    </style>
</head>
<body class="bg-gray-50 min-h-screen font-sans">

    <nav class="bg-white shadow-sm mb-8">
        <div class="max-w-4xl mx-auto px-4">
            <div class="flex space-x-8">
                <button onclick="showTab('form-tab')" id="nav-form" class="nav-link py-4 px-2 font-semibold active">Submit Entry</button>
                <button onclick="showTab('admin-tab')" id="nav-admin" class="nav-link py-4 px-2 font-semibold text-gray-500 hover:text-blue-500 transition">Admin Panel</button>
            </div>
        </div>
    </nav>

    <main class="max-w-4xl mx-auto px-4 pb-12">
        
        <!-- Submission Form Tab -->
        <section id="form-tab" class="tab-content active">
            <div class="bg-white p-8 rounded-xl shadow-md border border-gray-100">
                <h2 class="text-2xl font-bold mb-6 text-gray-800">Check-In Transaction</h2>
                <form id="submissionForm" class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Full Names</label>
                            <input type="text" id="name" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
                            <input type="date" id="date" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Amount ($)</label>
                            <input type="number" step="0.01" id="amount" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Receiver</label>
                            <input type="text" id="receiver" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                    </div>
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 transition transform active:scale-95 shadow-lg">
                        Check In
                    </button>
                </form>
                <div id="statusMessage" class="mt-4 hidden p-3 rounded-lg text-center font-medium"></div>
            </div>
        </section>

        <!-- Admin Panel Tab -->
        <section id="admin-tab" class="tab-content">
            <div class="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-gray-800">Admin Dashboard</h2>
                    <button onclick="fetchAdminData()" class="text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-md transition">Refresh Data</button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-50 border-b">
                                <th class="p-3 text-sm font-semibold text-gray-600">ID</th>
                                <th class="p-3 text-sm font-semibold text-gray-600">Name</th>
                                <th class="p-3 text-sm font-semibold text-gray-600">Date</th>
                                <th class="p-3 text-sm font-semibold text-gray-600">Amount</th>
                                <th class="p-3 text-sm font-semibold text-gray-600">Receiver</th>
                            </tr>
                        </thead>
                        <tbody id="adminTableBody">
                            <!-- Data injected here -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

    </main>

    <script>
        // Tab switching logic
        function showTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            const navId = tabId === 'form-tab' ? 'nav-form' : 'nav-admin';
            document.getElementById(navId).classList.add('active');

            if(tabId === 'admin-tab') fetchAdminData();
        }

        // Handle Form Submission
        document.getElementById('submissionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const statusBox = document.getElementById('statusMessage');
            
            const formData = {
                name: document.getElementById('name').value,
                date: document.getElementById('date').value,
                amount: parseFloat(document.getElementById('amount').value),
                receiver: document.getElementById('receiver').value
            };

            try {
                const response = await fetch('/api/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                statusBox.textContent = result.message;
                statusBox.className = `mt-4 p-3 rounded-lg text-center font-medium ${result.status === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`;
                statusBox.classList.remove('hidden');

                if(result.status === 'success') {
                    document.getElementById('submissionForm').reset();
                    setTimeout(() => statusBox.classList.add('hidden'), 3000);
                }
            } catch (err) {
                statusBox.textContent = "Error connecting to server.";
                statusBox.className = "mt-4 p-3 rounded-lg text-center font-medium bg-red-100 text-red-700";
                statusBox.classList.remove('hidden');
            }
        });

        // Fetch Admin Table Data
        async function fetchAdminData() {
            const tableBody = document.getElementById('adminTableBody');
            tableBody.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-gray-500">Loading records...</td></tr>';
            
            try {
                const response = await fetch('/api/admin/data');
                const data = await response.json();
                
                tableBody.innerHTML = '';
                if(data.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-gray-400">No records found.</td></tr>';
                    return;
                }

                data.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.className = "border-b hover:bg-gray-50 transition";
                    tr.innerHTML = `
                        <td class="p-3 text-sm text-gray-500">${row.id}</td>
                        <td class="p-3 text-sm font-medium text-gray-800">${row.name}</td>
                        <td class="p-3 text-sm text-gray-600">${row.date}</td>
                        <td class="p-3 text-sm text-green-600 font-bold">$${parseFloat(row.amount).toFixed(2)}</td>
                        <td class="p-3 text-sm text-gray-600">${row.receiver}</td>
                    `;
                    tableBody.appendChild(tr);
                });
            } catch (err) {
                tableBody.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-red-500">Failed to load data.</td></tr>';
            }
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # Using threaded mode for development convenience
    app.run(host='0.0.0.0', port=5000, debug=True)
