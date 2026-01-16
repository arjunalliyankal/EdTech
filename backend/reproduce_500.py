import requests
import json

# Login to get token (assuming test user exists or we can mock auth)
# For simplicity, let's assume we can hit the endpoint if we had a token, 
# but auth might be tricky without a real user. 
# Alternatively, I can call the service function directly in python.

# Let's try calling the service function directly first to see if it crashes.
# If that works, then it's the API layer.

import asyncio
from app.services.roadmap_llm import roadmap_llm
from app.api.assessment import submit_assessment
# We can't easily call API function due to dependencies.

# Let's use requests with a dummy token or try to register a user first.
# actually, verified previously verify_roadmap.py worked.
# verify_roadmap.py called roadmap_llm.generate_roadmap directly.
# If verify_roadmap.py PASSES, then the crash is likely in the API layer code (mapping to Pydantic) or DB insert.

API_URL = "http://localhost:8000"

def verify_api_crash():
    # 1. Login/Signup
    # User might not exist, let's create random one
    import time
    timestamp = int(time.time())
    email = f"test_{timestamp}@example.com"
    print(f"Attempting to register: {email}")
    
    # Try Signup
    r = requests.post(f"{API_URL}/api/v1/auth/signup", json={"email": email, "password": "password", "role": "student"})
    if r.status_code == 200:
        print("Signup successful.")
        # Login just to be sure or use token from signup if returned (usually not)
        r = requests.post(f"{API_URL}/api/v1/auth/login", data={"username": email, "password": "password"})
    elif r.status_code == 400 and "already exists" in r.text:
         print("User exists, logging in.")
         r = requests.post(f"{API_URL}/api/v1/auth/login", data={"username": email, "password": "password"})
    else:
        print(f"Signup failed with unexpected error: {r.text}")
        
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        print("Could not get token.")
        return

    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Submit Assessment
    payload = {
        "answers": {"q1": "Answer 1", "q2": "Answer 2", "q3": "Answer 3"},
        "text_input": "I struggle with API."
    }
    
    print("Submitting assessment...")
    r = requests.post(f"{API_URL}/api/v1/assessment/submit", json=payload, headers=headers)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")

if __name__ == "__main__":
    verify_api_crash()
