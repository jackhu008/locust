import time
from locust import HttpUser, task, between
 
class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    @task
    def index_page(self):
        self.client.get("/")

    @task
    def greeting_page(self):
        self.client.get("/hello")
        self.client.get("/hello/Hero")

    @task
    def quote_page(self):
        self.client.get("/quote")
