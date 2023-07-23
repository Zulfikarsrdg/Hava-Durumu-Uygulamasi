import re
import requests
import tkinter as tk
from tkinter import messagebox
from urllib.parse import quote
from unidecode import unidecode


def get_weather_data():
    city = selected_city.get()
    if not city:
        messagebox.showerror("Error", "Please select a city.")
        return


    encoded_city = quote(unidecode(city))
    url = f"https://www.havadurumu15gunluk.net/havadurumu/{encoded_city.lower()}-hava-durumu-15-gunluk.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
        site = response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not fetch weather data for {city}. Please check the city name and try again.")
        return

    r_gunduz = '<td width="45">&nbsp;&nbsp;(-?\d+)°C</td>'
    r_gece = '<td width="45">&nbsp;(-?\d+)°C</td>'
    r_gun = '<td width="70" nowrap="nowrap">(.*)</td>'
    r_tarih = '<td width="75" nowrap="nowrap">(.*)</td>'
    r_aciklama = '<img src="/havadurumu/images/trans.gif" alt="(.*)" width="1" height="1" />'

    comp_gunduz = re.compile(r_gunduz)
    comp_gece = re.compile(r_gece)
    comp_gun = re.compile(r_gun)
    comp_tarih = re.compile(r_tarih)
    comp_aciklama = re.compile(r_aciklama)

    gunduz = []
    gece = []
    gun = []
    tarih = []
    aciklama = []

    for i in re.findall(r_gunduz, site):
        gunduz.append(i)

    for i in re.findall(r_gece, site):
        gece.append(i)

    for i in re.findall(r_gun, site):
        gun.append(i)

    for i in re.findall(r_tarih, site):
        tarih.append(i)

    for i in re.findall(r_aciklama, site):
        aciklama.append(i)

    if len(gun) > 0:
        weather_info = f"Gündüz: {gunduz[0]} °C\nGece: {gece[0]} °C\nAçıklama: {city} hava durumu."
        label_result.config(text=weather_info)
    else:
        messagebox.showerror("Error", f"Could not fetch weather data for {city}. Please check the city name and try again.")



cities = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin",
    "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa",
    "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum",
    "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir",
    "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir",
    "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak",
    "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"
]

window = tk.Tk()
window.title("Weather App")
window.minsize(width=400, height=250)

label = tk.Label(text="Hava durumunu öğrenmek istediğiniz şehri seçin.")
label.pack()

selected_city = tk.StringVar()
selected_city.set(cities[0])
dropdown_city = tk.OptionMenu(window, selected_city, *cities)
dropdown_city.pack(pady=10)

button = tk.Button(text="Hava durumunu al", command=get_weather_data)
button.pack()

label_result = tk.Label()
label_result.pack()

window.mainloop()
