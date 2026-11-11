# Connecting to Enterprise LLM Gateway from CLI: A Journey with Claude AI

## Introduction

In enterprise environments, accessing Large Language Models (LLMs) isn't as straightforward as calling a public API. This article chronicles my journey setting up connectivity to an enterprise LLM gateway from a local development environment.

## The Goal

Connect to Claude AI models from a local development environment using Python, exploring multiple approaches:
1. Direct Anthropic API connection
2. Google Cloud Vertex AI integration
3. Enterprise LLM Gateway (the winning solution)

## Initial Setup: Installing the Claude SDK

The journey began with installing the Anthropic Python SDK:

```bash
pip install anthropic[vertex]
pip install google-cloud-aiplatform
```

This provided access to both direct Anthropic API and Google Vertex AI integration options.

## Approach 1: Direct Anthropic API Connection

### Initial Attempt

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

message = client.messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-3-5-sonnet-20241022",
)
```

### Challenge 1: Corporate SSL Proxy

**Error encountered:**
```
SSL: CERTIFICATE_VERIFY_FAILED - self-signed certificate in certificate chain
```

**Root cause:** Enterprise networks often use SSL inspection proxies that intercept HTTPS traffic with self-signed certificates.

**Solution:** Bypass SSL verification for development (not recommended for production):

```python
import httpx
from anthropic import Anthropic

http_client = httpx.Client(verify=False)
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    http_client=http_client
)
```

### Challenge 2: Invalid API Key

Even after resolving SSL issues, the authentication failed with a 401 error. This led to exploring alternative approaches.

## Approach 2: Google Cloud Vertex AI Integration

### Setup Process

1. **Installed Google Cloud SDK:**
```bash
brew install --cask google-cloud-sdk
```

2. **Authenticated with GCP:**
```bash
gcloud auth application-default login
gcloud config set project your-project-id
```

3. **Enabled Vertex AI API:**
```bash
gcloud services enable aiplatform.googleapis.com --project=your-project-id
```

### Implementation

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    project_id="your-project-id",
    region="global",
)

message = client.messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-6",
)
```

### Challenge 3: Model Access and Permissions

**Error encountered:**
```
403 Permission Denied: 'aiplatform.endpoints.predict' denied
404 Not Found: Model was not found or project does not have access
```

**Issues faced:**
- Claude models required explicit enablement in Vertex AI Model Garden
- Organization needed to accept terms of service for third-party models
- Model naming conventions differed between Anthropic API and Vertex AI
- IAM permissions needed proper Vertex AI roles

**Learning:** While Vertex AI integration eventually worked, it required significant administrative overhead and organizational approvals.

## Approach 3: Enterprise LLM Gateway (The Solution)

### Discovery

The breakthrough came when discovering the enterprise LLM Gateway endpoint, which provided:
- Pre-configured access to multiple LLM models
- Built-in authentication via OAuth2
- No need for individual API keys
- Centralized billing and governance

### Implementation

```python
import requests
import json

endpoint_url = "https://gateway.example.com/co/edap/anthropic/claude-4-5-sonnet-anthropic/eu1"

headers = {
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of USA?"
        }
    ],
    "model": "claude-sonnet-4-5",
    "max_tokens": 4096
}

response = requests.post(endpoint_url, headers=headers, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

### Success!

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "id": "msg_vrtx_01JnBU67LdSQki7tU7JGLRKU",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "The capital of the USA is **Washington, D.C.**"
    }
  ],
  "usage": {
    "input_tokens": 14,
    "output_tokens": 76
  }
}
```

## Bash Script for Command-Line Access

Created a reusable shell script for CLI access:

```bash
#!/bin/bash

TOKEN_URL="https://auth.example.com/as/token.oauth2"
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"
API_URL="https://gateway.example.com/co/edap/anthropic/claude-4-5-sonnet-anthropic/eu1"

PROMPT="${1:-What is the capitol of USA?}"

# Generate OAuth2 token
echo "Fetching access token..."
TOKEN_RESPONSE=$(curl --silent --location "$TOKEN_URL" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Call the LLM endpoint
curl --location "$API_URL" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --data "{
    \"messages\": [{\"role\": \"user\", \"content\": \"$PROMPT\"}],
    \"model\": \"claude-sonnet-4-5\",
    \"max_tokens\": 4096
}"
```

