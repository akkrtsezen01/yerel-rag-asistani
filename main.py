import streamlit as st
from openai import OpenAI
import sqlite3
import json
import math

# Kosinüs Benzerliği Fonksiyonu
def kosinus_benzerligi(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (magnitude1 * magnitude2)

# Web Arayüzü (UI) Tasarımı
st.set_page_config(page_title="Endüstriyel Simülatör", page_icon="⚙️", layout="wide")
st.title("⚙️ Endüstriyel Senaryo Simülatörü (Yerel RAG)")
st.markdown("Üretim hattı veya tedarik zinciri kriz senaryonuzu girin, sistem veri tabanındaki kurallara göre etki analizi yapsın.")

senaryo = st.text_area("Kriz Senaryosunu Buraya Yazın:", height=100)

if st.button("Senaryoyu Analiz Et"):
    if senaryo:
        with st.spinner("Sistem kuralları taranıyor ve simülasyon çalıştırılıyor..."):
            
            client = OpenAI(base_url="http://127.0.0.1:63672/v1", api_key="foundry-local")

            # Senaryoyu vektörleştirme
            cevap_vektor = client.embeddings.create(input=senaryo, model="qwen3-embedding-0.6b")
            soru_vektoru = cevap_vektor.data[0].embedding

            # Veri tabanında kural arama
            baglanti = sqlite3.connect("bilgi_bankasi.db")
            imlec = baglanti.cursor()
            imlec.execute("SELECT metin, vektor FROM belgeler")
            kayitlar = imlec.fetchall()

            en_iyi_metin = ""
            en_yuksek_skor = -1

            for kayit in kayitlar:
                metin = kayit[0]
                vektor = json.loads(kayit[1])
                skor = kosinus_benzerligi(soru_vektoru, vektor)
                
                if skor > en_yuksek_skor:
                    en_yuksek_skor = skor
                    en_iyi_metin = metin
                    
            baglanti.close()

            # Analiz ve Cevap Üretimi
            if en_yuksek_skor < 0.3:
                st.warning("Girdiğiniz senaryo parametreleri fabrika veri tabanında tanımlı değildir. Lütfen geçerli bir durum girin.")
            else:
                sistem_mesaji = f"""Sen bir Endüstri Mühendisliği Sistem Analistisin. 

SİSTEM KURALLARI: '{en_iyi_metin}'

GÖREVİN: Kullanıcının girdiği kriz senaryosunu SADECE yukarıdaki sistem kurallarına dayanarak 3 adımda analiz et:
1. Darboğaz / Kök Neden Tespiti
2. Üretime ve Maliyete Etki Tahmini
3. Kurallara Dayalı Eylem Planı (Optimizasyon)

Kurallarda geçmeyen hiçbir bilgiyi veya sayıyı uydurma. Eğer senaryo kurallarla örtüşmüyorsa 'Bu durum kurallarda tanımlanmamıştır' de."""
                
                response = client.chat.completions.create(
                    model="phi-3.5-mini",
                    messages=[
                        {"role": "system", "content": sistem_mesaji},
                        {"role": "user", "content": senaryo}
                    ],
                    temperature=0.1,
                    frequency_penalty=0.8,
                    max_tokens=500
                )
                
                st.success("Simülasyon Tamamlandı!")
                st.markdown(response.choices[0].message.content)
                
                with st.expander("Tetiklenen Sistem Kurallarını Gör"):
                    st.info(en_iyi_metin)
    else:
        st.error("Lütfen analiz edilecek bir senaryo girin!")