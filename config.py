# config.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

# Fetch environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")   # optional, if needed

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
