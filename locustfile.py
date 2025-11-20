from locust import HttpUser, task, between

class TrackingUser(HttpUser):
  wait_time = between(0.1, 1.0)

  @task(3)
  def track_valid_tag(self):
    # hit valid tags
    self.client.get("/t/facebook-test")

  @task(1)
  def track_valid_tag(self):
    # hit invalid tags
    self.client.get("/t/invalidtag-test")

  @task(1)
  def check_health(self):
    #ocassionally check health endpoint
    self.client.get("/health")
