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

# O'zbekistonning 12 viloyati, Toshkent shahri va Qoraqalpog'iston
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

# Kasblar va zamonaviy IT / maishiy xizmatlar bazasi
SERVICES_DB = [
    {"name": "Wi-Fi router va internet ustasi", "category": "IT & Tarmoqlar", "description": "Wi-Fi routerni sozlash, internet uzilishlarini bartaraf etish, LAN kabel tortish"},
    {"name": "Kompyuter va noutbuk ustasi", "category": "IT & Kompyuter", "description": "Windows o'rnatish, qotishni to'g'rilash, dasturlar va drayverlar yozish"},
    {"name": "Videokuzatuv kameralari", "category": "Xavfsizlik", "description": "Kamera va domofonlar o'rnatish, sozlash, telefon orqali ko'rsatish"},
    {"name": "Smart TV va televizor ustasi", "category": "Elektronika", "description": "Televizorni devorga osish, kanal va internetga ulash"},
    {"name": "Santexnik", "category": "Santexnika", "description": "Truba, kran, unitaz va isitish tizimlari ustasi"},
    {"name": "Elektrik", "category": "Elektrik", "description": "Rozetka, lyustra, simlar va elektr xavfsizligi"},
    {"name": "Telefon ustasi", "category": "Elektronika", "description": "Smartfon va planshetlarni ta'mirlash, ekran almashtirish"},
    {"name": "Konditsioner ustasi", "category": "Iqlim texnikasi", "description": "Konditsioner o'rnatish, tozalash va freon quyish"},
    {"name": "Kir yuvish mashinasi ustasi", "category": "Maishiy texnika", "description": "Barcha turdagi kir yuvish mashinalarini ta'mirlash"},
    {"name": "Mebel ustasi", "category": "Uy jihozlari", "description": "Mebellarni yig'ish, o'rnatish va ta'mirlash"}
]

TECHNICIANS_DB = [
    {
        "id": 1,
        "name": "Alisher Saidov",
        "job": "Wi-Fi router va internet ustasi",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 45,
        "phone": "+998 90 999 88 77",
        "price": "40,000 so'mdan"
    },
    {
        "id": 2,
        "name": "Jasur Rahimov",
        "job": "Kir yuvish mashinasi ustasi",
        "region": "Toshkent shahri",
        "rating": 4.9,
        "reviews_count": 28,
        "phone": "+998 90 123 45 67",
        "price": "50,000 so'mdan"
    },
    {
        "id": 3,
        "name": "Sardor Azimov",
        "job": "Santexnik",
        "region": "Farg'ona viloyati",
        "rating": 4.8,
        "reviews_count": 19,
        "phone": "+998 91 987 65 43",
        "price": "40,000 so'mdan"
    },
    {
        "id": 4,
        "name": "Bekzod Karimov",
        "job": "Elektrik",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 34,
        "phone": "+998 93 333 22 11",
        "price": "30,000 so'mdan"
    },
    {
        "id": 5,
        "name": "Anvar Tursunov",
        "job": "Konditsioner ustasi",
        "region": "Samarqand viloyati",
        "rating": 4.7,
        "reviews_count": 15,
        "phone": "+998 99 777 55 44",
        "price": "80,000 so'mdan"
    },
    {
        "id": 6,
        "name": "Sanjar Turgunov",
        "job": "Kompyuter va noutbuk ustasi",
        "region": "Andijon viloyati",
        "rating": 4.9,
        "reviews_count": 51,
        "phone": "+998 94 444 33 22",
        "price": "50,000 so'mdan"
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
            "reviews_db": []
        }
    )

@app.get("/api/services")
async def get_services(query: str = ""):
    if not query:
        return SERVICES_DB
    filtered = [s for s in SERVICES_DB if query.lower() in s["name"].lower() or query.lower() in s["description"].lower()]
    return filtered

@app.get("/api/technicians")
async def get_technicians(job: str = "", region: str = ""):
    result = TECHNICIANS_DB
    if job:
        result = [t for t in result if job.lower() in t["job"].lower()]
    if region and region != "Barcha hududlar":
        result = [t for t in result if t["region"].lower() == region.lower()]
    return result

@app.get("/api/search")
async def search_jobs(query: str = ""):
    if not query:
        return SERVICES_DB
    matched = [s for s in SERVICES_DB if query.lower() in s["name"].lower()]
    return matched
