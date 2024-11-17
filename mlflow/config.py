try:
    import _scproxy
    proxies = _scproxy._get_proxies()
    _scproxy._get_proxy_settings = lambda: proxies
    proxy_settings = _scproxy._get_proxy_settings()
    _scproxy._get_proxy_settings = lambda: proxy_settings
except ImportError:
    pass

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# MLflow configurations
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "default")

# Slack configurations
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    raise ValueError("SLACK_WEBHOOK_URL is not set in the environment.")