from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="UstaGo API")

templates = Jinja2Templates(directory="templates")

SERVICES_DB = {
    "Maishiy texnika": {
        "Kir yuvish mashinasi ta'miri va tozalash": [
            ("Nodir Abdullayev", 4.9, 210, "1.0 km"),
            ("Rustam Jo'rayev", 4.7, 130, "3.2 km"),
            ("Otabek KirMashina", 4.8, 95, "2.1 km")
        ],
        "Muzlatgich va sovutish tizimlari": [
            ("Anvar Xolodilshik", 4.9, 190, "1.2 km"),
            ("Zokir Master", 4.6, 80, "4.0 km")
        ],
        "Gaz plitasi va pech (duhovka) ta'miri": [
            ("Davron Valiyev", 4.8, 88, "2.1 km"),
            ("Shoxrux Qosmonov", 4.6, 54, "4.3 km")
        ],
        "Konditsioner tozalash va freon quyish": [
            ("Bekzod KOND", 4.7, 145, "2.7 km"),
            ("Sardor Klimat", 4.9, 230, "1.5 km")
        ],
        "Mikrotolqinli pech (Mikrovolnovka)": [
            ("Murod Master", 4.8, 62, "3.0 km")
        ],
        "Boshqa maishiy muammo": []
    },
    "Elektronika va Gadjetlar": {
        "Smartfonlar va Mobil telefonlar": [
            ("Jasurbek Aliyev (iPhone master)", 4.9, 320, "1.2 km"),
            ("Sardor Qodirov (Android master)", 4.7, 185, "2.5 km"),
            ("Farrux Mobile", 4.8, 140, "0.9 km")
        ],
        "Planshetlar va iPad qurilmalari": [
            ("Bobur Usmonov", 4.8, 95, "3.1 km"),
            ("Aziz Masharipov", 4.9, 140, "1.1 km")
        ],
        "Noutbuk va Kompyuter texnikasi": [
            ("Aziz Rahimov", 4.9, 240, "0.8 km"),
            ("Otabek PC", 4.6, 60, "2.0 km")
        ],
        "Aqlli soatlar (Smartwatch / Apple Watch)": [
            ("Farrux Gadget", 4.8, 76, "2.0 km")
        ],
        "Boshqa elektronika muammosi": []
    },
    "Santexnika muammolari": {
        "Rakovina, krant va jo'mraklar ta'miri": [
            ("Jasur Santexnik", 4.9, 310, "0.5 km"),
            ("Ilhom Zokirov", 4.8, 175, "1.8 km")
        ],
        "Quvurlar va oqish (protechka) muammosi": [
            ("Bahrom Truba", 4.7, 115, "2.3 km"),
            ("Umid Santexnik", 4.9, 205, "1.1 km")
        ],
        "Hojatxona va vanna tizimlari": [
            ("Sherzod Usta", 4.8, 90, "3.5 km")
        ],
        "Kanalizatsiya va tıkanoqlikni ochish": [
            ("Anvar Chistka", 4.9, 280, "0.7 km")
        ],
        "Boshqa santexnika muammosi": []
    }
}

BRANDS = ["Apple", "Samsung", "Xiaomi", "LG", "Bosch", "Beko", "Artel", "Lenovo", "HP", "Boshqa brend"]

WORKER_REVIEWS_DB = {
    "Jasurbek Aliyev (iPhone master)": [
        {"client": "Murod", "comment": "Ekranini 20 daqiqada almashtirib berdi, super!", "rating": 5}
    ],
    "Jasur Santexnik": [
        {"client": "Laziz", "comment": "Quvurdagi oqishni tezda to'xtatdi, raxmat!", "rating": 5}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    all_workers = []
    for category in SERVICES_DB.values():
        for service, workers in category.items():
            for w in workers:
                if w[0] not in all_workers:
                    all_workers.append(w[0])

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "categories": SERVICES_DB,
            "brands": BRANDS,
            "workers": all_workers,
            "reviews_db": WORKER_REVIEWS_DB
        }
    )

@app.get("/get-services")
async def get_services(category: str):
    return list(SERVICES_DB.get(category, {}).keys())

@app.get("/get-technicians")
async def get_technicians(category: str, service: str, brand: str = ""):
    return SERVICES_DB.get(category, {}).get(service, [])

@app.post("/add-worker-review")
async def add_worker_review(
    worker_name: str = Form(...),
    client_name: str = Form(...),
    comment: str = Form(...),
    rating: int = Form(5)
):
    if worker_name not in WORKER_REVIEWS_DB:
        WORKER_REVIEWS_DB[worker_name] = []
        
    WORKER_REVIEWS_DB[worker_name].append({
        "client": client_name,
        "comment": comment,
        "rating": rating
    })
    return RedirectResponse(url="/", status_code=303)
