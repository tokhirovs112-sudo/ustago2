from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="UstaGo API")

templates = Jinja2Templates(directory="templates")

# Toshkent va boshqa shahar tumanlari ro'yxati
DISTRICTS = [
    "Barchasi (Hudud bo'yicha)",
    "Chilonzor",
    "Yunusobod",
    "Mirzo Ulug'bek",
    "Yashnobod",
    "Mirobod",
    "Yakkasaroy",
    "Shayxontohur",
    "Olmazor",
    "Uchtepa",
    "Sergeli",
    "Yangihayot"
]

SERVICES_DB = {
    "Maishiy texnika": {
        "Kir yuvish mashinasi ta'miri va tozalash": [
            ("Nodir Abdullayev", 4.9, 210, "1.0 km", "+998901112233", True, "Chilonzor"),
            ("Rustam Jo'rayev", 4.7, 130, "3.2 km", "+998912223344", True, "Yunusobod"),
            ("Otabek KirMashina", 4.8, 95, "2.1 km", "+998933334455", False, "Mirobod"),
            ("Sardor Umarov", 4.9, 180, "1.5 km", "+998944445566", True, "Chilonzor"),
            ("Jahongir Vahobov", 4.6, 75, "4.2 km", "+998975556677", False, "Uchtepa"),
            ("Ilhomiddin Usta", 4.8, 110, "2.8 km", "+998996667788", True, "Mirzo Ulug'bek"),
            ("Botirxon Axmedov", 4.7, 64, "3.9 km", "+998907778899", False, "Yashnobod")
        ],
        "Muzlatgich va sovutish tizimlari": [
            ("Anvar Xolodilshik", 4.9, 190, "1.2 km", "+998901234501", True, "Chilonzor"),
            ("Zokir Master", 4.6, 80, "4.0 km", "+998912345602", False, "Olmazor"),
            ("Murod Xolod", 4.8, 145, "2.3 km", "+998933456703", True, "Yakkasaroy"),
            ("Shohrux Sovutgich", 4.7, 92, "3.1 km", "+998944567804", False, "Shayxontohur"),
            ("Dilshod Qodirov", 4.9, 210, "0.9 km", "+998975678905", True, "Mirobod"),
            ("Alisher Tursunov", 4.5, 55, "5.0 km", "+998996789006", False, "Sergeli")
        ],
        "Gaz plitasi va pech (duhovka) ta'miri": [
            ("Davron Valiyev", 4.8, 88, "2.1 km", "+998902345611", True, "Yunusobod"),
            ("Shoxrux Qosmonov", 4.6, 54, "4.3 km", "+998913456712", False, "Uchtepa"),
            ("Olimjon Gaz", 4.9, 160, "1.8 km", "+998934567813", True, "Chilonzor"),
            ("Hikmatillo Usta", 4.7, 72, "3.0 km", "+998945678914", False, "Olmazor"),
            ("Bobur Isoqov", 4.8, 105, "2.5 km", "+998976789015", True, "Mirzo Ulug'bek"),
            ("Sanjar Narziyev", 4.6, 48, "4.1 km", "+998997890116", False, "Yashnobod")
        ],
        "Konditsioner tozalash va freon quyish": [
            ("Bekzod KOND", 4.7, 145, "2.7 km", "+998903456721", True, "Mirobod"),
            ("Sardor Klimat", 4.9, 230, "1.5 km", "+998914567822", True, "Chilonzor"),
            ("Islomjon Klimat", 4.8, 120, "2.0 km", "+998935678923", True, "Yunusobod"),
            ("Jasur Freon", 4.6, 85, "3.8 km", "+998946789024", False, "Shayxontohur"),
            ("Farhod Mamatov", 4.9, 195, "1.1 km", "+998977890125", True, "Yakkasaroy"),
            ("Eldor Zokirov", 4.7, 67, "4.5 km", "+998998901226", False, "Sergeli")
        ],
        "Mikrotolqinli pech (Mikrovolnovka)": [
            ("Murod Master", 4.8, 62, "3.0 km", "+998904567831", True, "Olmazor"),
            ("Akmal Raximov", 4.9, 115, "1.4 km", "+998915678932", True, "Chilonzor"),
            ("Umidjon Pech", 4.7, 78, "2.9 km", "+998936789033", False, "Uchtepa"),
            ("Jamshid Bekov", 4.6, 40, "4.8 km", "+998947890134", False, "Yashnobod"),
            ("Xurshid Aliyev", 4.8, 93, "2.2 km", "+998978901235", True, "Mirzo Ulug'bek"),
            ("Ulug'bek Usta", 4.5, 33, "5.2 km", "+998999012336", False, "Sergeli")
        ],
        "Boshqa maishiy muammo": []
    },
    "Elektronika va Gadjetlar": {
        "Smartfonlar va Mobil telefonlar": [
            ("Jasurbek Aliyev (iPhone master)", 4.9, 320, "1.2 km", "+998905551122", True, "Chilonzor"),
            ("Sardor Qodirov (Android master)", 4.7, 185, "2.5 km", "+998916662233", True, "Yunusobod"),
            ("Farrux Mobile", 4.8, 140, "0.9 km", "+998937773344", True, "Mirobod"),
            ("Jamshid Fix", 4.9, 250, "1.8 km", "+998948884455", True, "Yakkasaroy"),
            ("Nodirbek Apple", 4.8, 165, "2.0 km", "+998979995566", False, "Mirzo Ulug'bek"),
            ("Bobur Samsung", 4.6, 98, "3.4 km", "+998990006677", False, "Olmazor"),
            ("Sirojiddin Gadget", 4.7, 112, "2.9 km", "+998901117788", False, "Shayxontohur")
        ],
        "Planshetlar va iPad qurilmalari": [
            ("Bobur Usmonov", 4.8, 95, "3.1 km", "+998905678941", True, "Yashnobod"),
            ("Aziz Masharipov", 4.9, 140, "1.1 km", "+998916789042", True, "Chilonzor"),
            ("Husniddin Tab", 4.7, 68, "2.8 km", "+998937890143", False, "Uchtepa"),
            ("Dilshod iPad", 4.9, 180, "1.6 km", "+998948901244", True, "Yunusobod"),
            ("Kamron Raxmatov", 4.6, 52, "4.0 km", "+998979012345", False, "Sergeli"),
            ("Javohir Master", 4.8, 87, "2.3 km", "+998990123446", False, "Mirobod")
        ],
        "Noutbuk va Kompyuter texnikasi": [
            ("Aziz Rahimov", 4.9, 240, "0.8 km", "+998906789051", True, "Chilonzor"),
            ("Otabek PC", 4.6, 60, "2.0 km", "+998917890152", False, "Mirzo Ulug'bek"),
            ("Sanjar IT", 4.8, 175, "1.9 km", "+998938901253", True, "Yakkasaroy"),
            ("Doston Comp", 4.7, 110, "3.3 km", "+998949012354", False, "Shayxontohur"),
            ("Sherzod Laptop", 4.9, 205, "1.3 km", "+998970123455", True, "Mirobod"),
            ("Ravshan Windows", 4.5, 45, "4.7 km", "+998991234556", False, "Olmazor")
        ],
        "Aqlli soatlar (Smartwatch / Apple Watch)": [
            ("Farrux Gadget", 4.8, 76, "2.0 km", "+998907890161", True, "Yunusobod"),
            ("Asilbek Watch", 4.9, 130, "1.2 km", "+998918901262", True, "Chilonzor"),
            ("Diyorbek AppleWatch", 4.7, 85, "2.6 km", "+998939012363", False, "Mirzo Ulug'bek"),
            ("Shoxrux Smart", 4.6, 42, "3.9 km", "+998940123464", False, "Uchtepa"),
            ("Mansur Isoqov", 4.8, 94, "1.7 km", "+998971234565", True, "Yakkasaroy"),
            ("Xursandbek Usta", 4.5, 30, "5.1 km", "+998992345666", False, "Sergeli")
        ],
        "Boshqa elektronika muammosi": []
    },
    "Santexnika muammolari": {
        "Rakovina, krant va jo'mraklar ta'miri": [
            ("Jasur Santexnik", 4.9, 310, "0.5 km", "+998908901271", True, "Chilonzor"),
            ("Ilhom Zokirov", 4.8, 175, "1.8 km", "+998919012372", True, "Mirobod"),
            ("Sanjar Krant", 4.7, 90, "3.2 km", "+998930123473", False, "Olmazor"),
            ("Murod Vanna", 4.9, 210, "1.0 km", "+998941234574", True, "Yakkasaroy"),
            ("Abdurohman Usta", 4.6, 65, "4.1 km", "+998972345675", False, "Sergeli"),
            ("Zuhiddin Santex", 4.8, 135, "2.4 km", "+998993456776", True, "Yunusobod"),
            ("Sherali Karimov", 4.7, 82, "3.6 km", "+998904567877", False, "Yashnobod")
        ],
        "Quvurlar va oqish (protechka) muammosi": [
            ("Bahrom Truba", 4.7, 115, "2.3 km", "+998909012381", False, "Shayxontohur"),
            ("Umid Santexnik", 4.9, 205, "1.1 km", "+998910123482", True, "Chilonzor"),
            ("Nodirbek Aquafix", 4.8, 140, "1.9 km", "+998931234583", True, "Mirzo Ulug'bek"),
            ("Alisher Quvur", 4.6, 70, "3.7 km", "+998942345684", False, "Uchtepa"),
            ("Tohirjon Santex", 4.9, 180, "0.8 km", "+998973456785", True, "Mirobod"),
            ("Shavkat Truboprof", 4.7, 95, "2.9 km", "+998994567886", False, "Yakkasaroy")
        ],
        "Hojatxona va vanna tizimlari": [
            ("Sherzod Usta", 4.8, 90, "3.5 km", "+998901234591", True, "Olmazor"),
            ("Farhod Vanna", 4.9, 160, "1.3 km", "+998912345692", True, "Chilonzor"),
            ("Jamshid Unitaz", 4.7, 85, "2.7 km", "+998933456793", False, "Yunusobod"),
            ("Botir Santexnik", 4.6, 50, "4.2 km", "+998944567894", False, "Sergeli"),
            ("Komiljon Umarov", 4.8, 110, "2.1 km", "+998975678995", True, "Mirobod"),
            ("Nurmurod Master", 4.7, 68, "3.8 km", "+998996789096", False, "Yashnobod")
        ],
        "Kanalizatsiya va tıkanoqlikni ochish": [
            ("Anvar Chistka", 4.9, 280, "0.7 km", "+998902345601", True, "Chilonzor"),
            ("Akmal Kanalizatsiya", 4.8, 150, "1.6 km", "+998913456702", True, "Mirzo Ulug'bek"),
            ("Dravshon Zassor", 4.7, 92, "3.1 km", "+998934567803", False, "Shayxontohur"),
            ("Sardor Ochish", 4.9, 210, "1.2 km", "+998945678904", True, "Yakkasaroy"),
            ("Oktam Santex", 4.6, 60, "4.4 km", "+998976789005", False, "Uchtepa"),
            ("Sobirjon Chist", 4.8, 105, "2.3 km", "+998997890106", True, "Yunusobod")
        ],
        "Boshqa santexnika muammosi": []
    }
}

