

from app import create_app


def test_metrics_counter_increments_after_tracking(monkeypatch):
  monkeypatch.setenv("METRICS_TOKEN", "secret123")
  monkeypatch.setenv("TARGET_URL", "https://example.com")

  app = create_app()
  app.config["TESTING"] = True
  client = app.test_client()

  response = client.get("/t/facebook")
  assert response.status_code == 302

  metrics_response = client.get("/metrics?token=secret123")
  assert metrics_response.status_code == 200

  body = metrics_response.data.decode("utf-8")
  assert 'qr_clicks_total{tag="facebook"}' in body, "Expected facebook tag to appear in metrics"

def test_metrics_counter_increments_after_false_tag(monkeypatch):
  monkeypatch.setenv("METRICS_TOKEN", "secret123")
  monkeypatch.setenv("TARGET_URL", "https://example.com")

  app = create_app()
  app.config["TESTING"] = True
  client = app.test_client()

  response = client.get("/t/something-invalid")
  assert response.status_code == 302

  metrics_response = client.get("metrics?token=secret123")
  assert metrics_response.status_code == 200

  body = metrics_response.data.decode("utf-8")
  assert 'qr_clicks_total{tag="something_invalid"}' not in body, "did not expect tag to appear in metrics"



