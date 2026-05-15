import os
import requests
import random
import time

API_URL = os.getenv("API_URL", "http://localhost:8000/api/iot/metrics")
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("Missing API_KEY environment variable")

while True:
    payload = {
        "device": "pico-lab-01",
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
    }

    headers = {
        "X-API-Key": API_KEY
    }

    response = requests.post(API_URL, json=payload, headers=headers, timeout=5)

    print("Sent:", payload)
    print("Status:", response.status_code)
    print("Response:", response.json())
    print("-" * 40)

    time.sleep(5)
