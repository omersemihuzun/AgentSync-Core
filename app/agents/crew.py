from crewai import Crew, Process
from app.agents.agents import AgentSyncAgents
from app.agents.tasks import AgentSyncTasks

class AgentSyncCrew:
    def __init__(self, customer_name: str, image_description: str):
        """
        AgentSync Çoklu Ajan (Multi-Agent) Yapısı
        :param customer_name: Veritabanında aranacak müşteri adı (Örn: Hasan Kurnaz)
        :param image_description: Görüntü işlemeden (veya WhatsApp'tan) gelen fotoğraf betimlemesi
        """
        self.customer_name = customer_name
        self.image_description = image_description
        
    def run(self):
        agents = AgentSyncAgents()
        tasks = AgentSyncTasks()
        
        # 1. Ajanları Başlat
        vision_agent = agents.vision_agent()
        policy_agent = agents.policy_agent()
        fraud_agent = agents.fraud_agent()
        decision_agent = agents.decision_agent()
        
        # 2. Görevleri Tanımla ve Ajanlara Ata
        task1 = tasks.analyze_image_task(vision_agent, self.image_description)
        task2 = tasks.check_policy_task(policy_agent)
        task3 = tasks.analyze_fraud_task(fraud_agent, self.customer_name)
        task4 = tasks.final_decision_task(decision_agent)
        
        # 3. Ekibi Topla ve Sıralı (Sequential) Çalıştır
        crew = Crew(
            agents=[vision_agent, policy_agent, fraud_agent, decision_agent],
            tasks=[task1, task2, task3, task4],
            process=Process.sequential,
            verbose=True
        )
        
        # Görevi Başlat
        result = crew.kickoff()
        return result
