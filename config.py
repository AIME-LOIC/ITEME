# config.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file locally (optional, Render uses system env vars)
load_dotenv()

# Supabase config
SUPABASE_URL = os.getenv("https://ruxiswyfpkbatnzcbvog.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1eGlzd3lmcGtiYXRuemNidm9nIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjQ4Mjg3NiwiZXhwIjoyMDc4MDU4ODc2fQ.ZORdALaEwnazZX0045UB5bNF--vta8dduHoYGv00UhY")
SUPABASE_ANON_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1eGlzd3lmcGtiYXRuemNidm9nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0ODI4NzYsImV4cCI6MjA3ODA1ODg3Nn0.M7lYjHx5rPo3fziZtmi4FP-skH6FVKopCjM5O2246QY")

# Validate env variables
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is not set in environment variables")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY is not set in environment variables")
if not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_ANON_KEY is not set in environment variables")

# Create Supabase client for backend (admin access)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
