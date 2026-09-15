# Yerel RAG Projesi (İnternetsiz Soru-Cevap Asistanı)

## Projenin Amacı ve Çalışma Mantığı
Bu projeyi, 1 aylık bilgisayar bilimleri yaz okulu kapsamında geliştirdim[cite: 1]. Amacım, internet bağlantısına ihtiyaç duymadan kendi bilgisayarımda çalışan bir yapay zeka asistanı yapmaktı[cite: 1]. Normal modeller bazen bilmedikleri konularda mantıklı görünen yalanlar uydurabiliyor (halüsinasyon)[cite: 1]. Bunun önüne geçmek için RAG (Retrieval-Augmented Generation) sistemini kurdum ve asistanın sadece benim verdiğim dosyalardan cevap üretmesini sağladım[cite: 1].

Sistemim 3 temel adımda çalışıyor:
* **Verilerin Hazırlanması:** `belge.txt` içindeki notlarımı `qwen3-embedding-0.6b` modelini kullanarak sayısal vektörlere çevirdim ve yerel bir SQLite veri tabanına kaydettim[cite: 1].
* **Arama ve Filtreleme:** Kullanıcı bir soru sorduğunda, soruyu da vektöre çevirip veri tabanında kosinüs benzerliği ile aratıyorum[cite: 1]. Geliştirme aşamasında modelin alakasız sorularda (örneğin "Mars'a nasıl gidilir?") kafasının karıştığını fark ettim[cite: 1]. Çözüm olarak kod seviyesinde bir eşik belirledim: Benzerlik skoru 0.3'ün altındaysa yapay zekayı hiç uyandırmadan "Bu bilgiye sahip değilim." çıktısını verdiriyorum[cite: 1].
* **Cevap Üretimi:** Eğer alakalı bir bilgi bulunursa, bu metni yerel olarak çalışan `phi-3.5-mini` modeline gönderiyorum ve sadece benim belgelerime dayanan Türkçe bir cevap alıyorum[cite: 1].

## Kullanılan Araçlar
* Python 3.10 ve Visual Studio Code[cite: 1]
* Microsoft Foundry Local SDK (Modelleri yerel çalıştırmak için)[cite: 1]
* SQLite (Sunucusuz yerel veri tabanı)[cite: 1]

## Kurulum Adımları
Benim sistemimi kendi cihazınızda web arayüzü ile denemek isterseniz şu adımları izleyebilirsiniz:
1. Terminalden gerekli paketleri indirin: `pip install foundry-local-sdk streamlit`
2. `belge.txt` dosyasını kendi notlarınızla doldurup veri tabanını oluşturun: `python veri_isleme.py`
3. İnterneti kapatın ve web arayüzünü başlatmak için şu komutu çalıştırın: `streamlit run main.py`