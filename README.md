# GCP Model Integration

Enterprise LLM Gateway integration examples using Claude AI and Google Vertex AI.

## Project Overview

This project demonstrates multiple approaches for integrating Claude AI in enterprise environments:
- Direct Anthropic API connection
- Google Cloud Vertex AI integration
- Enterprise LLM Gateway (Kong) integration
- Command-line interface (CLI) access

## Setup

### Prerequisites
- Python 3.11+
- Google Cloud SDK (for Vertex AI integration)
- Access to LLM Gateway (optional)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment template:
   ```bash
   cp .env.template .env
   ```

4. Edit `.env` and fill in your credentials:
   - OAuth2 credentials (for LLM Gateway)
   - API endpoints
   - GCP project details

## Files

- **main.py** - Vertex AI integration example
- **claude_api.py** - LLM Gateway REST API client
- **anthropic_direct.py** - Direct Anthropic API connection
- **call_claude.sh** - Bash script for CLI access
- **.env.template** - Environment variables template
- **requirements.txt** - Python dependencies

## Usage

### Using LLM Gateway

```bash
python claude_api.py
```

### Using Vertex AI

```bash
python main.py
```

### Using Direct Anthropic API

```bash
export ANTHROPIC_API_KEY='your-api-key'
python anthropic_direct.py
```

### Using CLI Script

```bash
./call_claude.sh "Your question here"
```

## Security

⚠️ **Important:** Never commit `.env` file to version control. It contains sensitive credentials.

The `.env` file is:
- Excluded in `.gitignore`
- Set with restricted permissions (600 - owner read/write only)
- Should never be shared publicly

## Configuration

All sensitive configuration is stored in `.env`:

```bash
# OAuth2 Configuration
TOKEN_URL="https://your-federation-server.com/as/token.oauth2"
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"

# API Endpoints
API_URL="https://your-api-gateway.com/endpoint"
ENDPOINT_URL="https://your-api-gateway.com/endpoint"

# GCP Configuration
GCP_PROJECT_ID="your-project-id"
GCP_REGION="global"
```

## Documentation

See the tech articles for detailed guides:
- [LLM Gateway Integration](TECH_ARTICLE_LLM_Gateway.md)
- [Claude CLI Setup](TECH_ARTICLE_Claude_CLI_LLM_Gateway.md)

## License

Internal use only.
