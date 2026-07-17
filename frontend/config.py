# frontend/config.py

import os

# When deployed to Streamlit Cloud — no backend available
# When running locally — use FastAPI backend
API_BASE = os.environ.get(
    "API_BASE",
    "http://localhost:8000/api"
)

# Set this to True for Streamlit Cloud deployment
STANDALONE_MODE = os.environ.get(
    "STANDALONE_MODE", "false"
).lower() == "true"