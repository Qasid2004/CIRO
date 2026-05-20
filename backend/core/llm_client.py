import time
from google import genai

API_KEYS = [
    "Add_your_own_API :)",   # Account 1
    "Add_your_own_API :)",  # Account 2
]

current_key_index = 0
client = genai.Client(api_key=API_KEYS[0])

def switch_key():
    global current_key_index, client
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    client = genai.Client(api_key=API_KEYS[current_key_index])
    print(f"🔄 Switched to API key {current_key_index + 1}")

def call_llm(prompt: str, system_prompt: str = "") -> str:
    global client
    for attempt in range(len(API_KEYS) * 3):
        try:
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            error_message = str(e)
            if "503" in error_message:
                time.sleep(3)
                continue
            elif "429" in error_message or "quota" in error_message.lower():
                print(f"⚠️  Key {current_key_index + 1} quota hit — switching...")
                switch_key()
                time.sleep(2)
                continue
            elif "403" in error_message or "api key" in error_message.lower():
                print(f"❌ Key {current_key_index + 1} invalid — switching...")
                switch_key()
                continue
            else:
                return f"ERROR_UNKNOWN: {error_message}"
    return "ERROR_UNKNOWN: All keys exhausted."

def test_connection():
    print("Testing connection...")
    result = call_llm("Reply with exactly: CIRO_ONLINE")
    if "CIRO_ONLINE" in result:
        print(f"✅ Connected on key {current_key_index + 1}. CIRO is ready.")
    else:
        print(f"⚠️  {result}")

if __name__ == "__main__":
    test_connection()