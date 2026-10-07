from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="UstaGo API")

templates = Jinja2Templates(directory="templates")

# Every worker tuple format: (Name, Rating, ReviewsCount, Distance, Phone)
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
    # --- Maishiy Texnika ---
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
        {"client": "Davron", "comment": "Motor cho'tkalarini almashtirib berdi, mashinka yangiday ishlayapti.", "rating": 5},
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
        {"client": "Murod", "comment": "Muzlatgich eshik rezinalarini almashtirib berdi.", "rating": 5},
        {"client": "Kamola", "comment": "Insofli usta, narxi ham qimmat emas.", "rating": 4}
    ],
    "Dilshod Qodirov": [
        {"client": "Rustam", "comment": "Bosch muzlatgichni rasmiy servisdagidan arzonroq tuzatdi.", "rating": 5},
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
        {"client": "Zohid", "comment": "Gaz sizishini to'xtatib, xavfsizlik klapanini o'rnatdi.", "rating": 5},
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
        {"client": "Ulug'bek", "comment": "Gaz shlangini xavfsiz rezina shlangga almashtirdi.", "rating": 4},
        {"client": "Zaynab", "comment": "Sifatli xizmat ko'rsatildi.", "rating": 5}
    ],
    "Bekzod KOND": [
        {"client": "Jamshid", "comment": "Konditsioner filtrlarini yuvib, freon quydi. Muzdek!", "rating": 5},
        {"client": "Diyora", "comment": "Mavsum oldidan juda kerakli xizmat bo'ldi.", "rating": 4}
    ],
    "Sardor Klimat": [
        {"client": "Jahongir", "comment": "Konditsionerga freon quyib berdi, sovuqligi zo'r bo'ldi.", "rating": 5},
        {"client": "Barno", "comment": "Drenajni tozalab berdi, suv oqishi to'xtadi.", "rating": 5}
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
        {"client": "Sherzod", "comment": "Konditsionerni demontaj qilib boshqa xonaga ko'chirdi.", "rating": 5},
        {"client": "G'azal", "comment": "Ixcham va toza ishlaydi.", "rating": 4}
    ],
    "Murod Master": [
        {"client": "Farrux", "comment": "Mikrovolnovka likopcha motorini almashtirdi.", "rating": 5},
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
        {"client": "Dilmurod", "comment": "Sensori ishlamay qolgandi, tugmachali panelga o'tkazdi.", "rating": 5},
        {"client": "Sabohat", "comment": "Mas'uliyatli usta.", "rating": 5}
    ],
    "Ulug'bek Usta": [
        {"client": "Davlat", "comment": "Ichki saqlagichini (predoxranitel) almashtirib berdi.", "rating": 4},
        {"client": "Shirin", "comment": "Tushunarli tushuntirib berdi.", "rating": 5}
    ],

    # --- Elektronika va Gadjetlar ---
    "Jasurbek Aliyev (iPhone master)": [
        {"client": "Murod", "comment": "Ekranini 20 daqiqada almashtirib berdi, super!", "rating": 5},
        {"client": "Kamron", "comment": "iPhone 13 battery health 100% qilib yangilap berdi.", "rating": 5}
    ],
    "Sardor Qodirov (Android master)": [
        {"client": "Doston", "comment": "Samsung S21 ekranini originaliga almashtirdi.", "rating": 5},
        {"client": "Laylo", "comment": "Gnezdosini almashtirib berdi, tez zaryad olmoqda.", "rating": 4}
    ],
    "Farrux Mobile": [
        {"client": "Shoxrux", "comment": "Suvga tushgan telefonni platasini tozalab berdi.", "rating": 5},
        {"client": "Munira", "comment": "Platasidagi mikrosxemani qayta kalitlab berdi.", "rating": 5}
    ],
    "Jamshid Fix": [
        {"client": "Javohir", "comment": "Xiaomi telefondagi bootloop xatosini tuzatdi.", "rating": 5},
        {"client": "Zarina", "comment": "Kamerasi ishlamay qolgandi, lentasini almashtirdi.", "rating": 5}
    ],
    "Nodirbek Apple": [
        {"client": "Sirojiddin", "comment": "FaceID ishlamay qolgandi, tiklab berdi.", "rating": 5},
        {"client": "Madinabonu", "comment": "Orqa shishasini lazerda sifatli almashtirdi.", "rating": 5}
    ],
    "Bobur Samsung": [
        {"client": "Mirzo", "comment": "Dinamikidan ovoz chiqmayotgandi, tozalab yangiladi.", "rating": 4},
        {"client": "Nodira", "comment": "Original zapchast qo'ygani uchun rahmat.", "rating": 5}
    ],
    "Sirojiddin Gadget": [
        {"client": "Sardor", "comment": "Mikrofon va dinamiklarini diagnostika qildi.", "rating": 5},
        {"client": "Gulnoza", "comment": "Proshivkasini yangilab berdi.", "rating": 4}
    ],
    "Bobur Usmonov": [
        {"client": "Asadbek", "comment": "iPad 9 ekran oynasini sensorini buzmasdan almashtirdi.", "rating": 5},
        {"client": "Aziza", "comment": "Akkumulyatorini yangiladi.", "rating": 5}
    ],
    "Aziz Masharipov": [
        {"client": "Xursand", "comment": "Samsung Tab A7 gnezdosini almashtirib berdi.", "rating": 5},
        {"client": "Dildora", "comment": "Rasm va ma'lumotlarimni saqlab qoldi!", "rating": 5}
    ],
    "Husniddin Tab": [
        {"client": "Rustam", "comment": "Grafik planshetni qalamini sozlab berdi.", "rating": 4},
        {"client": "Charos", "comment": "Tezkor va sifatli xizmat.", "rating": 5}
    ],
    "Dilshod iPad": [
        {"client": "Bek", "comment": "iPad Pro zaryadlash chipini almashtirib berdi.", "rating": 5},
        {"client": "Surayyo", "comment": "Ishim bitdi, katta rahmat!", "rating": 5}
    ],
    "Kamron Raxmatov": [
        {"client": "Nodir", "comment": "Display modulini tezda topib o'rnatib berdi.", "rating": 4},
        {"client": "Feruz", "comment": "Baraka topsin usta.", "rating": 5}
    ],
    "Javohir Master": [
        {"client": "Sanjar", "comment": "Planshet bluetooth modullarini ta'mirladi.", "rating": 5},
        {"client": "Gulinur", "comment": "Toza va chiroyli ta'mirlash.", "rating": 4}
    ],
    "Aziz Rahimov": [
        {"client": "Ravshan", "comment": "Noutbukni termo-pastasini almashtirib tozaladi.", "rating": 5},
        {"client": "Zebo", "comment": "SSD o'rnatib Windows 11 qo'yib berdi.", "rating": 5}
    ],
    "Otabek PC": [
        {"client": "Sanjar", "comment": "Kompyuter blok pitaniyasini almashtirdi.", "rating": 4},
        {"client": "Dilbar", "comment": "Videokarta kuleri shovqin qilayotgandi, yog'ladi.", "rating": 5}
    ],
    "Sanjar IT": [
        {"client": "Timur", "comment": "Operativ xotirani ko'paytirib, tezlashtirib berdi.", "rating": 5},
        {"client": "Shoxida", "comment": "Platasini qayta kavsharlab berdi.", "rating": 5}
    ],
    "Doston Comp": [
        {"client": "Xurshed", "comment": "Noutbuk klaviaturasini almashtirib berdi.", "rating": 4},
        {"client": "Oksana", "comment": "Ekran shleyfini almashtirdi.", "rating": 5}
    ],
    "Sherzod Laptop": [
        {"client": "Anvar", "comment": "Asus ROG gaming noutbukni sovutish tizimini tozaladi.", "rating": 5},
        {"client": "Sitora", "comment": "Zaryadlash portini almashtirib berdi.", "rating": 5}
    ],
    "Ravshan Windows": [
        {"client": "Tohir", "comment": "Barcha kerakli dasturlarni va antikvivrusni o'rnatdi.", "rating": 4},
        {"client": "Malika", "comment": "Printer drayverlarini sozlab berdi.", "rating": 5}
    ],
    "Farrux Gadget": [
        {"client": "Farxod", "comment": "Apple Watch ekranini almashtirib berdi.", "rating": 5},
        {"client": "Nilufar", "comment": "Tasma (remeshok) qisqichini sozlab berdi.", "rating": 5}
    ],
    "Asilbek Watch": [
        {"client": "Jamshid", "comment": "Galaxy Watch bateriyasini yangiladi.", "rating": 5},
        {"client": "Dinora", "comment": "Sensorni kalibrovka qilib berdi.", "rating": 5}
    ],
    "Diyorbek AppleWatch": [
        {"client": "Shohruh", "comment": "Watch Series 7 korpusini va oynasini silliqladi.", "rating": 4},
        {"client": "Nargiza", "comment": "Zaryadnik platasini ta'mirladi.", "rating": 5}
    ],
    "Shoxrux Smart": [
        {"client": "Ulug'bek", "comment": "Amazfit soatimni ulanmayotganini sozlab berdi.", "rating": 4},
        {"client": "Dildora", "comment": "Bluetooth aloqasini tikladi.", "rating": 5}
    ],
    "Mansur Isoqov": [
        {"client": "Jasur", "comment": "Soat dinamigiga suv kirganini tozaladi.", "rating": 5},
        {"client": "Lola", "comment": "Tugmachalar qotib qolganini sozlab berdi.", "rating": 5}
    ],
    "Xursandbek Usta": [
        {"client": "Doniyor", "comment": "Xizmatidan mamnunman, tez bajarildi.", "rating": 4},
        {"client": "Shahnoza", "comment": "Yaxshi muomala va tezkor ish.", "rating": 5}
    ],

    # --- Santexnika ---
    "Jasur Santexnik": [
        {"client": "Laziz", "comment": "Quvurdagi oqishni tezda to'xtatdi, raxmat!", "rating": 5},
        {"client": "Otabek", "comment": "Grohe smesitelini o'rnatib berdi.", "rating": 5}
    ],
    "Ilhom Zokirov": [
        {"client": "Sardor", "comment": "Rakovina ostidagi sifon va shlanglarni almashtirdi.", "rating": 5},
        {"client": "Gulsanam", "comment": "Krant tomchilab turgandi, prokladkasini yangiladi.", "rating": 4}
    ],
    "Sanjar Krant": [
        {"client": "Dilshod", "comment": "Dush smesitelini tezda montaj qildi.", "rating": 5},
        {"client": "Dilnoza", "comment": "Xushfe'l usta, rahmat.", "rating": 4}
    ],
    "Murod Vanna": [
        {"client": "Bobur", "comment": "Jakuzi smesiteli va dush ushlagichini o'rnatdi.", "rating": 5},
        {"client": "Aziza", "comment": "Ajoyib sifat va toza ish.", "rating": 5}
    ],
    "Abdurohman Usta": [
        {"client": "Omon", "comment": "Oshxona rakovinasini o'rnatib, suv bosimini sozlab berdi.", "rating": 4},
        {"client": "Munira", "comment": "Vaqtida keldi va muammoni hal qildi.", "rating": 5}
    ],
    "Zuhiddin Santex": [
        {"client": "Rustam", "comment": "Suv filtrlarini montaj qilib berdi.", "rating": 5},
        {"client": "Umida", "comment": "Juda hushfe'l inson ekan.", "rating": 5}
    ],
    "Sherali Karimov": [
        {"client": "Shohjahon", "comment": "Suv isitgich (Ariston) krantlarini yangiladi.", "rating": 4},
        {"client": "Madina", "comment": "Tez va arzon xizmat.", "rating": 5}
    ],
    "Bahrom Truba": [
        {"client": "Javlon", "comment": "Devor ichidagi plastmassa quvurni payvandladi.", "rating": 5},
        {"client": "Maloxat", "comment": "Oqayotgan jo'mrakni darhol to'xtatdi.", "rating": 4}
    ],
    "Umid Santexnik": [
        {"client": "Nodir", "comment": "Kvartiradagi barcha quvurlarni yangisiga o'tkazdi.", "rating": 5},
        {"client": "Diyora", "comment": "Juda toza va chiroyli payvand qildi.", "rating": 5}
    ],
    "Nodirbek Aquafix": [
        {"client": "Farrux", "comment": "Suv bosimini oshiruvchi nasosni o'rnatdi.", "rating": 5},
        {"client": "Muborak", "comment": "Oqayotgan joyini payvandlab berdi.", "rating": 5}
    ],
    "Alisher Quvur": [
        {"client": "Jamshid", "comment": "Isitish tizimi (otopleniye) quvurlarini tozaladi.", "rating": 4},
        {"client": "Shahlo", "comment": "Yaxshi mutaxassis.", "rating": 5}
    ],
    "Tohirjon Santex": [
        {"client": "Sherzod", "comment": "Plastik quvurlar kollektorini yig'ib berdi.", "rating": 5},
        {"client": "Zulxumor", "comment": "Toza va sifatli xizmat.", "rating": 5}
    ],
    "Shavkat Truboprof": [
        {"client": "Botir", "comment": "Teshilgan quvurni tezda almashtirib berdi.", "rating": 4},
        {"client": "Zaynab", "comment": "Chaqiruvga darhol yetib keldi.", "rating": 5}
    ],
    "Sherzod Usta": [
        {"client": "Bahodir", "comment": "Unitaz bachog'i (siston) mexanizmini almashtirdi.", "rating": 5},
        {"client": "Umida", "comment": "Vannani germetiklab berdi.", "rating": 5}
    ],
    "Farhod Vanna": [
        {"client": "Murod", "comment": "Akkril vannani sifatli montaj qilib berdi.", "rating": 5},
        {"client": "Shahnoza", "comment": "Dush kabinasi eshigini sozlab berdi.", "rating": 5}
    ],
    "Jamshid Unitaz": [
        {"client": "Otabek", "comment": "Podvesnoy (instyle) unitazni montaj qildi.", "rating": 5},
        {"client": "Sitora", "comment": "Tez va sifatli o'rnatdi.", "rating": 4}
    ],
    "Botir Santexnik": [
        {"client": "Laziz", "comment": "Vanna ostidagi sifonni yangiladi.", "rating": 4},
        {"client": "Mavjuda", "comment": "Rahmat usta aka.", "rating": 5}
    ],
    "Komiljon Umarov": [
        {"client": "Davron", "comment": "Gigiyenik dush o'rnatib berdi.", "rating": 5},
        {"client": "Nigora", "comment": "Sifatli va kafolatli xizmat.", "rating": 5}
    ],
    "Nurmurod Master": [
        {"client": "Kamar", "comment": "Hojatxona havoni tortish tizimini sozladi.", "rating": 4},
        {"client": "Guli", "comment": "Yaxshi usta.", "rating": 5}
    ],
    "Anvar Chistka": [
        {"client": "Murodjon", "comment": "Kanalizatsiya tıkanib qolgandi, tros bilan ochdi.", "rating": 5},
        {"client": "Nigora", "comment": "Oshxona quvurini tozalab berdi.", "rating": 5}
    ],
    "Akmal Kanalizatsiya": [
        {"client": "Bekzod", "comment": "Gidrodinamik usulda quvurlarni tozaladi.", "rating": 5},
        {"client": "Shoira", "comment": "Sassiq hid ketdi, rahmat usta!", "rating": 4}
    ],
    "Dravshon Zassor": [
        {"client": "Mirzo", "comment": "Tıkanib qolgan maxsus quvurni maxsus apparatda ochdi.", "rating": 5},
        {"client": "Lola", "comment": "Tez yetib keldi.", "rating": 4}
    ],
    "Sardor Ochish": [
        {"client": "Jahongir", "comment": "Oshxona va vanna quvurlarini tozalab berdi.", "rating": 5},
        {"client": "Dildora", "comment": "Juda tajribali usta.", "rating": 5}
    ],
    "Oktam Santex": [
        {"client": "Umid", "comment": "Kanalizatsiya quvuri tirqishini berkitdi.", "rating": 4},
        {"client": "Nodira", "comment": "Toza ishlab ketdi.", "rating": 5}
    ],
    "Sobirjon Chist": [
        {"client": "Sanjar", "comment": "Markaziy truba tıkanoqligini bartaraf qildi.", "rating": 5},
        {"client": "Feruza", "comment": "E'tiborli va insofli usta.", "rating": 5}
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
