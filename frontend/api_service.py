import requests

def analyze_crisis(user_input: str) -> dict:
    try:
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"user_input": user_input},
            timeout=60
        )
        return response.json()
    except Exception as e:
        raise Exception(f"Backend error: {e}")