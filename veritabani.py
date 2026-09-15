import sqlite3

# SQLite veri tabanına bağlan (dosya yoksa sistem otomatik oluşturur)
baglanti = sqlite3.connect("bilgi_bankasi.db")
imlec = baglanti.cursor()

# Metinleri ve sayısal vektörleri kaydedeceğimiz tabloyu oluştur
imlec.execute('''
    CREATE TABLE IF NOT EXISTS belgeler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metin TEXT,
        vektor TEXT
    )
''')
baglanti.commit()

print("Harika! SQLite veri tabanı başarıyla oluşturuldu.")