PRICE_ESTIMATES_DB = {
    "Kir yuvish mashinasi ta'miri va tozalash": "100,000 - 250,000 so'm",
    "Muzlatgich va sovutish tizimlari": "150,000 - 350,000 so'm",
    "Gaz plitasi va pech (duhovka) ta'miri": "80,000 - 180,000 so'm",
    "Konditsioner tozalash va freon quyish": "120,000 - 300,000 so'm",
    "Mikrotolqinli pech (Mikrovolnovka)": "70,000 - 150,000 so'm",
    "Smartfonlar va Mobil telefonlar": "50,000 - 400,000 so'm",
    "Planshetlar va iPad qurilmalari": "80,000 - 450,000 so'm",
    "Noutbuk va Kompyuter texnikasi": "100,000 - 500,000 so me",
    "Aqlli soatlar (Smartwatch / Apple Watch)": "70,000 - 300,000 so'm",
    "Rakovina, krant va jo'mraklar ta'miri": "50,000 - 150,000 so'm",
    "Quvurlar va oqish (protechka) muammosi": "100,000 - 300,000 so'm",
    "Hojatxona va vanna tizimlari": "80,000 - 250,000 so'm",
    "Kanalizatsiya va tıkanoqlikni ochish": "120,000 - 350,000 so'm"
}

