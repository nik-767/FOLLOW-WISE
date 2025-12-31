import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# We access the specific NVIDIA variable now
api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

def generate_email(prompt_context: str):
    if not api_key:
        return "Error: NVIDIA_API_KEY not found in .env"
        
    completion = client.chat.completions.create(
        model="meta/llama-3.1-405b-instruct",
        messages=[{"role": "user", "content": prompt_context}],
        temperature=0.7,
        max_tokens=500
    )
    return completion.choices[0].message.content
# Add this to the bottom of backend/app/ai/service.py
if __name__ == "__main__":
    print("Testing NVIDIA API...")
    try:
        response = generate_email("Write a hello world message")
        print("Success! AI replied:", response)
    except Exception as e:
        print("Error:", e)       