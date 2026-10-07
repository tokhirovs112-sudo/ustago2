from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="UstaGo API")

templates = Jinja2Templates(directory="templates")

# Har bir usta formati: (Ism, Baho, SharhlarSoni, Masofa, Telefon)
SERVICES_DB = {
    "Maishiy texnika": {
        "Kir yuvish mashinasi ta'miri va tozalash": [
            ("Nodir Abdullayev", 4.9, 210, "1.0 km", "+998901112233"),
            ("Rustam Jo'rayev", 4.7, 130, "3.2 km", "+998912223344"),
            ("Otabek KirMashina", 4.8, 95, "2.1 km", "+998933334455"),
            ("Sardor Umarov", 4.9, 180, "1.5 km", "+998944445566"),
            ("Jahongir Vahobov", 4.6, 75, "4.2 km", "+998975556677"),
            ("Ilhomiddin Usta", 4.8, 110, "2.8 km", "+998996667788"),
            ("Botirxon Axmedov", 4.7, 64, "3.9 km", "+998907778899")
        ],
        "Muzlatgich va sovutish tizimlari": [
            ("Anvar Xolodilshik", 4.9, 190, "1.2 km", "+998901234501"),
            ("Zokir Master", 4.6, 80, "4.0 km", "+998912345602"),
            ("Murod Xolod", 4.8, 145, "2.3 km", "+998933456703"),
            ("Shohrux Sovutgich", 4.7, 92, "3.1 km", "+998944567804"),
            ("Dilshod Qodirov", 4.9, 210, "0.9 km", "+998975678905"),
            ("Alisher Tursunov", 4.5, 55, "5.0 km", "+998996789006")
        ],
        "Gaz plitasi va pech (duhovka) ta'miri": [
            ("Davron Valiyev", 4.8, 88, "2.1 km", "+998902345611"),
            ("Shoxrux Qosmonov", 4.6, 54, "4.3 km", "+998913456712"),
            ("Olimjon Gaz", 4.9, 160, "1.8 km", "+998934567813"),
            ("Hikmatillo Usta", 4.7, 72, "3.0 km", "+998945678914"),
            ("Bobur Isoqov", 4.8, 105, "2.5 km", "+998976789015"),
            ("Sanjar Narziyev", 4.6, 48, "4.1 km", "+998997890116")
        ],
        "Konditsioner tozalash va freon quyish": [
            ("Bekzod KOND", 4.7, 145, "2.7 km", "+998903456721"),
            ("Sardor Klimat", 4.9, 230, "1.5 km", "+998914567822"),
            ("Islomjon Klimat", 4.8, 120, "2.0 km", "+998935678923"),
            ("Jasur Freon", 4.6, 85, "3.8 km", "+998946789024"),
            ("Farhod Mamatov", 4.9, 195, "1.1 km", "+998977890125"),
            ("Eldor Zokirov", 4.7, 67, "4.5 km", "+998998901226")
        ],
        "Mikrotolqinli pech (Mikrovolnovka)": [
            ("Murod Master", 4.8, 62, "3.0 km", "+998904567831"),
            ("Akmal Raximov", 4.9, 115, "1.4 km", "+998915678932"),
            ("Umidjon Pech", 4.7, 78, "2.9 km", "+998936789033"),
            ("Jamshid Bekov", 4.6, 40, "4.8 km", "+998947890134"),
            ("Xurshid Aliyev", 4.8, 93, "2.2 km", "+998978901235"),
            ("Ulug'bek Usta", 4.5, 33, "5.2 km", "+998999012336")
        ],
        "Boshqa maishiy muammo": []
    },
    "Elektronika va Gadjetlar": {
        "Smartfonlar va Mobil telefonlar": [
            ("Jasurbek Aliyev (iPhone master)", 4.9, 320, "1.2 km", "+998905551122"),
            ("Sardor Qodirov (Android master)", 4.7, 185, "2.5 km", "+998916662233"),
            ("Farrux Mobile", 4.8, 140, "0.9 km", "+998937773344"),
            ("Jamshid Fix", 4.9, 250, "1.8 km", "+998948884455"),
            ("Nodirbek Apple", 4.8, 165, "2.0 km", "+998979995566"),
            ("Bobur Samsung", 4.6, 98, "3.4 km", "+998990006677"),
            ("Sirojiddin Gadget", 4.7, 112, "2.9 km", "+998901117788")
        ],
        "Planshetlar va iPad qurilmalari": [
            ("Bobur Usmonov", 4.8, 95, "3.1 km", "+998905678941"),
            ("Aziz Masharipov", 4.9, 140, "1.1 km", "+998916789042"),
            ("Husniddin Tab", 4.7, 68, "2.8 km", "+998937890143"),
            ("Dilshod iPad", 4.9, 180, "1.6 km", "+998948901244"),
            ("Kamron Raxmatov", 4.6, 52, "4.0 km", "+998979012345"),
            ("Javohir Master", 4.8, 87, "2.3 km", "+998990123446")
        ],
        "Noutbuk va Kompyuter texnikasi": [
            ("Aziz Rahimov", 4.9, 240, "0.8 km", "+998906789051"),
            ("Otabek PC", 4.6, 60, "2.0 km", "+998917890152"),
            ("Sanjar IT", 4.8, 175, "1.9 km", "+998938901253"),
            ("Doston Comp", 4.7, 110, "3.3 km", "+998949012354"),
            ("Sherzod Laptop", 4.9, 205, "1.3 km", "+998970123455"),
            ("Ravshan Windows", 4.5, 45, "4.7 km", "+998991234556")
        ],
        "Aqlli soatlar (Smartwatch / Apple Watch)": [
            ("Farrux Gadget", 4.8, 76, "2.0 km", "+998907890161"),
            ("Asilbek Watch", 4.9, 130, "1.2 km", "+998918901262"),
            ("Diyorbek AppleWatch", 4.7, 85, "2.6 km", "+998939012363"),
            ("Shoxrux Smart", 4.6, 42, "3.9 km", "+998940123464"),
            ("Mansur Isoqov", 4.8, 94, "1.7 km", "+998971234565"),
            ("Xursandbek Usta", 4.5, 30, "5.1 km", "+998992345666")
        ],
        "Boshqa elektronika muammosi": []
    },
    "Santexnika muammolari": {
        "Rakovina, krant va jo'mraklar ta'miri": [
            ("Jasur Santexnik", 4.9, 310, "0.5 km", "+998908901271"),
            ("Ilhom Zokirov", 4.8, 175, "1.8 km", "+998919012372"),
            ("Sanjar Krant", 4.7, 90, "3.2 km", "+998930123473"),
            ("Murod Vanna", 4.9, 210, "1.0 km", "+998941234574"),
            ("Abdurohman Usta", 4.6, 65, "4.1 km", "+998972345675"),
            ("Zuhiddin Santex", 4.8, 135, "2.4 km", "+998993456776"),
            ("Sherali Karimov", 4.7, 82, "3.6 km", "+998904567877")
        ],
        "Quvurlar va oqish (protechka) muammosi": [
            ("Bahrom Truba", 4.7, 115, "2.3 km", "+998909012381"),
            ("Umid Santexnik", 4.9, 205, "1.1 km", "+998910123482"),
            ("Nodirbek Aquafix", 4.8, 140, "1.9 km", "+998931234583"),
            ("Alisher Quvur", 4.6, 70, "3.7 km", "+998942345684"),
            ("Tohirjon Santex", 4.9, 180, "0.8 km", "+998973456785"),
            ("Shavkat Truboprof", 4.7, 95, "2.9 km", "+998994567886")
        ],
        "Hojatxona va vanna tizimlari": [
            ("Sherzod Usta", 4.8, 90, "3.5 km", "+998901234591"),
            ("Farhod Vanna", 4.9, 160, "1.3 km", "+998912345692"),
            ("Jamshid Unitaz", 4.7, 85, "2.7 km", "+998933456793"),
            ("Botir Santexnik", 4.6, 50, "4.2 km", "+998944567894"),
            ("Komiljon Umarov", 4.8, 110, "2.1 km", "+998975678995"),
            ("Nurmurod Master", 4.7, 68, "3.8 km", "+998996789096")
        ],
        "Kanalizatsiya va tıkanoqlikni ochish": [
            ("Anvar Chistka", 4.9, 280, "0.7 km", "+998902345601"),
            ("Akmal Kanalizatsiya", 4.8, 150, "1.6 km", "+998913456702"),
            ("Dravshon Zassor", 4.7, 92, "3.1 km", "+998934567803"),
            ("Sardor Ochish", 4.9, 210, "1.2 km", "+998945678904"),
            ("Oktam Santex", 4.6, 60, "4.4 km", "+998976789005"),
            ("Sobirjon Chist", 4.8, 105, "2.3 km", "+998997890106")
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
        {"client": "Kamron", "comment": "iPhone 13 battery health 100% qilib yangilap berdi.", "rating": 5}
    ],
    "Jasur Santexnik": [
        {"client": "Laziz", "comment": "Quvurdagi oqishni tezda to'xtatdi, raxmat!", "rating": 5},
        {"client": "Otabek", "comment": "Grohe smesitelini o'rnatib berdi.", "rating": 5}
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
        return {
            "workers": [
                {
                    "name": w[0],
                    "rating": w[1],
                    "reviews_count": w[2],
                    "distance": w[3],
                    "phone": w[4]
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
