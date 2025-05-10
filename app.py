from flask import Flask, render_template, request, send_from_directory
import requests
import os
import math

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", sonuc=None, doviz_sonuc=None)

@app.route('/hesapla', methods=['POST'])
def hesapla():
    sayi1 = float(request.form['sayi1'])
    sayi2 = float(request.form['sayi2'])
    islem = request.form['islem']

    if islem == "toplama":
        sonuc = sayi1 + sayi2
    elif islem == "cikarma":
        sonuc = sayi1 - sayi2
    elif islem == "carpma":
        sonuc = sayi1 * sayi2
    elif islem == "bolme":
        sonuc = "Hata: Sıfıra Bölme!" if sayi2 == 0 else sayi1 / sayi2
    elif islem == "us_alma":
        sonuc = sayi1 ** sayi2
    elif islem == "karekok":
        sonuc = math.sqrt(sayi1)
    elif islem == "yuzde":
        sonuc = (sayi1 * sayi2) / 100
    elif islem == "logaritma":
        sonuc = math.log(sayi1)
    elif islem == "sinus":
        sonuc = math.sin(math.radians(sayi1))
    elif islem == "cosinus":
        sonuc = math.cos(math.radians(sayi1))
    else:
        sonuc = "Geçersiz İşlem"

    return render_template("index.html", sonuc=sonuc, doviz_sonuc=None)

@app.route('/doviz', methods=['POST'])
def doviz():
    miktar = float(request.form['miktar'])
    birim = request.form['birim'].upper()

    api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(api_url)
    data = response.json()

    if "rates" in data and birim in data['rates']:
        kur = data['rates'][birim]
        tl_kuru = data['rates']["TRY"]
        sonuc = (miktar / kur) * tl_kuru
        doviz_sonuc = f"{miktar} {birim} = {sonuc:.2f} TL"
    else:
        doviz_sonuc = "Geçersiz para birimi."

    return render_template("index.html", sonuc=None, doviz_sonuc=doviz_sonuc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


