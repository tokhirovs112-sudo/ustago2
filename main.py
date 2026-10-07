import asyncio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# bot.py faylidan bot va dispatcher obyektlarini import qilamiz
from bot import dp, bot

app = FastAPI(title="UstaGo Platformasi")

# Statik fayllar va shablonlarni ulash
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# FastAPI ishga tushganda Telegram botni ham orqa fonda yurgizish
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoints
@app.get("/api/services")
async def get_services():
    return [
        {"id": 1, "name": "Maishiy texnika ta'miri", "icon": "Wrench"},
        {"id": 2, "name": "Santexnika xizmati", "icon": "Droplet"},
        {"id": 3, "name": "Elektrik xizmati", "icon": "Zap"},
        {"id": 4, "name": "Konditsioner ustalari", "icon": "Wind"}
    ]

@app.get("/api/technicians")
async def get_technicians():
    return [
        {
            "id": 1,
            "name": "Jasur Rahimov",
            "specialty": "Maishiy texnika ustasi",
            "rating": 4.9,
            "reviews_count": 28,
            "phone": "+998 90 123 45 67"
        },
        {
            "id": 2,
            "name": "Sardor Azimov",
            "specialty": "Professional Santexnik",
            "rating": 4.8,
            "reviews_count": 19,
            "phone": "+998 91 987 65 43"
        }
    ]

@app.get("/api/search")
async def search_services(q: str = ""):
    all_services = await get_services()
    if not q:
        return all_services
    filtered = [s for s in all_services if q.lower() in s["name"].lower()]
    return filtered
