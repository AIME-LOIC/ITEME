# config.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

# Fetch environment variables
SUPABASE_URL = os.getenv("https://ruxiswyfpkbatnzcbvog.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1eGlzd3lmcGtiYXRuemNidm9nIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjQ4Mjg3NiwiZXhwIjoyMDc4MDU4ODc2fQ.ZORdALaEwnazZX0045UB5bNF--vta8dduHoYGv00UhY")
SUPABASE_ANON_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1eGlzd3lmcGtiYXRuemNidm9nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0ODI4NzYsImV4cCI6MjA3ODA1ODg3Nn0.M7lYjHx5rPo3fziZtmi4FP-skH6FVKopCjM5O2246QY")  # optional, if needed

# Validate required variables
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is not set in environment variables")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY is not set in environment variables")

# Initialize Supabase client using the service role key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Optional: function to switch between anon key and service role
def get_supabase_client(use_anon=False) -> Client:
    """
    Returns Supabase client.
    use_anon: if True, uses ANON_KEY instead of SERVICE_ROLE_KEY
    """
    key = SUPABASE_ANON_KEY if use_anon else SUPABASE_SERVICE_ROLE_KEY
    if not key:
        raise ValueError("Requested Supabase key is not set")
    return create_client(SUPABASE_URL, key)
