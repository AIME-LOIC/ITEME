from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
