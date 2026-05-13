import sys
import os
import streamlit as st
from dotenv import load_dotenv

# PYTHONPATH=/app docker-compose'da tanımlı; bu satır yerel çalıştırma için fallback
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.agents.crew import AgentSyncCrew

# Sayfa Yapılandırması (Senior UI/UX)
st.set_page_config(
    page_title="AgentSync AI | Yönetici Paneli",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ortam değişkenlerini yükle
load_dotenv()

def main():
    st.title("🤖 AgentSync AI - Otonom KOBİ Yönetimi")
    st.markdown("Bu panel, **Yapay Zeka Ajanlarının (CrewAI)** müşteri taleplerini nasıl analiz ettiğini canlı olarak sergiler.")

    # Sol Menü (Sidebar) - Senaryo Seçimi
    with st.sidebar:
        st.header("📋 Demo Senaryoları")
        st.info("Jüriye sunum yaparken aşağıdaki hazır test kurgularını kullanabilirsiniz.")
        
        scenario = st.radio(
            "Bir Senaryo Seçin:",
            ("1. Suistimalci Müşteri (Yüksek Risk)", 
             "2. Kural İhlali (Etiketsiz Ürün)", 
             "3. Sorunsuz İade (Hızlı Onay)",
             "4. Özel Test (Kendin Yaz)")
        )

    # Senaryo Değişkenleri
    customer_name = ""
    image_desc = ""

    if scenario.startswith("1"):
        customer_name = "Hasan Kurnaz"
        image_desc = "Mavi gömleğin sol kolunda belirgin bir yırtık var. Etiketi üzerinde duruyor."
        st.warning(f"**Seçilen Kurgu:** Ürün yırtık (Kurala uygun) ancak '{customer_name}' isimli müşterinin veritabanında çok sayıda geçmiş iadesi var. Ajanların bunu fark etmesi bekleniyor.")
    elif scenario.startswith("2"):
        customer_name = "Ayşe Yılmaz"
        image_desc = "Ürün sapasağlam görünüyor ancak üzerindeki orijinal marka etiketi ve barkodu koparılmış."
        st.error(f"**Seçilen Kurgu:** '{customer_name}' temiz bir müşteri ancak etiket koparılmış. Kural ajanının iadeyi anında reddetmesi bekleniyor.")
    elif scenario.startswith("3"):
        customer_name = "Mehmet Dürüst"
        image_desc = "Cam fanus kargoda tamamen ezilmiş ve kırık parçalar var. Marka etiketi kutunun içinde duruyor."
        st.success(f"**Seçilen Kurgu:** '{customer_name}' temiz bir müşteri ve kargo hasarı bariz. Otonom anında onay bekleniyor.")
    else:
        customer_name = st.text_input("Müşteri Adı (Veritabanında olmalı):", value="Hasan Kurnaz")
        image_desc = st.text_area("Görsel Betimlemesi (WhatsApp'tan gelen):", value="Ürün lekeli.")

    st.divider()

    # Aksiyon Bölümü
    if st.button("🚀 Yapay Zeka Ajanlarını Başlat (CrewAI Run)", type="primary"):
        if not os.getenv("GEMINI_API_KEY"):
            st.error("HATA: .env dosyasında GEMINI_API_KEY bulunamadı!")
            return

        with st.status("Ajanlar çalışıyor, lütfen bekleyin...", expanded=True) as status:
            st.write("🕵️‍♂️ **Vision Agent** fotoğrafı inceliyor...")
            st.write("📜 **Policy Agent** iade kurallarını denetliyor...")
            st.write("🛡️ **Fraud Agent** veritabanından müşteri geçmişini sorguluyor...")
            st.write("⚖️ **Decision Agent** nihai kararı veriyor...")
            
            try:
                # Backend Logic Çağrısı (Spagetti kodu önler, temiz mimari)
                crew = AgentSyncCrew(customer_name=customer_name, image_description=image_desc)
                result = crew.run()
                
                status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)
                
                st.subheader("🎯 Ajanların Ortak Kararı (Nihai Çıktı)")
                st.info(result)
                
            except Exception as e:
                status.update(label="Bir hata oluştu!", state="error")
                st.error(f"Sistem Hatası: {str(e)}")

if __name__ == "__main__":
    main()
