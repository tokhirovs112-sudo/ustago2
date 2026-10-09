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
    "Toshkent shahri", "Toshkent viloyati", "Farg'ona viloyati", "Andijon viloyati", 
    "Namangan viloyati", "Samarqand viloyati", "Buxoro viloyati", "Qashqadaryo viloyati", 
    "Surxondaryo viloyati", "Jizzax viloyati", "Sirdaryo viloyati", "Navoiy viloyati", 
    "Xorazm viloyati", "Qoraqalpog'iston Respublikasi"
]

CATEGORIES_DB = {
    "Telefon va Gadjetlar": {"services": ["Telefon ekranini almashtirish", "Akkumulyator almashtirish", "Smartfon ta'miri"]},
    "Xavfsizlik va tarmoqlar": {"services": ["Kamera o'rnatish", "Wi-Fi router sozlash"]},
    "Iqlim texnikasi": {"services": ["Konditsioner o'rnatish va sozlash"]},
    "Maishiy texnika": {"services": ["Kir yuvish mashinasi ta'miri"]}
}

TECHNICIANS_DB = [
    {
        "id": 1, "name": "Nikita", "job": "Kamera o'rnatish", "category": "Xavfsizlik va tarmoqlar", 
        "region": "Toshkent shahri", "rating": 5.0, "reviews_count": 31, "phone": "+998996420670", 
        "price": "Kelishilgan holda", "is_real": True, 
        "description": "Malakali mutaxassis. Xonadonlar, office va obyektlarga zamonaviy videokuzatuv kameralarini sifatli o'rnatish."
    },
    {
        "id": 2, "name": "Doston", "job": "Wi-Fi router sozlash", "category": "Xavfsizlik va tarmoqlar", 
        "region": "Toshkent shahri", "rating": 4.9, "reviews_count": 24, "phone": "+998998880802", 
        "price": "Kelishilgan holda", "is_real": True, 
        "description": "Wi-Fi routerlar va internet tarmoqlari bo'yicha mutaxassis. Routerni to'g'ri o'rnatish va kengaytirish."
    },
    {
        "id": 3, "name": "Nizom", "job": "Konditsioner o'rnatish va sozlash", "category": "Iqlim texnikasi", 
        "region": "Toshkent shahri", "rating": 4.8, "reviews_count": 19, "phone": "+998945040999", 
        "price": "Kelishilgan holda", "is_real": True, 
        "description": "Konditsionerlarni professional darajada o'rnatish (montaj), tozalash, freon quyish."
    },
    {
        "id": 4, "name": "Dostonbek", "job": "Kamera o'rnatish", "category": "Xavfsizlik va tarmoqlar", 
        "region": "Toshkent shahri", "rating": 5.0, "reviews_count": 40, "phone": "+998909123161", 
        "price": "Kelishilgan holda", "is_real": True, 
        "description": "Videokuzatuv va xavfsizlik tizimlarini o'rnatish bo'yicha tajribali usta."
    },
    {
        "id": 5, "name": "Aleksandr", "job": "Kir yuvish mashinasi ta'miri", "category": "Maishiy texnika", 
        "region": "Toshkent shahri", "rating": 4.9, "reviews_count": 27, "phone": "+998903539108", 
        "price": "Kelishilgan holda", "is_real": True, 
        "description": "Barcha turdagi kir yuvish mashinalarini uyingizga kelib malakali ta'mirlash."
    },
    {
        "id": 6, "name": "Ismoilov Baxodir (OYNACHI)", "job": "Telefon ekran va akkumulyator almashtirish", 
        "category": "Telefon va Gadjetlar", "region": "Toshkent shahri", "rating": 5.0, "reviews_count": 64, 
        "phone": "+998991405555", "price": "Kelishilgan holda", "is_real": True, 
        "description": "OYNACHI servis markazi. 180 kun kafolat. iPhone va Samsung akkumulyator almashtirganda foiz 100% ko'rsatiladi."
    }
]

# Quick Tips (Tezkor maslahatlar) Bazasi
QUICK_TIPS_DB = [
    {
        "id": 1,
        "title": "Telefoningiz tez qizib ketyaptimi?",
        "category": "Gadjetlar",
        "icon": "fa-mobile-screen-button",
        "tip": "Og'ir o'yinlar yoki ilovalardan so'ng telefoningiz qizisa, uni g'ilofidan (chexolidan) chiqarib turing va quyosh nuri tushmaydigan salqin joyga qo'ying."
    },
    {
        "id": 2,
        "title": "Konditsioner yomon sovutyaptimi?",
        "category": "Iqlim",
        "icon": "fa-snowflake",
        "tip": "Ko'pincha sabab oddiy: ichki blok havo filtrlarida chang to'lib qolgan bo'ladi. Ularni har oyda bir marta iliq suvda yuvib quritib taqib qo'ying."
    },
    {
        "id": 3,
        "title": "Wi-Fi internet sekin ishlayotgan bo'lsa",
        "category": "Tarmoqlar",
        "icon": "fa-wifi",
        "tip": "Routerni har hafta 10 soniyaga tokdan o'chirib yoqing (pereczerka). Bu uning xotirasini tozalab, tezligini tiklaydi."
    },
    {
        "id": 4,
        "title": "Kir yuvish mashinasidan yoqimsiz hid kelsa",
        "category": "Maishiy texnika",
        "icon": "fa-shirt",
        "tip": "Har oyda bir marta mashinani kirsiz, 90 gradus haroratda ichiga ozgina limon kislotasi (limonnaya kislota) solib bo'sh yuvdirib yuboring."
    },
    {
        "id": 5,
        "title": "Smartfon batareyasini 100% gacha zaryadlamang",
        "category": "Gadjetlar",
        "icon": "fa-battery-half",
        "tip": "Akkumulyator uzoq xizmat qilishi uchun uni doim 80-85% gacha quvvatlab, 20% dan pastga tushirmaslikka harakat qiling."
    },
    {
        "id": 6,
        "title": "Televizor yoki routerni tokdan himoya qilish",
        "category": "Elektr",
        "icon": "fa-bolt",
        "tip": "Tok kuchlanishi keskin o'zgarganda qimmatbaho texnikalaringiz yonib ketmasligi uchun albatta sifatli stabilizator yoki rezinaviy tarmoq filtridan foydalaning."
    }
]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request, "regions": REGIONS_DB, "categories": CATEGORIES_DB})

@app.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse(request, "about.html", {"request": request})

@app.get("/blog")
async def blog_page(request: Request):
    return templates.TemplateResponse(request, "blog.html", {"request": request, "tips": QUICK_TIPS_DB})

@app.get("/blog/{article_id}")
async def article_detail(request: Request, article_id: int):
    # Agar eski article_id bo'yicha kirishsa, Quick Tip ma'lumotini ochib beramiz
    article = next((a for a in QUICK_TIPS_DB if a["id"] == article_id), QUICK_TIPS_DB[0])
    return templates.TemplateResponse(request, "article.html", {"request": request, "article": article})

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
