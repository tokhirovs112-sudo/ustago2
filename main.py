from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from aiogram.types import Update
from bot import dp, bot, BOT_TOKEN

app = FastAPI(title="UstaGo Platformasi")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Renderdagi saytingizning aniq domeni (oxirida / bo'lmasin)
WEBHOOK_HOST = "https://ustagoorg.onrender.com"
WEBHOOK_PATH = f"/bot/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    # Sayt yoqilganda Telegramga Webhook manzilini ulab qo'yamiz
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
        }
    ]
