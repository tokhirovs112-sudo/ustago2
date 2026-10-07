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

# To'liq ma'lumotlar bazasi (Kategoriyalar va xizmatlar)
CATEGORIES_DB = {
    "Maishiy texnika": {
        "icon": "Wrench",
        "services": ["Kir yuvish mashinasi", "Sovutgich", "Televizor", "Mikroto'lqinli pech"]
    },
    "Santexnika": {
        "icon": "Droplet",
        "services": ["Krani almashtirish", "Unitaz o'rnatish", "Truba tozalash", "Nasos ta'mirlash"]
    },
    "Elektrik": {
        "icon": "Zap",
        "services": ["Rozetka o'rnatish", "Lyustra osish", "Simlar almashinuvi", "Avtomat qo'yish"]
    },
    "Konditsioner": {
        "icon": "Wind",
        "services": ["Fread quyish", "Tozalash", "Montaj qilish", "Ta'mirlash"]
    }
}

TECHNICIANS_DB = [
    {
        "id": 1,
        "name": "Jasur Rahimov",
        "category": "Maishiy texnika",
        "service": "Kir yuvish mashinasi",
        "district": "Yunusobod",
        "rating": 4.9,
        "reviews_count": 28,
        "phone": "+998 90 123 45 67",
        "price": "50,000 so'mdan"
    },
    {
        "id": 2,
        "name": "Sardor Azimov",
        "category": "Santexnika",
        "service": "Krani almashtirish",
        "district": "Chilonzor",
        "rating": 4.8,
        "reviews_count": 19,
        "phone": "+998 91 987 65 43",
        "price": "40,000 so'mdan"
    },
    {
        "id": 3,
        "name": "Bekzod Karimov",
        "category": "Elektrik",
        "service": "Rozetka o'rnatish",
        "district": "Mirzo Ulug'bek",
        "rating": 5.0,
        "reviews_count": 34,
        "phone": "+998 93 333 22 11",
        "price": "30,000 so'mdan"
    },
    {
        "id": 4,
        "name": "Anvar Tursunov",
        "category": "Konditsioner",
        "service": "Tozalash",
        "district": "Mirobod",
        "rating": 4.7,
        "reviews_count": 15,
        "phone": "+998 99 777 55 44",
        "price": "80,000 so'mdan"
    }
]

@app.get("/")
async def home(request: Request):
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
    
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "request": request, 
            "categories": CATEGORIES_DB,
            "districts": districts_data,
            "reviews_db": []
        }
    )

@app.get("/api/services")
async def get_services(category: str = ""):
    if category and category in CATEGORIES_DB:
        return [{"name": s} for s in CATEGORIES_DB[category]["services"]]
    
    # Agar kategoriya berilmagan bo'lsa, hamma xizmatlarni qaytaramiz
    all_services = []
    for cat_name, cat_data in CATEGORIES_DB.items():
        for s in cat_data["services"]:
            all_services.append({"name": s, "category": cat_name})
    return all_services

@app.get("/api/technicians")
async def get_technicians(category: str = "", service: str = "", district: str = ""):
    result = TECHNICIANS_DB
    if category:
        result = [t for t in result if t["category"] == category]
    if service:
        result = [t for t in result if t["service"] == service]
    if district and district != "Barchasi (Hudud bo'yicha)":
        result = [t for t in result if t["district"] == district]
    return result

@app.get("/api/search")
async def search_services(query: str = ""):
    if not query:
        return []
    matched = []
    for cat_name, cat_data in CATEGORIES_DB.items():
        for s in cat_data["services"]:
            if query.lower() in s.lower() or query.lower() in cat_name.lower():
                matched.append({"name": s, "category": cat_name})
    return matched
