from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from aiogram.types import Update
from bot import dp, bot, BOT_TOKEN

app = FastAPI(title="UstaGo Platformasi")

# Statik fayllar va shablonlar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Renderdagi saytingizning aniq domeni
WEBHOOK_HOST = "https://ustagoorg.onrender.com"
WEBHOOK_PATH = f"/bot/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook o'rnatildi: {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()

# Telegramdan keladigan xabarlarni qabul qiluvchi endpoint
@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    json_data = await request.json()
    update = Update.model_validate(json_data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def home(request: Request):
    categories_data = {
        "Maishiy texnika": "Wrench",
        "Santexnika": "Droplet",
        "Elektrik": "Zap",
        "Konditsioner": "Wind"
    }
    
    districts_data = [
        "Barchasi (Hudud bo'yicha)",
        "Yunusobod",
        "Mirzo Ulug'bek",
        "Chilonzor",
        "Mirobod",
        "Shayxontohur",
        "Olmazor",
        "Uchtepa",
        "Yakkasaroy",
        "Yashnobod",
        "Sergeli"
    ]
    
    reviews_db = []
    
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "request": request, 
            "categories": categories_data,
            "districts": districts_data,
            "reviews_db": reviews_db
        }
    )

# API Endpoints
@app.get("/api/services")
async def get_services(category: str = ""):
    return [
        {"id": 1, "name": "Maishiy texnika ta'miri", "icon": "Wrench"},
        {"id": 2, "name": "Santexnika xizmati", "icon": "Droplet"},
        {"id": 3, "name": "Elektrik xizmati", "icon": "Zap"},
        {"id": 4, "name": "Konditsioner ustalari", "icon": "Wind"}
    ]

@app.get("/api/technicians")
async def get_technicians(category: str = "", service: str = "", district: str = ""):
    return [
        {
            "id": 1,
            "name": "Jasur Rahimov",
            "specialty": service or "Maishiy texnika ustasi",
            "rating": 4.9,
            "reviews_count": 28,
            "phone": "+998 90 123 45 67"
        },
        {
            "id": 2,
            "name": "Sardor Azimov",
            "specialty": service or "Professional Usta",
            "rating": 4.8,
            "reviews_count": 19,
            "phone": "+998 91 987 65 43"
        }
    ]

@app.get("/api/search")
async def search_services(query: str = ""):
    all_services = await get_services()
    if not query:
        return all_services
    filtered = [s for s in all_services if query.lower() in s["name"].lower()]
    return filtered