Usage:
```bash
./call_claude.sh "Explain quantum computing in simple terms"
```

## Advantages of Using an LLM Gateway

### 1. **Unified Access Management**
- Single authentication mechanism for multiple LLM providers
- Centralized user permissions and access control
- No need to manage individual API keys for each provider

### 2. **Cost Management & Governance**
- Centralized billing across organization
- Usage tracking and quota management
- Cost allocation by team or project
- Prevention of unauthorized spending

### 3. **Security & Compliance**
- Data residency controls (e.g., EU vs US endpoints)
- Audit logging of all LLM interactions
- PII detection and filtering
- Compliance with corporate security policies

### 4. **Simplified Integration**
- Consistent API interface across different LLM providers
- No vendor lock-in - easy to switch models
- Standard authentication (OAuth2) across all services
- Built-in rate limiting and retry logic

### 5. **Enterprise Support**
- Internal IT support for connectivity issues
- Pre-configured network access (no SSL certificate hassles)
- Approved for use within corporate environment
- SLA guarantees from internal teams

### 6. **Model Variety**
- Access to multiple models through single endpoint
- Easy A/B testing between models
- Fallback options if primary model unavailable

## Key Learnings

### 1. **SSL Certificate Challenges in Enterprise**
Corporate SSL inspection proxies are common and require either:
- Installing corporate CA certificates
- Disabling SSL verification (development only)
- Using pre-configured internal endpoints

### 2. **Model Naming Inconsistencies**
Model names vary between providers:
- Anthropic API: `claude-3-5-sonnet-20241022`
- Vertex AI: `claude-3-5-sonnet@20240620`
- LLM Gateway: `claude-sonnet-4-5`

Always check the specific gateway's documentation.

### 3. **Authentication Methods Matter**
Three different auth approaches encountered:
- Direct API: API keys in environment variables
- Vertex AI: Google Application Default Credentials
- LLM Gateway: OAuth2 client credentials flow

### 4. **Region Selection Is Critical**
- Vertex AI: Claude not available in all regions
- LLM Gateway: Different endpoints for EU vs US
- Data residency requirements may dictate endpoint choice

### 5. **Error 127 in CI/CD**
When running scripts in Azure DevOps or CI/CD pipelines, ensure dependencies like `jq` are installed:
```bash
sudo apt-get update && sudo apt-get install -y jq
```

## Troubleshooting Guide

### Issue: SSL Certificate Errors
```python
# Quick fix for development
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.post(url, json=data, verify=False)
```

### Issue: Permission Denied (403)
- Verify OAuth2 credentials are correct
- Check token expiration
- Ensure user has access to the LLM Gateway
- Contact IT for permission grants

### Issue: Model Not Found (404)
- Verify model name spelling
- Check if model is available in your region
- Confirm your organization has enabled the model

### Issue: Environment Variables Not Set
```bash
# Add to ~/.zshrc or ~/.bashrc
export ANTHROPIC_API_KEY='your-key'
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/creds.json'
```

## Project Structure

Final project structure:
```
GCPModelIntegration/
├── requirements.txt          # Python dependencies
├── main.py                   # Vertex AI integration
├── gsk_claude_api.py        # LLM Gateway client
├── anthropic_direct.py      # Direct Anthropic API
├── call_claude.sh           # Bash wrapper for CLI
├── azure-pipelines.yml      # CI/CD configuration
└── README.md               # Documentation
```

## Conclusion

While multiple approaches exist for accessing LLMs in enterprise environments, an LLM Gateway provides the most seamless experience by abstracting away authentication complexities, SSL certificate issues, and model-specific details.

The key takeaways:
- **Start simple**: Try the enterprise gateway first before complex integrations
- **Security matters**: Corporate networks require special SSL handling
- **Documentation is key**: Model names and endpoints vary significantly
- **Governance wins**: Centralized access management simplifies scaling

The time invested in understanding these different approaches paid off in creating robust, maintainable code that works reliably in enterprise environments.

## Resources

- [Anthropic API Documentation](https://docs.anthropic.com)
- [Google Vertex AI Claude Setup](https://cloud.google.com/vertex-ai/docs/generative-ai/model-garden/claude)
- [OAuth2 Client Credentials Flow](https://oauth.net/2/grant-types/client-credentials/)

---

*Published: February 2026*
*Author: Enterprise AI Integration Team*

