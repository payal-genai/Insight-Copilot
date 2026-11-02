from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Check API key
if not api_key:
    print("API Key not found!")
else:
    print("API Key loaded successfully!")

    # Initialize Groq LLM
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    # Send test message
    response = llm.invoke("Explain Generative AI in simple words.")

    print("\n--- GROQ RESPONSE ---")
    print(response.content)