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

CATEGORIES_DB = {
    "Telefon va Gadjetlar": {
        "services": ["Telefon ekranini almashtirish", "Akkumulyator almashtirish", "Smartfon ta'miri"]
    },
    "Xavfsizlik va tarmoqlar": {
        "services": ["Kamera o'rnatish", "Wi-Fi router sozlash"]
    },
    "Iqlim texnikasi": {
        "services": ["Konditsioner o'rnatish va sozlash"]
    },
    "Maishiy texnika": {
        "services": ["Kir yuvish mashinasi ta'miri"]
    }
}

# Barcha ustalar bazasi (Yangi "OYNACHI" servisi ham qo'shildi)
TECHNICIANS_DB = [
    {
        "id": 1,
        "name": "Nikita",
        "job": "Kamera o'rnatish",
        "category": "Xavfsizlik va tarmoqlar",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 31,
        "phone": "+998996420670",
        "price": "Kelishilgan holda",
        "is_real": True,
        "description": "Malakali mutaxassis. Xonadonlar, office va obyektlarga zamonaviy videokuzatuv kameralarini sifatli o'rnatish, tarmoqqa ulash va telefon orqali kuzatishni sozlab berish xizmatini ko'rsataman."
    },
    {
        "id": 2,
        "name": "Doston",
        "job": "Wi-Fi router sozlash",
        "category": "Xavfsizlik va tarmoqlar",
        "region": "Toshkent shahri",
        "rating": 4.9,
        "reviews_count": 24,
        "phone": "+998998880802",
        "price": "Kelishilgan holda",
        "is_real": True,
        "description": "Wi-Fi routerlar va internet tarmoqlari bo'yicha mutaxassis. Routerni to'g'ri o'rnatish, Wi-Fi zonasini kengaytirish va internet uzilishlarini bartaraf etaman."
    },
    {
        "id": 3,
        "name": "Nizom",
        "job": "Konditsioner o'rnatish va sozlash",
        "category": "Iqlim texnikasi",
        "region": "Toshkent shahri",
        "rating": 4.8,
        "reviews_count": 19,
        "phone": "+998945040999",
        "price": "Kelishilgan holda",
        "is_real": True,
        "description": "Konditsionerlarni professional darajada o'rnatish (montaj), tozalash, freon quyish va texnik xizmat ko'rsatish ishlarini tez va kafolatli bajaramiz."
    },
    {
        "id": 4,
        "name": "Dostonbek",
        "job": "Kamera o'rnatish",
        "category": "Xavfsizlik va tarmoqlar",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 40,
        "phone": "+998909123161",
        "price": "Kelishilgan holda",
        "is_real": True,
        "description": "Videokuzatuv va xavfsizlik tizimlarini o'rnatish bo'yicha tajribali usta. Istalgan turdagi kameralarni tez va sifatli o'rnatib beraman."
    },
    {
        "id": 5,
        "name": "Aleksandr",
        "job": "Kir yuvish mashinasi ta'miri",
        "category": "Maishiy texnika",
        "region": "Toshkent shahri",
        "rating": 4.9,
        "reviews_count": 27,
        "phone": "+998903539108",
        "price": "Kelishilgan holda",
        "is_real": True,
        "description": "Barcha turdagi kir yuvish mashinalarini uyingizga kelib malakali ta'mirlash. Diagnostika va ehtiyot qismlarini almashtirish kafolati bilan."
    },
    {
        "id": 6,
        "name": "Ismoilov Baxodir (OYNACHI)",
        "job": "Telefon ekran va akkumulyator almashtirish",
        "category": "Telefon va Gadjetlar",
        "region": "Toshkent shahri",
        "rating": 5.0,
        "reviews_count": 64,
        "phone": "+998991405555",
        "price": "Kelishilgan holda",
        "is_real": True,
        "description": "OYNACHI servis markazi. iPhone, Samsung, Huawei, Xiaomi va boshqa barcha turdagi smartfonlarga ekran, shisha va akkumulyator almashtirish (180 kun kafolat). Batareya foizi 100% ko'rsatiladi. Ish vaqti: 10:00 dan 20:00 gacha, dam olish kunisiz."
    }
]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request, "regions": REGIONS_DB, "categories": CATEGORIES_DB})

@app.get("/api/technicians")
async def get_technicians(job: str = "", region: str = "", category: str = ""):
    result = TECHNICIANS_DB
    if category:
        result = [t for t in result if t.get("category") == category]
    if job:
        result = [t for t in result if job.lower() in t["job"].lower()]
    if region and region != "Barcha hududlar":
        result = [t for t in result if region.lower() in t["region"].lower()]
    return result

@app.get("/technician/{tech_id}")
async def technician_detail(request: Request, tech_id: int):
    tech = next((t for t in TECHNICIANS_DB if t["id"] == tech_id), None)
    return templates.TemplateResponse(request, "detail.html", {"request": request, "tech": tech})
