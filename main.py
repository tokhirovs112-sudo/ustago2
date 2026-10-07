from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="UstaGo API")

templates = Jinja2Templates(directory="templates")

SERVICES_DB = {
    "Maishiy texnika": {
        "Kir yuvish mashinasi ta'miri va tozalash": [
            ("Nodir Abdullayev", 4.9, 210, "1.0 km"),
            ("Rustam Jo'rayev", 4.7, 130, "3.2 km"),
            ("Otabek KirMashina", 4.8, 95, "2.1 km"),
            ("Sardor Umarov", 4.9, 180, "1.5 km"),
            ("Jahongir Vahobov", 4.6, 75, "4.2 km"),
            ("Ilhomiddin Usta", 4.8, 110, "2.8 km"),
            ("Botirxon Axmedov", 4.7, 64, "3.9 km")
        ],
        "Muzlatgich va sovutish tizimlari": [
            ("Anvar Xolodilshik", 4.9, 190, "1.2 km"),
            ("Zokir Master", 4.6, 80, "4.0 km"),
            ("Murod Xolod", 4.8, 145, "2.3 km"),
            ("Shohrux Sovutgich", 4.7, 92, "3.1 km"),
            ("Dilshod Qodirov", 4.9, 210, "0.9 km"),
            ("Alisher Tursunov", 4.5, 55, "5.0 km")
        ],
        "Gaz plitasi va pech (duhovka) ta'miri": [
            ("Davron Valiyev", 4.8, 88, "2.1 km"),
            ("Shoxrux Qosmonov", 4.6, 54, "4.3 km"),
            ("Olimjon Gaz", 4.9, 160, "1.8 km"),
            ("Hikmatillo Usta", 4.7, 72, "3.0 km"),
            ("Bobur Isoqov", 4.8, 105, "2.5 km"),
            ("Sanjar Narziyev", 4.6, 48, "4.1 km")
        ],
        "Konditsioner tozalash va freon quyish": [
            ("Bekzod KOND", 4.7, 145, "2.7 km"),
            ("Sardor Klimat", 4.9, 230, "1.5 km"),
            ("Islomjon Klimat", 4.8, 120, "2.0 km"),
            ("Jasur Freon", 4.6, 85, "3.8 km"),
            ("Farhod Mamatov", 4.9, 195, "1.1 km"),
            ("Eldor Zokirov", 4.7, 67, "4.5 km")
        ],
        "Mikrotolqinli pech (Mikrovolnovka)": [
            ("Murod Master", 4.8, 62, "3.0 km"),
            ("Akmal Raximov", 4.9, 115, "1.4 km"),
            ("Umidjon Pech", 4.7, 78, "2.9 km"),
            ("Jamshid Bekov", 4.6, 40, "4.8 km"),
            ("Xurshid Aliyev", 4.8, 93, "2.2 km"),
            ("Ulug'bek Usta", 4.5, 33, "5.2 km")
        ],
        "Boshqa maishiy muammo": []
    },
    "Elektronika va Gadjetlar": {
        "Smartfonlar va Mobil telefonlar": [
            ("Jasurbek Aliyev (iPhone master)", 4.9, 320, "1.2 km"),
            ("Sardor Qodirov (Android master)", 4.7, 185, "2.5 km"),
            ("Farrux Mobile", 4.8, 140, "0.9 km"),
            ("Jamshid Fix", 4.9, 250, "1.8 km"),
            ("Nodirbek Apple", 4.8, 165, "2.0 km"),
            ("Bobur Samsung", 4.6, 98, "3.4 km"),
            ("Sirojiddin Gadget", 4.7, 112, "2.9 km")
        ],
        "Planshetlar va iPad qurilmalari": [
            ("Bobur Usmonov", 4.8, 95, "3.1 km"),
            ("Aziz Masharipov", 4.9, 140, "1.1 km"),
            ("Husniddin Tab", 4.7, 68, "2.8 km"),
            ("Dilshod iPad", 4.9, 180, "1.6 km"),
            ("Kamron Raxmatov", 4.6, 52, "4.0 km"),
            ("Javohir Master", 4.8, 87, "2.3 km")
        ],
        "Noutbuk va Kompyuter texnikasi": [
            ("Aziz Rahimov", 4.9, 240, "0.8 km"),
            ("Otabek PC", 4.6, 60, "2.0 km"),
            ("Sanjar IT", 4.8, 175, "1.9 km"),
            ("Doston Comp", 4.7, 110, "3.3 km"),
            ("Sherzod Laptop", 4.9, 205, "1.3 km"),
            ("Ravshan Windows", 4.5, 45, "4.7 km")
        ],
        "Aqlli soatlar (Smartwatch / Apple Watch)": [
            ("Farrux Gadget", 4.8, 76, "2.0 km"),
            ("Asilbek Watch", 4.9, 130, "1.2 km"),
            ("Diyorbek AppleWatch", 4.7, 85, "2.6 km"),
            ("Shoxrux Smart", 4.6, 42, "3.9 km"),
            ("Mansur Isoqov", 4.8, 94, "1.7 km"),
            ("Xursandbek Usta", 4.5, 30, "5.1 km")
        ],
        "Boshqa elektronika muammosi": []
    },
    "Santexnika muammolari": {
        "Rakovina, krant va jo'mraklar ta'miri": [
            ("Jasur Santexnik", 4.9, 310, "0.5 km"),
            ("Ilhom Zokirov", 4.8, 175, "1.8 km"),
            ("Sanjar Krant", 4.7, 90, "3.2 km"),
            ("Murod Vanna", 4.9, 210, "1.0 km"),
            ("Abdurohman Usta", 4.6, 65, "4.1 km"),
            ("Zuhiddin Santex", 4.8, 135, "2.4 km"),
            ("Sherali Karimov", 4.7, 82, "3.6 km")
        ],
        "Quvurlar va oqish (protechka) muammosi": [
            ("Bahrom Truba", 4.7, 115, "2.3 km"),
            ("Umid Santexnik", 4.9, 205, "1.1 km"),
            ("Nodirbek Aquafix", 4.8, 140, "1.9 km"),
            ("Alisher Quvur", 4.6, 70, "3.7 km"),
            ("Tohirjon Santex", 4.9, 180, "0.8 km"),
            ("Shavkat Truboprof", 4.7, 95, "2.9 km")
        ],
        "Hojatxona va vanna tizimlari": [
            ("Sherzod Usta", 4.8, 90, "3.5 km"),
            ("Farhod Vanna", 4.9, 160, "1.3 km"),
            ("Jamshid Unitaz", 4.7, 85, "2.7 km"),
            ("Botir Santexnik", 4.6, 50, "4.2 km"),
            ("Komiljon Umarov", 4.8, 110, "2.1 km"),
            ("Nurmurod Master", 4.7, 68, "3.8 km")
        ],
        "Kanalizatsiya va tıkanoqlikni ochish": [
            ("Anvar Chistka", 4.9, 280, "0.7 km"),
            ("Akmal Kanalizatsiya", 4.8, 150, "1.6 km"),
            ("Dravshon Zassor", 4.7, 92, "3.1 km"),
            ("Sardor Ochish", 4.9, 210, "1.2 km"),
            ("Oktam Santex", 4.6, 60, "4.4 km"),
            ("Sobirjon Chist", 4.8, 105, "2.3 km")
        ],
        "Boshqa santexnika muammosi": []
    }
}