WORKER_REVIEWS_DB = {
    "Nodir Abdullayev": [
        {"client": "Sardor", "comment": "Kir yuvish mashinasini gigiyenik tozalab berdi, hamma hidlar yo'qoldi.", "rating": 5},
        {"client": "Madina", "comment": "Baraban shovqin qilayotgan edi, podshipnikni almashtirib berdi. Rahmat!", "rating": 5}
    ],
    "Jasurbek Aliyev (iPhone master)": [
        {"client": "Murod", "comment": "Ekranini 20 daqiqada almashtirib berdi, super!", "rating": 5}
    ]
}

# Yangi ustalar ariza bazasi (Vaqtincha xotirada)
MASTER_APPLICATIONS_DB = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "categories": SERVICES_DB,
            "reviews_db": WORKER_REVIEWS_DB,
            "price_db": PRICE_ESTIMATES_DB,
            "districts": DISTRICTS
        }
    )

@app.get("/api/services")
async def get_services(category: str):
    if category in SERVICES_DB:
        return {"services": list(SERVICES_DB[category].keys())}
    return {"services": []}

@app.get("/api/technicians")
async def get_technicians(category: str, service: str, district: str = "Barchasi (Hudud bo'yicha)"):
    if category in SERVICES_DB and service in SERVICES_DB[category]:
        workers = SERVICES_DB[category][service]
        
        # Tuman filtri
        if district and district != "Barchasi (Hudud bo'yicha)":
            workers = [w for w in workers if w[6] == district]
            
        estimate = PRICE_ESTIMATES_DB.get(service, "Kelishilgan narxda")
        return {
            "workers": [
                {
                    "name": w[0],
                    "rating": w[1],
                    "reviews_count": w[2],
                    "distance": w[3],
                    "phone": w[4],
                    "verified": w[5],
                    "district": w[6]
                }
                for w in workers
            ],
            "price_estimate": estimate
        }
    return {"workers": [], "price_estimate": "Noma'lum"}

