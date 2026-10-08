from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Undefined
from aiogram.types import Update
from bot import dp, bot, BOT_TOKEN

class SilentUndefined(Undefined):
    def __str__(self):
        return ""
    def __iter__(self):
        return iter([])
    def __getattr__(self, name):
        return self
    def __call__(self, *args, **kwargs):
        return self

app = FastAPI(title="UstaGo Platformasi", debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

templates.env.undefined = SilentUndefined

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

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    json_data = await request.json()
    update = Update.model_validate(json_data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# O'zbekistonning hududlari
REGIONS_DB = [
    "Toshkent shahri",
    "Toshkent viloyati",
    "Farg'ona viloyati",
    "Andijon viloyati",
    "Namangan viloyati",
    "Samarqand viloyati",
    "Buxoro viloyati",
    "Qashqadaryo viloyati",
    "Surxondaryo viloyati",
    "Jizzax viloyati",
    "Sirdaryo viloyati",
    "Navoiy viloyati",
    "Xorazm viloyati",
    "Qoraqalpog'iston Respublikasi"
]

# Kategoriyalar va ularning ichidagi ishlar (ustalar faoliyatiga asoslangan)
CATEGORIES_DB = {
    "Xavfsizlik va tarmoqlar": {
        "icon": "Shield",
        "services": ["Kamera o'rnatish", "Wi-Fi router sozlash"]
    },
    "Iqlim texnikasi": {
        "icon": "Wind",
        "services": ["Konditsioner o'rnatish va sozlash"]
    },
    "Maishiy texnika": {
        "icon": "Wrench",
        "services": ["Kir yuvish mashinasi ta'miri"]
    }
}

SERVICES_DB = [
    {"name": "Kamera o'rnatish", "category": "Xavfsizlik va tarmoqlar", "description": "Videokuzatuv kameralarini o'rnatish va sozlash"},
    {"name": "Wi-Fi router sozlash", "category": "Xavfsizlik va tarmoqlar", "description": "Wi-Fi routerni ulash va internetni sozlash"},
    {"name": "Konditsioner o'rnatish va sozlash", "category": "Iqlim texnikasi", "description": "Konditsionerlarni montaj qilish va ta'mirlash"},
    {"name": "Kir yuvish mashinasi ta'miri", "category": "Maishiy texnika", "description": "Kir yuvish mashinalarini sifatli ta'mirlash"}
]

# Siz taqdim etgan real ustalar bazasi (Real usta belgisi bilan)
TECHNICIANS_DB = [
    {
        "id": 1,
        "name": "Nikita",
        "job": "Kamera o'rnatish",
        "category": "Xavfsizlik va tarmoqlar",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 31,
        "phone": "+998 99 642 06 70",
        "price": "Kelishilgan holda",
        "is_real": True
    },
    {
        "id": 2,
        "name": "Doston",
        "job": "Wi-Fi router sozlash",
        "category": "Xavfsizlik va tarmoqlar",
        "region": "Toshkent shahri",
        "rating": 4.9,
        "reviews_count": 24,
        "phone": "+998 99 888 08 02",
        "price": "Kelishilgan holda",
        "is_real": True
    },
    {
        "id": 3,
        "name": "Nizom",
        "job": "Konditsioner o'rnatish va sozlash",
        "category": "Iqlim texnikasi",
        "region": "Toshkent shahri",
        "rating": 4.8,
        "reviews_count": 19,
        "phone": "+998 94 504 09 99",
        "price": "Kelishilgan holda",
        "is_real": True
    },
    {
        "id": 4,
        "name": "Dostonbek",
        "job": "Kamera o'rnatish",
        "category": "Xavfsizlik va tarmoqlar",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 40,
        "phone": "+998 90 912 31 61",
        "price": "Kelishilgan holda",
        "is_real": True
    },
    {
        "id": 5,
        "name": "Aleksandr",
        "job": "Kir yuvish mashinasi ta'miri",
        "category": "Maishiy texnika",
        "region": "Toshkent shahri",
        "rating": 4.9,
        "reviews_count": 27,
        "phone": "+998 90 353 91 08",
        "price": "Kelishilgan holda",
        "is_real": True
    }
]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "request": request, 
            "regions": REGIONS_DB,
            "services": SERVICES_DB,
            "categories": CATEGORIES_DB,
            "districts": REGIONS_DB,
            "reviews_db": []
        }
    )

@app.get("/api/services")
async def get_services(query: str = "", category: str = ""):
    if category and category in CATEGORIES_DB:
        return [{"name": s} for s in CATEGORIES_DB[category]["services"]]
    if not query:
        return SERVICES_DB
    filtered = [s for s in SERVICES_DB if query.lower() in s["name"].lower() or query.lower() in s["description"].lower()]
    return filtered

@app.get("/api/technicians")
async def get_technicians(job: str = "", region: str = "", category: str = ""):
    result = TECHNICIANS_DB
    if category:
        result = [t for t in result if t.get("category") == category]
    if job:
        result = [t for t in result if job.lower() in t["job"].lower()]
    if region and region != "Barcha hududlar" and region != "Barchasi (Hudud bo'yicha)":
        result = [t for t in result if region.lower() in t["region"].lower()]
    return result

@app.get("/api/search")
async def search_jobs(query: str = ""):
    if not query:
        return SERVICES_DB
    matched = [s for s in SERVICES_DB if query.lower() in s["name"].lower()]
    return matched
