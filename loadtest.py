from locust import HttpUser, task, constant

class MyUser(HttpUser):
    wait_time = constant(0.001)  # Adjusted to send 1000 requests per second

    @task
    def get_hits(self):
        query_params = {
            "q": "Facebook",
            "w": 0.5  # Adjust the weight parameter as needed
        }
        self.client.get("", params=query_params)
