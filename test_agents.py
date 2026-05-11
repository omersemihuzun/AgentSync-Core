import os
import sys

# Proje kök dizinini yola ekle ki app modülleri çalışsın
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Eğer API key yoksa test çalışmasın
if not os.getenv("GEMINI_API_KEY"):
    print("HATA: GEMINI_API_KEY .env dosyasında bulunamadı. Lütfen ekleyin.")
    sys.exit(1)

from app.agents.crew import AgentSyncCrew

def run_tests():
    print("="*60)
    print("🧠 AGENTSYNC AI - YAPAY ZEKA TEST SENARYOLARI".center(60))
    print("="*60)

    print("\n[SENARYO 1: SUİSTİMALCİ MÜŞTERİ (Hasan Kurnaz)]")
    print("Açıklama: Ürün gerçekten yırtık ama müşterinin geçmişte 3 iadesi daha var.")
    print("Beklenen Karar: MANUAL REVIEW (Patron Onaylamalı)")
    print("-" * 40)
    crew1 = AgentSyncCrew(
        customer_name="Hasan Kurnaz",
        image_description="Mavi gömleğin sol kolunda belirgin bir yırtık var. Etiketi üzerinde duruyor."
    )
    result1 = crew1.run()
    print("\n>>> SENARYO 1 NİHAİ ÇIKTI:")
    print(result1)
    print("="*60)

    print("\n[SENARYO 2: KURAL İHLALİ (Ayşe Yılmaz)]")
    print("Açıklama: Ürün sapasağlam ama etiketi koparılmış.")
    print("Beklenen Karar: REJECT (Kurallara Aykırı)")
    print("-" * 40)
    crew2 = AgentSyncCrew(
        customer_name="Ayşe Yılmaz",
        image_description="Ürün sapasağlam görünüyor ancak üzerindeki orijinal marka etiketi ve barkodu koparılmış."
    )
    result2 = crew2.run()
    print("\n>>> SENARYO 2 NİHAİ ÇIKTI:")
    print(result2)
    print("="*60)

    print("\n[SENARYO 3: SORUNSUZ HAKLI İADE (Mehmet Dürüst)]")
    print("Açıklama: Kargoda cam kırılmış, ürün hasarlı, müşteri geçmişi temiz.")
    print("Beklenen Karar: APPROVE (Anında Onay)")
    print("-" * 40)
    crew3 = AgentSyncCrew(
        customer_name="Mehmet Dürüst",
        image_description="Cam fanus kargoda tamamen ezilmiş ve kırık parçalar var. Marka etiketi kutunun içinde duruyor."
    )
    result3 = crew3.run()
    print("\n>>> SENARYO 3 NİHAİ ÇIKTI:")
    print(result3)
    print("="*60)

if __name__ == "__main__":
    run_tests()
