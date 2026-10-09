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
    "Konditsionerlar": {"services": ["Konditsioner o'rnatish va ta'mirlash"]},
    "Maishiy texnika": {"services": ["Kir yuvish mashinasi va muzlatgich ta'miri"]}
}

# Faqat OYNACHI va siz bergan yangi 2 ta usta qoldirildi, sharhlar 0 qilindi
TECHNICIANS_DB = [
    {
        "id": 1, "name": "Ismoilov Baxodir (OYNACHI)", "job": "Telefon ekran va akkumulyator almashtirish", 
        "category": "Telefon va Gadjetlar", "region": "Toshkent shahri", "rating": 5.0, "reviews_count": 0, 
        "phone": "+998991405555", "price": "Kelishilgan holda", "is_real": True, 
        "description": "OYNACHI servis markazi. 180 kun kafolat. iPhone, Samsung, Huawei, Xiaomi va boshqa modellar uchun ekran, shisha va akkumulyator almashtirish. Batareya foizi 100% ko'rsatiladi."
    },
    {
        "id": 2, "name": "Zafar", "job": "Konditsioner va muzlatgich ta'miri", "category": "Konditsionerlar", 
        "region": "Toshkent shahri", "rating": 5.0, "reviews_count": 0, 
        "phone": "+998935717774", "price": "Kelishilgan holda", "is_real": True, 
        "description": "Ustanofka, remont, demontaj, zapravka freon, kompressor almashtirish va profilaktika. Muzlatgich va marazilka ta'mirlash."
    },
    {
        "id": 3, "name": "Khalmuratov Dilmurod", "job": "Maishiy texnika va konditsioner ta'miri", "category": "Maishiy texnika", 
        "region": "Toshkent shahri", "rating": 5.0, "reviews_count": 0, 
        "phone": "+998957073773", "price": "Kelishilgan holda", "is_real": True, 
        "description": "Konditsionerlar, muzlatgichlar, kir yuvish mashinalari va boshqa maishiy texnikalarni professional diagnostika va kafolatli ta'mirlash."
    }
]

QUICK_TIPS_DB = [
    {
        "id": 1, "title": "Telefoningiz tez qizib ketyaptimi?", "category": "Gadjetlar", "icon": "fa-mobile-screen-button",
        "tip": "Og'ir o'yinlar yoki ilovalardan so'ng telefoningiz qizisa, uni g'ilofidan chiqarib turing va salqin joyga qo'ying."
    },
    {
        "id": 2, "title": "Konditsioner yomon sovutyaptimi?", "category": "Konditsionerlar", "icon": "fa-snowflake",
        "tip": "Ichki blok havo filtrlarini har oyda bir marta iliq suvda yuvib turing."
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
