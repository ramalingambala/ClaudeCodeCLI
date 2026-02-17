import os
from anthropic import Anthropic

# Initialize Anthropic client with API key
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Create a message
message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude! Can you tell me about yourself?",
        }
    ],
    model="claude-3-5-sonnet-20241022",
)

# Print the response
print(message.content[0].text)
