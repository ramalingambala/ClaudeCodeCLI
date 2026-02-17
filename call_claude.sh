#!/bin/bash

# Load environment variables from .env file
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found at $ENV_FILE"
  echo "Please copy .env.template to .env and fill in your credentials"
  exit 1
fi

# Source the environment variables
source "$ENV_FILE"

# Prompt can be passed as an argument, defaults to a sample question
PROMPT="${1:-What is the capitol of USA?}"

# Generate OAuth2 token
echo "Fetching access token..."
TOKEN_RESPONSE=$(curl --silent --location "$TOKEN_URL" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$ACCESS_TOKEN" ]; then
  echo "Error: Failed to retrieve access token."
  echo "Response: $TOKEN_RESPONSE"
  exit 1
fi

echo "Token acquired successfully."

# Call the Anthropic LLM endpoint with the token
curl --location "$API_URL" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --data "{
    \"messages\": [
        {
            \"role\": \"user\",
            \"content\": \"$PROMPT\"
        }
    ],
    \"model\": \"claude-sonnet-4-5\",
    \"max_tokens\": 4096
}"
echo ""
