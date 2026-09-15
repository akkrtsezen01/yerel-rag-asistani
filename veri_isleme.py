from openai import OpenAI
import sqlite3
import json

# 1. YEREL SUNUCUYA BAĞLANTI
# İşlemlerin buluta gitmemesi için kendi bilgisayarımızdaki yerel porta bağlanıyoruz.
client = OpenAI(base_url="http://127.0.0.1:63672/v1", api_key="foundry-local")

print("Belge okunuyor ve parçalara ayrılıyor...")

# 2. BELGEYİ OKUMA VE PARÇALAMA
# 'belge.txt' dosyasını okuyup, yapay zekanın daha iyi anlaması için paragraflara bölüyoruz.
with open("belge.txt", "r", encoding="utf-8") as dosya:
    icerik = dosya.read()
parcalar = icerik.split("\n\n")

# 3. VERİ TABANI BAĞLANTISI
# Sunucusuz, yerel ve hafif bir çözüm olan SQLite veri tabanımızı oluşturup bağlanıyoruz.
baglanti = sqlite3.connect("bilgi_bankasi.db")
imlec = baglanti.cursor()

# Tablomuz yoksa oluşturuyoruz (Geliştirme aşamasında veritabani.py ile yapmıştık, buraya entegre ettik).
imlec.execute('''
    CREATE TABLE IF NOT EXISTS belgeler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metin TEXT,
        vektor TEXT
    )
''')

print("Vektörler hesaplanıp veri tabanına kaydediliyor. Lütfen bekleyin...")

# 4. VEKTÖRLEŞTİRME (EMBEDDING) VE KAYIT
for parca in parcalar:
    if parca.strip() == "": 
        continue
        
    # Her bir metin parçası için anlamsal bir sayısal vektör hesaplatıyoruz.
    response = client.embeddings.create(
        input=parca,
        model="qwen3-embedding-0.6b"
    )
    vektor = response.data[0].embedding
    
    # Vektörü SQLite'a kaydedebilmek için metin formatına (JSON) çeviriyoruz.
    vektor_json = json.dumps(vektor)
    
    # Metni ve sayısal temsilini veri tabanına kaydediyoruz.
    imlec.execute("INSERT INTO belgeler (metin, vektor) VALUES (?, ?)", (parca, vektor_json))

# İşlemleri kaydedip veri tabanını güvenlice kapatıyoruz.
baglanti.commit()
baglanti.close()

print("Harika! Tüm veriler başarıyla vektörleştirilip veri tabanına kaydedildi!")