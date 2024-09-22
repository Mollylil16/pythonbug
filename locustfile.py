from locust import HttpUser, task, between

class PerformanceTest(HttpUser):
    wait_time = between(1, 2)  # Temps d'attente entre les requêtes

    @task
    def load_homepage(self):
        self.client.get("/")  # Test de la page d'accueil

    @task
    def load_competition(self):
        self.client.get("/showSummary")  # Test de la page de résumé