BRANDS = ["Apple", "Samsung", "Xiaomi", "LG", "Bosch", "Beko", "Artel", "Lenovo", "HP", "Boshqa brend"]

WORKER_REVIEWS_DB = {
    "Nodir Abdullayev": [
        {"client": "Sardor", "comment": "Kir yuvish mashinasini gigiyenik tozalab berdi, hamma hidlar yo'qoldi.", "rating": 5},
        {"client": "Madina", "comment": "Baraban shovqin qilayotgan edi, podshipnikni almashtirib berdi. Rahmat!", "rating": 5}
    ],
    "Rustam Jo'rayev": [
        {"client": "Bekzod", "comment": "Toshkent markaziga yetib kelishi tez bo'ldi. Sifatli ta'mir.", "rating": 5},
        {"client": "Nilufar", "comment": "Suv to'kib yuborayotgan edi, nasosini almashtirib berdi.", "rating": 4}
    ],
    "Jasurbek Aliyev (iPhone master)": [
        {"client": "Murod", "comment": "Ekranini 20 daqiqada almashtirib berdi, super!", "rating": 5},
        {"client": "Kamron", "comment": "iPhone 13 battery health 100% qilib yangilap berdi. TrueTone saqlanib qoldi.", "rating": 5}
    ],
    "Jasur Santexnik": [
        {"client": "Laziz", "comment": "Quvurdagi oqishni tezda to'xtatdi, raxmat!", "rating": 5},
        {"client": "Otabek", "comment": "Grohe smesitelini o'rnatib berdi. Ishiga a'lo baho!", "rating": 5}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "categories": SERVICES_DB,
            "brands": BRANDS,
            "reviews_db": WORKER_REVIEWS_DB
        }
    )

@app.get("/api/services")
async def get_services(category: str):
    if category in SERVICES_DB:
        return {"services": list(SERVICES_DB[category].keys())}
    return {"services": []}

@app.get("/api/technicians")
async def get_technicians(category: str, service: str):
    if category in SERVICES_DB and service in SERVICES_DB[category]:
        workers = SERVICES_DB[category][service]
        # Return formatted structure for frontend script
        return {
            "workers": [
                {
                    "name": w[0],
                    "rating": w[1],
                    "reviews_count": w[2],
                    "distance": w[3]
                }
                for w in workers
            ]
        }
    return {"workers": []}

@app.post("/add-worker-review")
async def add_review(
    worker_name: str = Form(...),
    client_name: str = Form(...),
    rating: int = Form(...),
    comment: str = Form(...)
):
    if worker_name not in WORKER_REVIEWS_DB:
        WORKER_REVIEWS_DB[worker_name] = []
    
    WORKER_REVIEWS_DB[worker_name].insert(0, {
        "client": client_name,
        "rating": rating,
        "comment": comment
    })
    return RedirectResponse(url="/", status_code=303)
