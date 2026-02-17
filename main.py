import os
from anthropic import AnthropicVertex
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Vertex AI client
client = AnthropicVertex(
    project_id=os.getenv("GCP_PROJECT_ID"),
    region=os.getenv("GCP_REGION", "global"),
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude. What is the news in AI world",
        }
    ],
    model="claude-opus-4-6",  # Vertex AI model name
)
print(message.content)
