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

# Kengaytirilgan Blog va Qo'llanmalar Bazasi (5 ta maqola)
ARTICLES_DB = [
    {
        "id": 1,
        "title": "Smartfon akkumulyatorini to'g'ri quvvatlash va uning muddatini uzaytirish sirlari",
        "category": "Gadjetlar",
        "date": "2026-10-08",
        "read_time": "5 daqiqa",
        "content": "Bugungi kunda smartfonlar hayotimizning ajralmas qismiga aylandi. Ularning eng nozik joylaridan biri bu — akkumulyator (batareya). Batareya quvvati tez tugashi ko'pchilikning muammosi. Uni to'g'ri quvvatlash uchun quyidagi qoidalarga amal qilish lozim: Telefoningizni doimiy ravishda 0% gacha o'chirib qo'ymang, optimal quvvat oralig'i 20% dan 80% gacha hisoblanadi. Tunda zaryadga qo'yib uxlash batareya resursini qisqartiradi. Shuningdek, faqat original adapter va kabellardan foydalanish telefoningizni ortiqcha qizishdan saqlaydi."
    },
    {
        "id": 2,
        "title": "Konditsionerga o'z vaqtida texnik xizmat ko'rsatish nima uchun muhim?",
        "category": "Iqlim texnikasi",
        "date": "2026-10-05",
        "read_time": "4 daqiqa",
        "content": "Konditsionerlar yozda salqinlik, qishda iliqlik baxsh etadi. Ammo ularga o'z vaqtida texnik xizmat ko'rsatilmasa, ichki filtrlar chang bilan to'lib, havo aylanishi buziladi va freon (sovutish gazi) kamayib ketadi. Natijada kompressor ortiqcha yuklama bilan ishlab, ishdan chiqishi mumkin. Har mavsum boshlanishidan oldin ichki filtrlarni tozalash va malakali ustaga freon bosimini tekshirtirish tavsiya etiladi."
    },
    {
        "id": 3,
        "title": "Uyda Wi-Fi internet tezligini oshirish va routerni to'g'ri joylashtirish",
        "category": "Tarmoqlar",
        "date": "2026-09-28",
        "read_time": "6 daqiqa",
        "content": "Internet tezligi pastligidan shikoyat qilyapsizmi? Ko'pincha buning sababi routerning uyning chekka xonasida yoki temir-beton devorlar ortida turganidadir. Routerni uyning markaziy qismiga, balandroq joyga o'rnatish signallarning bir tekis tarqalishini ta'minlaydi. Shuningdek, mikroto'lqinli pechlar va ko'zgu oynalar Wi-Fi signalini to'sishi mumkinligini unutmang."
    },
    {
        "id": 4,
        "title": "Kir yuvish mashinasi titrashi va shovqin qilishining asosiy sabablari",
        "category": "Maishiy texnika",
        "date": "2026-09-20",
        "read_time": "5 daqiqa",
        "content": "Kir yuvish mashinasi siqish rejimida kuchli sakray boshlasa yoki g'ichirlasa, bu e'tiborsiz qoldirib bo'lmaydigan signaldir. Birinchi navbatda barabandagi kirlar teng taqsimlanganiga va mashinaning oyoqlari tekis turganiga e'tibor bering. Shuningdek, transport boltlarining yechilgani va amotizatorlarning holati ham muhim rol o'ynaydi."
    },
    {
        "id": 5,
        "title": "Videokuzatuv kameralarini o'rnatishda nimalarga e'tibor berish kerak?",
        "category": "Xavfsizlik",
        "date": "2026-09-15",
        "read_time": "7 daqiqa",
        "content": "Uy yoki ofis xavfsizligini ta'minlash uchun videokuzatuv kameralari eng yaxshi yechimdir. Kamerani o'rnatishda uning ko'rish burchagi kengligiga, qorong'ida ham yaxshi ko'rsatishiga (IK-yoritish) hamda internet tarmoqlariga barqaror ulanishiga alohida e'tibor qaratish lozim."
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
    return templates.TemplateResponse(request, "blog.html", {"request": request, "articles": ARTICLES_DB})

@app.get("/blog/{article_id}")
async def article_detail(request: Request, article_id: int):
    article = next((a for a in ARTICLES_DB if a["id"] == article_id), None)
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
