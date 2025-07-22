import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
