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

# Har bir ustada kamida 2 tadan sharh mavjud
WORKER_REVIEWS_DB = {
    # Maishiy texnika ustalari
    "Nodir Abdullayev": [
        {"client": "Sardor", "comment": "Kir yuvish mashinasini gigiyenik tozalab berdi, hamma hidlar yo'qoldi.", "rating": 5},
        {"client": "Madina", "comment": "Baraban shovqin qilayotgan edi, podshipnikni almashtirib berdi. Rahmat!", "rating": 5}
    ],
    "Rustam Jo'rayev": [
        {"client": "Bekzod", "comment": "Toshkent markaziga yetib kelishi tez bo'ldi. Sifatli ta'mir.", "rating": 5},
        {"client": "Nilufar", "comment": "Suv to'kib yuborayotgan edi, nasosini almashtirib berdi.", "rating": 4}
    ],
    "Otabek KirMashina": [
        {"client": "Jasur", "comment": "Ishiga juda mas'uliyatli usta. Barcha detallarga kafolat berdi.", "rating": 5},
        {"client": "Umida", "comment": "Tushunmovchiliksiz tez va toza ishlab ketdi.", "rating": 5}
    ],
    "Sardor Umarov": [
        {"client": "Otabek", "comment": "Artel kir mashinamizni tezda sozlab berdi. Tavsiya qilaman!", "rating": 5},
        {"client": "Lola", "comment": "O'z ishining ustasi, narxi ham juda hamyonbop.", "rating": 5}
    ],
    "Jahongir Vahobov": [
        {"client": "Sherzod", "comment": "Platasida muammo bor ekan, qayta proshivka qilib berdi.", "rating": 4},
        {"client": "Nigora", "comment": "Vaqtida keldi, muammoni darhol aniqladi.", "rating": 5}
    ],
    "Ilhomiddin Usta": [
        {"client": "Bobur", "comment": "LG kir yuvish mashinasining shlangini almashtirdi. Baraka topsin.", "rating": 5},
        {"client": "Dildora", "comment": "Juda hushfe'l va insofli usta.", "rating": 5}
    ],
    "Botirxon Axmedov": [
        {"client": "Davron", "comment": "Motor cho'tkalarini almashtirib berdi, mashinka yana yangiday ishlayapti.", "rating": 5},
        {"client": "Aziza", "comment": "Xizmat ko'rsatish darajasi a'lo.", "rating": 4}
    ],

    "Anvar Xolodilshik": [
        {"client": "Dilshod", "comment": "Muzlatgich freonini quyib berdi, hozir muzlatishi juda zo'r.", "rating": 5},
        {"client": "Shaxnoza", "comment": "Motorini almashtirdi, kafolat taloni ham berdi.", "rating": 5}
    ],
    "Zokir Master": [
        {"client": "Jahongir", "comment": "Eski Stinol muzlatgichimizni ham zo'r sozlab berdi.", "rating": 4},
        {"client": "Sevara", "comment": "Tez va sifatli ta'mirlash uchun rahmat!", "rating": 5}
    ],
    "Murod Xolod": [
        {"client": "Farhod", "comment": "No-Frost tizimi muzlab qolayotgan edi, datchigini almashtirdi.", "rating": 5},
        {"client": "Guli", "comment": "Chaqiruvimizga tezda yetib keldi.", "rating": 5}
    ],
    "Shohrux Sovutgich": [
        {"client": "Murod", "comment": "Muzlatgich eshik rezinalarini almashtirib berdi. Zanglagan joylarini ham tozalab ketdi.", "rating": 5},
        {"client": "Kamola", "comment": "Insofli usta, narxi ham qimmat emas.", "rating": 4}
    ],
    "Dilshod Qodirov": [
        {"client": "Rustam", "comment": "Bosch muzlatgichni rasmiy servisdagidan arzonroq va tezroq tuzatib berdi.", "rating": 5},
        {"client": "Nodira", "comment": "Baraka topsinlar, muzlatgichim saqlab qolindi.", "rating": 5}
    ],
    "Alisher Tursunov": [
        {"client": "Ilhom", "comment": "Kompressor muammosini tezda hal qildi.", "rating": 4},
        {"client": "Muxlisa", "comment": "O'z ishining ustasi, rahmat.", "rating": 5}
    ],

    "Davron Valiyev": [
        {"client": "Alisher", "comment": "Gaz plita forsunkalarini tozalab, alangasini sozlab berdi.", "rating": 5},
        {"client": "Malika", "comment": "Elektro-podjig ishlamayotgan edi, almashtirib berdi.", "rating": 5}
    ],
    "Shoxrux Qosmonov": [
        {"client": "Sanjar", "comment": "Duhovka qizimayotgan edi, tenini almashtirdi.", "rating": 4},
        {"client": "Munisa", "comment": "Juda toza va tartibli ishladi.", "rating": 5}
    ],
    "Olimjon Gaz": [
        {"client": "Zohid", "comment": "Gaz szivishini to'xtatib, xavfsizlik klapanini o'rnatdi.", "rating": 5},
        {"client": "Nargiza", "comment": "Ajoyib mutaxassis, o'z ishini biladi.", "rating": 5}
    ],
    "Hikmatillo Usta": [
        {"client": "Siroj", "comment": "Pech oynasini almashtirib berdi, juda shaffof va mustahkam.", "rating": 5},
        {"client": "Feruza", "comment": "Vaqtida kelgani uchun rahmat.", "rating": 4}
    ],
    "Bobur Isoqov": [
        {"client": "Shohruh", "comment": "Beko plitamizni qisqa vaqtda sozlab berdi.", "rating": 5},
        {"client": "Gulasal", "comment": "Xushmuomala va tajribali usta.", "rating": 5}
    ],
    "Sanjar Narziyev": [
        {"client": "Ulug'bek", "comment": "Gaz shlangini xavfsiz rezina shlangga almashtirib berdi.", "rating": 4},
        {"client": "Zaynab", "comment": "Sifatli xizmat ko'rsatildi.", "rating": 5}
    ],

    "Bekzod KOND": [
        {"client": "Jamshid", "comment": "Konditsioner filtrlarini yuvib, freon quydi. Muzdek sovutayapti.", "rating": 5},
        {"client": "Diyora", "comment": "Mavsum oldidan juda kerakli xizmat bo'ldi.", "rating": 4}
    ],
    "Sardor Klimat": [
        {"client": "Jahongir", "comment": "Konditsionerga freon quyib berdi, sovuqligi zo'r bo'ldi.", "rating": 5},
        {"client": "Barno", "comment": "Trubalardan suv oqayotgan edi, drenajni tozalab berdi.", "rating": 5}
    ],
    "Islomjon Klimat": [
        {"client": "Akmal", "comment": "Inverter konditsionerni proshivka qilib berdi.", "rating": 5},
        {"client": "Saida", "comment": "Tashqi blokni ham yuvib tozalab ketdi.", "rating": 5}
    ],
    "Jasur Freon": [
        {"client": "Otabek", "comment": "30 daqiqada yetib keldi. R-410 freon quyib berdi.", "rating": 4},
        {"client": "Dilfuza", "comment": "Baraka topsin, juda yaxshi usta.", "rating": 5}
    ],
    "Farhod Mamatov": [
        {"client": "Bekzod", "comment": "Platasidagi kondensatorlarni almashtirib sozlab berdi.", "rating": 5},
        {"client": "Shahlo", "comment": "Toshkent bo'ylab eng yaxshi klimatist!", "rating": 5}
    ],
    "Eldor Zokirov": [
        {"client": "Sherzod", "comment": "Konditsionerni demontaj qilib boshqa xonaga ko'chirib berdi.", "rating": 5},
        {"client": "G'azal", "comment": "Ixcham va toza ishlaydi.", "rating": 4}
    ],

    "Murod Master": [
        {"client": "Farrux", "comment": "Mikrovolnovka likopchasi aylanmayotgan edi, motorini almashtirdi.", "rating": 5},
        {"client": "Zulfiya", "comment": "Qizitmayotgan edi, magnetronini sozlab berdi.", "rating": 5}
    ],
    "Akmal Raximov": [
        {"client": "Tohir", "comment": "Eski LG mikrovolnovkamizni saqlab qoldi.", "rating": 5},
        {"client": "Rayhon", "comment": "Juda tez va sifatli xizmat.", "rating": 5}
    ],
    "Umidjon Pech": [
        {"client": "Mansur", "comment": "Eshik zamogini almashtirdi. Hozir bemalol yopilyapti.", "rating": 5},
        {"client": "Nargiz", "comment": "Arzon va sifatli xizmat ko'rsatdi.", "rating": 4}
    ],
    "Jamshid Bekov": [
        {"client": "Botir", "comment": "Kondensatorini almashtirdi, uchqun chiqarmayapti endi.", "rating": 4},
        {"client": "Rano", "comment": "Rahmat usta aka, baraka toping.", "rating": 5}
    ],
    "Xurshid Aliyev": [
        {"client": "Dilmurod", "comment": "Sensori ishlamay qolgandi, tugmachali panelga o'tkazib berdi.", "rating": 5},
        {"client": "Sabohat", "comment": "Mas'uliyatli usta.", "rating": 5}
    ],
    "Ulug'bek Usta": [
        {"client": "Davlat", "comment": "Ichki saqlagichini (predoxranitel) almashtirib berdi.", "rating": 4},
        {"client": "Shirin", "comment": "Tushunarli tushuntirib berdi.", "rating": 5}
    ],

    # Elektronika ustalari
    "Jasurbek Aliyev (iPhone master)": [
        {"client": "Murod", "comment": "Ekranini 20 daqiqada almashtirib berdi, super!", "rating": 5},
        {"client": "Kamron", "comment": "iPhone 13 battery health 100% qilib yangilap berdi. TrueTone saqlanib qoldi.", "rating": 5}
    ],
    "Sardor Qodirov (Android master)": [
        {"client": "Doston", "comment": "Samsung S21 ekranini originaliga almashtirdi.", "rating": 5},
        {"client": "Laylo", "comment": "Gnezdosini almashtirib berdi, tez zaryad olmoqda.", "rating": 4}
    ],
    "Farrux Mobile": [
        {"client": "Shoxrux", "comment": "Suvga tushgan telefonni platasini tozalab qayta yoqib berdi.", "rating": 5},
        {"client": "Munira", "comment": "Platasidagi mikrosxemani qayta kalitlab berdi.", "rating": 5}
    ],
    "Jamshid Fix": [
        {"client": "Javohir", "comment": "Xiaomi telefondagi bootloop xatosini tuzatib berdi.", "rating": 5},
        {"client": "Zarina", "comment": "Kamerasi ishlamay qolgandi, lentasini almashtirdi.", "rating": 5}
    ],
    "Nodirbek Apple": [
        {"client": "Sirojiddin", "comment": "FaceID ishlamay qolgandi, mikroskop ostida tiklab berdi.", "rating": 5},
        {"client": "Madinabonu", "comment": "Orqa shishasini lazerda sifatli almashtirdi.", "rating": 5}
    ],
    "Bobur Samsung": [
        {"client": "Mirzo", "comment": "Dinamikidan ovoz chiqmayotgandi, tozalab yangiladi.", "rating": 4},
        {"client": "Nodira", "comment": "Original zapchast qo'ygani uchun rahmat.", "rating": 5}
    ],
    "Sirojiddin Gadget": [
        {"client": "Sardor", "comment": "Mikrofon va dinamiklarini diagnostika qilib berdi.", "rating": 5},
        {"client": "Gulnoza", "comment": "Proshivkasini yangilab berdi.", "rating": 4}
    ],

    "Bobur Usmonov": [
        {"client": "Asadbek", "comment": "iPad 9 ekran oynasini sensorini buzmasdan almashtirdi.", "rating": 5},
        {"client": "Aziza", "comment": "Zaryad ushlamayotgan edi, akkumulyatorini yangiladi.", "rating": 5}
    ],
    "Aziz Masharipov": [
        {"client": "Xursand", "comment": "Samsung Tab A7 ni gnezdosini almashtirib berdi.", "rating": 5},
        {"client": "Dildora", "comment": "Rasm va ma'lumotlarimni saqlab qolgani uchun rahmat!", "rating": 5}
    ],
    "Husniddin Tab": [
        {"client": "Rustam", "comment": "Grafik planshetni qalamini sozlab berdi.", "rating": 4},
        {"client": "Charos", "comment": "Tezkor va sifatli xizmat.", "rating": 5}
    ],

    "Aziz Rahimov": [
        {"client": "Ravshan", "comment": "Noutbukni termo-pastasini almashtirib tozaladi, qizimayapti endi.", "rating": 5},
        {"client": "Zebo", "comment": "SSD o'rnatib Windows 11 qo'yib berdi, uchoqday ishlayapti.", "rating": 5}
    ],
    "Otabek PC": [
        {"client": "Sanjar", "comment": "Kompyuter blok pitaniyasini almashtirdi.", "rating": 4},
        {"client": "Dilbar", "comment": "Videokarta kuleri shovqin qilayotgandi, yog'lab berdi.", "rating": 5}
    ],

    "Farrux Gadget": [
        {"client": "Farxod", "comment": "Apple Watch ekranini almashtirib berdi, suv kirib ketmaydi.", "rating": 5},
        {"client": "Nilufar", "comment": "Tasma (remeshok) qisqichini sozlab berdi.", "rating": 5}
    ],
    "Asilbek Watch": [
        {"client": "Jamshid", "comment": "Galaxy Watch bateriyasini yangiladi. Endi 2 kunga yetyapti.", "rating": 5},
        {"client": "Dinora", "comment": "Sensor yaxshi ishlamayotgandi, kalibrovka qilib berdi.", "rating": 5}
    ],

    # Santexnika ustalari
    "Jasur Santexnik": [
        {"client": "Laziz", "comment": "Quvurdagi oqishni tezda to'xtatdi, raxmat!", "rating": 5},
        {"client": "Otabek", "comment": "Grohe smesitelini o'rnatib berdi. Ishiga a'lo baho!", "rating": 5}
    ],
    "Ilhom Zokirov": [
        {"client": "Sardor", "comment": "Rakovina ostidagi sifonni va egiluvchan shlanglarni almashtirdi.", "rating": 5},
        {"client": "Gulsanam", "comment": "Krant tomchilab turgandi, prokladkasini yangiladi.", "rating": 4}
    ],
    "Sanjar Krant": [
        {"client": "Dilshod", "comment": "Dush smesitelini tezda montaj qildi.", "rating": 5},
        {"client": "Dilnoza", "comment": "Xushfe'l usta, rahmat.", "rating": 4}
    ],

    "Bahrom Truba": [
        {"client": "Javlon", "comment": "Devor ichidagi plastmassa quvur teshilganini payvandlab berdi.", "rating": 5},
        {"client": "Maloxat", "comment": "Oqayotgan jo'mrakni darhol to'xtatdi.", "rating": 4}
    ],
    "Umid Santexnik": [
        {"client": "Nodir", "comment": "Kvartiradagi barcha plastmassa quvurlarni yangisiga o'tkazdi.", "rating": 5},
        {"client": "Diyora", "comment": "Juda toza va chiroyli payvand qildi.", "rating": 5}
    ],

    "Sherzod Usta": [
        {"client": "Bahodir", "comment": "Unitaz bachog'i (siston) mexanizmini almashtirdi.", "rating": 5},
        {"client": "Umida", "comment": "Vannani germetiklab berdi, endi suv oqmayapti.", "rating": 5}
    ],
    "Farhod Vanna": [
        {"client": "Murod", "comment": "Akkril vannani sifatli montaj qilib berdi.", "rating": 5},
        {"client": "Shahnoza", "comment": "Dush kabinasi eshigini sozlab berdi.", "rating": 5}
    ],

    "Anvar Chistka": [
        {"client": "Murodjon", "comment": "Kanalizatsiya tıkanib qolgandi, tros bilan 15 minutda ochdi.", "rating": 5},
        {"client": "Nigora", "comment": "Ajoyib uskunasi bor ekan, oshxona quvurini tozalab berdi.", "rating": 5}
    ],
    "Akmal Kanalizatsiya": [
        {"client": "Bekzod", "comment": "Gidrodinamik usulda quvurlarni yog'lardan tozaladi.", "rating": 5},
        {"client": "Shoira", "comment": "Sassiq hid ketdi, rahmat usta!", "rating": 4}
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
