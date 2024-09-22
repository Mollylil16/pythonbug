from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task(1)
    def load_homepage(self):
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(f"Homepage loading took too long: {response.elapsed.total_seconds()} seconds")

    @task(2)
    def update_points(self):
        data = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': 1}
        with self.client.post("/purchasePlaces", data=data, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(f"Updating points took too long: {response.elapsed.total_seconds()} seconds")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
