from locust import HttpUser, TaskSet, task, between

class WebsiteTasks(TaskSet):

    @task(1)
    def load_home_page(self):
        """
        Test the loading of the home page.
        The response time should be under 5 seconds.
        """
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(f"Home page took too long to load: {response.elapsed.total_seconds()} seconds")
            else:
                response.success()

    @task(2)
    def update_points(self):
        """
        Simulate updating points, the response time should be under 2 seconds.
        """
        with self.client.post("/updatePoints", json={"club": "Some Club", "points": 10}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(f"Updating points took too long: {response.elapsed.total_seconds()} seconds")
            else:
                response.success()


class WebsiteUser(HttpUser):
    tasks = [WebsiteTasks]
    wait_time = between(1, 5)  # Simulate users waiting between 1 and 5 seconds before next action