# Live Search API
@app.get("/api/search")
async def search_technicians(query: str = ""):
    q = query.strip().lower()
    if not q or len(q) < 2:
        return {"workers": []}
    
    results = []
    seen = set()
    
    for cat, services in SERVICES_DB.items():
        for s_name, workers in services.items():
            for w in workers:
                # Usta ismi, xizmat nomi yoki tumaniga ko'ra qidirish
                if (q in w[0].lower() or q in s_name.lower() or q in w[6].lower()) and w[0] not in seen:
                    results.append({
                        "name": w[0],
                        "rating": w[1],
                        "reviews_count": w[2],
                        "distance": w[3],
                        "phone": w[4],
                        "verified": w[5],
                        "district": w[6],
                        "service": s_name
                    })
                    seen.add(w[0])
                    
    return {"workers": results[:10]} # Maksimal 10 ta natija

# Usta bo'lib ro'yxatdan o'tish formasi
@app.post("/apply-as-master")
async def apply_master(
    full_name: str = Form(...),
    phone: str = Form(...),
    category: str = Form(...),
    district: str = Form(...)
):
    MASTER_APPLICATIONS_DB.append({
        "full_name": full_name,
        "phone": phone,
        "category": category,
        "district": district
    })
    return RedirectResponse(url="/?applied=true", status_code=303)

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
