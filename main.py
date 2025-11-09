from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from threading import Thread
import time, requests, os, signal
from config import supabase  # ✅ Import Supabase client

app = FastAPI()

# Serve templates
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------
# Routes
# -------------------

@app.get("/")
def parent_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/arrival")
def add_arrival(request: Request, student_name: str = Form(...), class_name: str = Form(...)):
    try:
        data = {
            "student_name": student_name,
            "class_name": class_name,
            "status": "waiting"
        }
        supabase.table("arrival").insert(data).execute()
    except Exception as e:
        return {"error": str(e)}

    return RedirectResponse("/", status_code=303)


@app.get("/admin")
def admin_dashboard(request: Request):
    try:
        result = supabase.table("arrival").select("*").order("id", desc=True).execute()
        arrivals = result.data
    except Exception as e:
        arrivals = []
    return templates.TemplateResponse("admin.html", {"request": request, "arrivals": arrivals})
@app.post("/activate/{student_id}")
def activate_student(student_id: int):
    try:
        response = supabase.table("arrival").update({"status": "active"}).eq("id", student_id).execute()
        if response.error:
            return {"status": "error", "message": response.error.message}
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}



# -------------------
# Keep-Alive + Auto-Restart Section
# -------------------

RENDER_URL = "https://iteme-charity-wk9f.onrender.com"  # 🔁 replace with your real Render URL

def keep_alive():
    """Ping the app every 10 minutes to prevent sleeping (for free plans)."""
    while True:
        try:
            res = requests.get(RENDER_URL, timeout=10)
            print(f"[KeepAlive] Pinged {RENDER_URL} -> {res.status_code}")
        except Exception as e:
            print("[KeepAlive] Ping failed:", e)
        time.sleep(600)  # every 10 minutes


@app.get("/restart")
def restart_server():
    """Manual restart endpoint (private use)."""
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "Server restarting..."}


# Start keep-alive thread
Thread(target=keep_alive, daemon=True).start()
