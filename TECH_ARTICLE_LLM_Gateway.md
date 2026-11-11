# Connecting Claude Code CLI to Enterprise LLM Gateway: A Practical Guide

## Introduction

As enterprises adopt AI-powered development tools, integrating them with centralized LLM gateways becomes crucial for governance, security, and cost management. This article chronicles my experience connecting Claude Code CLI to a secure enterprise gateway.

## What is Claude Code CLI?

Claude Code CLI is a command-line interface that brings AI-powered coding assistance directly to your terminal. It allows developers to:
- Generate code snippets and entire functions
- Debug and refactor existing code
- Get explanations for complex code
- Create projects from natural language descriptions
- Automate repetitive coding tasks

## What is an LLM Gateway?

An LLM Gateway (like Kong-based solutions) acts as a reverse proxy for LLM APIs, providing:
- **Unified API interface** across multiple LLM providers
- **Authentication & authorization** with fine-grained IAM controls
- **Rate limiting & quota management** per user/team
- **Request/response logging** for audit trails
- **Cost tracking & billing** across organization
- **Model routing** based on policies or load

## Why Connect Claude CLI to LLM Gateway?

Instead of connecting Claude CLI directly to Anthropic's API, routing through an LLM Gateway offers:

1. **Centralized governance** - IT controls access, models, and spending
2. **Cost attribution** - Track usage by team or project
3. **Vendor flexibility** - Switch between OpenAI, Anthropic, or open-source models
4. **Security compliance** - Data stays within corporate boundaries
5. **Enhanced monitoring** - Real-time usage analytics and anomaly detection

## Setup Guide

### Prerequisites

- macOS, Linux, WSL, or Windows system
- Terminal access
- LLM Gateway account with API key
- Network access to LLM Gateway endpoint

### Step 1: Install Claude Code CLI

The installation varies by operating system:

**For macOS, Linux, or WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**For Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**For Windows CMD:**
```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Alternative for macOS (if bash script is blocked):**
```bash
brew install claude-cli
```

> **Note:** In enterprise environments with strict security policies, bash script execution might be blocked. Using Homebrew or requesting IT to whitelist the installation script are common workarounds.

### Step 2: Verify Installation

Confirm Claude CLI is properly installed:

```bash
# Check version
claude --version

# Run diagnostic
claude doctor
```

Expected output:
```
Claude CLI v1.x.x
✓ Installation verified
✓ Auto-update enabled
✓ All systems operational
```

> **Pro tip:** Native installs include auto-update functionality, ensuring you always have the latest features and security patches.

### Step 3: Configure LLM Gateway Connection

This is where the magic happens - redirecting Claude CLI to use your enterprise LLM Gateway instead of Anthropic's public API.

#### Set the Gateway Endpoint

```bash
export ANTHROPIC_BASE_URL="https://api.llmgateway.io"
```

Replace with your actual gateway endpoint:
- **Production:** `https://api.llmgateway.io`
- **Development:** `https://gateway.example.com/anthropic`
- **Local LiteLLM:** `http://0.0.0.0:4000`

#### Set Authentication Token

```bash
export ANTHROPIC_AUTH_TOKEN="llmgtwy_YourAPIKeyHere"
```

This is your LLM Gateway API key, NOT an Anthropic API key.

#### (Optional) Specify Model

```bash
export ANTHROPIC_MODEL="glm-4.5-flash"
```

Common model options:
- `glm-4.5-flash` - Open-source, fast responses
- `claude-sonnet-4-5-20250929` - Anthropic's latest
- `gpt-4` - OpenAI's flagship model
- Leave unset to use gateway's default

### Step 4: Obtain LLM Gateway API Key

#### Access the Dashboard

1. Navigate to your LLM Gateway dashboard: `https://dashboard.llmgateway.io`
2. Log in with your enterprise credentials
3. Go to **Keys Section** in the sidebar

#### Generate API Key

1. Click **"Create New Key"**
2. Give it a descriptive name: `claude-cli-dev` or `yourname-workstation`
3. Set permissions and restrictions:
    - **Models allowed:** `glm-4.5-flash`, `claude-sonnet-4-5`
    - **Rate limits:** 100 requests/minute
    - **Budget cap:** $50/month
4. Click **"Generate"** and copy the key

#### Configure IAM Rules (Optional but Recommended)

Fine-grained access control via IAM:

```json
{
  "user": "user.name@company.com",
  "allowed_models": ["glm-4.5-flash", "claude-sonnet-4-5"],
  "rate_limit": {
    "requests_per_minute": 100,
    "tokens_per_day": 1000000
  },
  "budget": {
    "monthly_limit_usd": 50,
    "alert_threshold": 0.8
  },
  "allowed_ip_ranges": ["10.0.0.0/8"],
  "data_residency": "eu-west-1"
}
```

### Step 5: Create a Test Project

Test the integration with a simple project:

```bash
# Create project directory
mkdir claude-gateway-test
cd claude-gateway-test

# Initialize Claude
claude
```

Claude will start in interactive mode, ready to accept your prompts.

#### Using Specific Models

For one-off model selection:

```bash
claude --model glm-4.5-flash
```

Or for specific tasks:

```bash
claude --model claude-sonnet-4-5 "Create a REST API for user management"
```

### Step 6: Invoke LLM Through Gateway

Now the exciting part - using Claude CLI with your enterprise LLM Gateway!

#### Example 1: Code Generation

```bash
claude "Create a Python function to validate email addresses with regex"
```

**Response (via GLM-4.5-Flash through gateway):**
```python
import re

def validate_email(email: str) -> bool:
    """
    Validate email address using regex pattern.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Test examples
print(validate_email("user@example.com"))  # True
print(validate_email("invalid.email"))      # False
```

#### Example 2: Code Refactoring

```bash
claude "Refactor this code to use type hints and add error handling" < old_code.py
```

#### Example 3: Project Scaffolding

```bash
claude "Create a FastAPI project structure with authentication, database models, and API routes"
```

Claude will generate:
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── database.py
│   └── dependencies.py
├── requirements.txt
└── README.md
```

#### Example 4: Debugging Assistance

```bash
claude "Explain why this code throws a KeyError" < buggy_script.py
```

### Step 7: Make Configuration Persistent

To avoid setting environment variables every time, add them to your shell profile:

**For Zsh (macOS default):**

```bash
# Edit profile
nano ~/.zshrc

# Add these lines
export ANTHROPIC_BASE_URL="https://api.llmgateway.io"
export ANTHROPIC_AUTH_TOKEN="llmgtwy_YourAPIKeyHere"
export ANTHROPIC_MODEL="glm-4.5-flash"

# Save and reload
source ~/.zshrc
```

**For Bash:**

```bash
# Edit profile
nano ~/.bashrc

# Add the same exports
# Save and reload
source ~/.bashrc
```

**For Windows PowerShell:**

```powershell
# Edit profile
notepad $PROFILE

# Add:
$env:ANTHROPIC_BASE_URL = "https://api.llmgateway.io"
$env:ANTHROPIC_AUTH_TOKEN = "llmgtwy_YourAPIKeyHere"
$env:ANTHROPIC_MODEL = "glm-4.5-flash"
```

#### Using Profiles for Multiple Environments

Create separate profiles for different contexts:

**~/.claude-profiles/dev.sh:**
```bash
export ANTHROPIC_BASE_URL="https://dev-gateway.company.com"
export ANTHROPIC_AUTH_TOKEN="llmgtwy_dev_key"
export ANTHROPIC_MODEL="glm-4.5-flash"
```

**~/.claude-profiles/prod.sh:**
```bash
export ANTHROPIC_BASE_URL="https://prod-gateway.company.com"
export ANTHROPIC_AUTH_TOKEN="llmgtwy_prod_key"
export ANTHROPIC_MODEL="claude-sonnet-4-5"
```

Switch between profiles:
```bash
source ~/.claude-profiles/dev.sh
claude "Generate test data"

source ~/.claude-profiles/prod.sh
claude "Optimize production database query"
```

## Key Challenges Encountered

### Challenge 1: Network Connectivity Issues

**Problem:** Claude CLI couldn't reach the LLM Gateway endpoint.

**Symptoms:**
```
Error: Failed to connect to https://api.llmgateway.io
Connection timeout after 30s
```

**Root Causes:**
- Corporate firewall blocking the gateway domain
- VPN required but not connected
- Incorrect endpoint URL

**Solutions:**
1. Verify endpoint URL with `curl`:
   ```bash
   curl -I https://api.llmgateway.io/health
   ```

2. Check network connectivity:
   ```bash
   ping api.llmgateway.io
   traceroute api.llmgateway.io
   ```

3. Contact IT to whitelist the gateway domain

4. Connect to corporate VPN if required

### Challenge 2: Authentication Failures

**Problem:** 401 Unauthorized or 403 Forbidden errors.

**Symptoms:**
```
Error: Authentication failed
Status: 401 Unauthorized
Message: Invalid or expired API key
```

**Common Mistakes:**
- Using Anthropic API key instead of gateway key
- Typo in the API key
- Key expired or revoked
- Missing `ANTHROPIC_AUTH_TOKEN` prefix

**Solutions:**
1. Regenerate key from gateway dashboard
2. Verify key format: `llmgtwy_xxx` (not `sk-ant-xxx`)
3. Check key hasn't expired
4. Ensure proper environment variable:
   ```bash
   echo $ANTHROPIC_AUTH_TOKEN  # Should show key
   ```

### Challenge 3: Model Not Available

**Problem:** Requested model not accessible through gateway.

**Symptoms:**
```
Error: Model 'claude-4' not found
Available models: glm-4.5-flash, claude-sonnet-4-5-20250929
```

**Root Causes:**
- Model not enabled in gateway configuration
- Typo in model name
- IAM policy restricts access to specific models

**Solutions:**
1. List available models:
   ```bash
   curl -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
        https://api.llmgateway.io/v1/models
   ```

2. Check gateway dashboard for enabled models

3. Request access from admin if model needed

4. Use correct model naming convention:
    - ✅ `glm-4.5-flash`
    - ❌ `glm4.5flash`

### Challenge 4: Rate Limiting

**Problem:** Hitting rate limits during intensive development.

**Symptoms:**
```
Error: Rate limit exceeded
Retry after: 60 seconds
Quota: 100 requests/minute
```

**Solutions:**
1. Check your current quota in dashboard

2. Implement request throttling:
   ```bash
   # Add delay between requests
   for prompt in prompts.txt; do
     claude "$prompt"
     sleep 2
   done
   ```

3. Request quota increase from admin

4. Use lower-cost models for experimentation

### Challenge 5: SSL Certificate Issues

**Problem:** Corporate SSL inspection breaking HTTPS connections.

**Symptoms:**
```
Error: SSL certificate verification failed
CERTIFICATE_VERIFY_FAILED: self-signed cert in chain
```

**Solutions:**
1. Install corporate CA certificate:
   ```bash
   export SSL_CERT_FILE=/path/to/corporate-ca.pem
   export REQUESTS_CA_BUNDLE=/path/to/corporate-ca.pem
   ```

2. For development only, disable verification (not recommended):
   ```bash
   export NODE_TLS_REJECT_UNAUTHORIZED=0
   ```

3. Contact IT for proper certificate installation

### Challenge 6: Environment Variable Conflicts

**Problem:** Multiple AI tools using same environment variables.

**Symptoms:**
- Claude CLI using wrong endpoint
- Conflicting API keys from different tools
- Unexpected model being called

**Solutions:**
1. Use tool-specific variables:
   ```bash
   # Instead of generic OPENAI_API_KEY
   export CLAUDE_CLI_API_KEY="..."
   export COPILOT_API_KEY="..."
   ```

2. Create isolated profiles per tool

3. Use direnv for project-specific environment:
   ```bash
   # .envrc in project root
   export ANTHROPIC_BASE_URL="https://api.llmgateway.io"
   export ANTHROPIC_AUTH_TOKEN="project_specific_key"
   ```

## Key Learnings

### 1. Gateway Configuration is Critical

The success of this integration hinges on proper gateway configuration:

- **Endpoint URLs must be exact** - trailing slashes matter
- **API keys follow gateway format**, not original provider
- **Model names differ** between direct API and gateway

**Best Practice:** Document your gateway's specific requirements in a team wiki.

### 2. Environment Variables Drive Behavior

Claude CLI respects environment variables in this priority:
1. Command-line flags (`--model`)
2. Environment variables (`ANTHROPIC_MODEL`)
3. Config file (`~/.claude/config.yaml`)
4. Gateway defaults

**Best Practice:** Use environment variables for flexibility, command flags for one-offs.

### 3. Open-Source Models Perform Well

GLM-4.5-Flash surprised me with:
- **Fast response times** (2-3 seconds average)
- **Good code quality** for common tasks
- **Lower cost** compared to proprietary models

**Use Case Recommendation:**
- **GLM-4.5-Flash:** Quick code snippets, syntax help, simple refactoring
- **Claude Sonnet:** Complex architecture, detailed explanations, production code

### 4. IAM Policies Prevent Accidents

Fine-grained access control saved us from:
- Accidental high-cost model usage
- Quota exhaustion by runaway scripts
- Unauthorized access to sensitive models

**Best Practice:** Start restrictive, loosen as needed.

### 5. Monitoring Reveals Patterns

LLM Gateway analytics showed:
- **Peak usage hours:** 9-11 AM, 2-4 PM
- **Most used models:** GLM-4.5-Flash (70%), Claude Sonnet (25%)
- **Cost per developer:** ~$15/month average
- **Common prompts:** "fix bug", "explain code", "refactor"

**Insight:** Cached common responses could reduce costs by 30%.

### 6. Profiles Simplify Multi-Environment Work

Switching between dev/staging/prod gateways became seamless:

```bash
# Morning: Development work
source ~/.claude-profiles/dev.sh
claude "Create test fixtures"

# Afternoon: Production support
source ~/.claude-profiles/prod.sh
claude "Optimize production database query"
```

**Best Practice:** Name profiles by purpose: `dev.sh`, `prod.sh`, `experiments.sh`

### 7. Local LiteLLM for Offline Development

Running a local gateway proxy enables:
- Development without internet
- Testing gateway changes before deployment
- Privacy-sensitive work on local models

```bash
# Run local LiteLLM proxy
litellm --port 4000 --model glm-4.5-flash

# Point Claude to local
export ANTHROPIC_BASE_URL="http://localhost:4000"
```

## Best Practices

### 1. Security

- **Never commit API keys** to version control
- **Use `.gitignore`** for profile files with keys
- **Rotate keys regularly** (every 90 days)
- **Use separate keys** per environment/developer
- **Enable audit logging** in gateway dashboard

### 2. Cost Management

- **Set budget alerts** in gateway (80% threshold)
- **Use lower-cost models** for experimentation
- **Cache common responses** where possible
- **Monitor usage** weekly via dashboard
- **Delete unused keys** to prevent forgotten usage

### 3. Performance

- **Choose regions wisely** (closer = faster)
- **Use streaming mode** for long responses
- **Batch similar requests** to reduce overhead
- **Profile different models** for your use cases
- **Implement retry logic** with exponential backoff

### 4. Developer Experience

- **Document setup** in team README
- **Share successful prompts** in team wiki
- **Create prompt templates** for common tasks
- **Use aliases** for frequent commands:
   ```bash
   alias claude-debug="claude 'Debug this code and suggest fixes'"
   alias claude-explain="claude 'Explain this code in detail'"
   ```

### 5. Governance

- **Require approval** for production model access
- **Track usage** per team/project
- **Regular access reviews** (quarterly)
- **Document incident response** for quota exhaustion
- **Establish model selection guidelines**

## Comparison: Direct API vs LLM Gateway

| Aspect | Direct API | LLM Gateway |
|--------|-----------|-------------|
| **Setup Complexity** | Simple | Moderate |
| **Cost Tracking** | Per API key | Centralized |
| **Model Flexibility** | Single provider | Multi-provider |
| **Access Control** | API key only | IAM + policies |
| **Monitoring** | Limited | Comprehensive |
| **Corporate Compliance** | Self-managed | Built-in |
| **Vendor Lock-in** | High | Low |
| **Support** | Provider only | Internal IT + provider |

## Real-World Usage Examples

### Example 1: Daily Standup Helper

```bash
# Summarize git commits for standup
git log --since="yesterday" --oneline | \
  claude "Summarize these commits for a standup update"
```

### Example 2: Code Review Assistant

```bash
# Review changes before commit
git diff | claude "Review this diff for bugs, security issues, and style"
```

### Example 3: Documentation Generator

```bash
# Generate README for project
claude "Create a comprehensive README for this Python project" \
  --model claude-sonnet-4-5 < requirements.txt
```

### Example 4: Test Case Generator

```bash
# Generate unit tests
claude "Generate pytest unit tests for this function" < my_module.py
```

### Example 5: Migration Assistant

```bash
# Help with framework migration
claude "Convert this Flask app to FastAPI, explaining changes"
```

## Troubleshooting Commands

Quick reference for common issues:

```bash
# Check Claude CLI health
claude doctor

# Verify environment variables
env | grep ANTHROPIC

# Test gateway connectivity
curl -I $ANTHROPIC_BASE_URL/health

# List available models
curl -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
     $ANTHROPIC_BASE_URL/v1/models

# Check current usage
curl -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
     $ANTHROPIC_BASE_URL/v1/usage

# Verbose mode for debugging
claude --verbose "test prompt"

# Clear cache
rm -rf ~/.claude/cache

# Reset configuration
claude config reset
```

## Conclusion

Integrating Claude Code CLI with an enterprise LLM Gateway transforms individual AI assistance into a governed, scalable, and cost-effective development tool. While the initial setup requires coordination with gateway administrators and environment configuration, the benefits in governance and security quickly outweigh the complexity.

✅ **Centralized cost and usage tracking**  
✅ **Fine-grained access control via IAM**  
✅ **Flexibility to use any LLM model**  
✅ **Enhanced security and compliance**  
✅ **Team-wide visibility and governance**  

The key is starting small—get the basic integration working, then layer on profiles, monitoring, and policies as your usage grows.

### Next Steps

1. **Pilot with small team** (5-10 developers)
2. **Gather feedback** on model quality and performance
3. **Refine IAM policies** based on actual usage patterns
4. **Scale to department** once proven
5. **Evangelize success stories** to drive adoption

### Future Enhancements

- **Prompt library** for common tasks
- **Custom models** fine-tuned on company code
- **IDE integration** (VS Code, JetBrains)
- **Slack bot** for team queries
- **Automated code review** in CI/CD pipelines

---

## Resources

- [Claude Code CLI Documentation](https://docs.anthropic.com/claude/docs/cli)
- [LLM Gateway (Kong) Setup Guide](https://docs.konghq.com/gateway/)
- [LiteLLM Proxy Documentation](https://docs.litellm.ai/)
- [GLM-4.5 Model Information](https://github.com/THUDM/GLM-4)

---

*Published: February 2026*  
*Author: Enterprise AI Development Team*  
*Tags: #AI #LLM #Claude #Kong #DevTools #EnterpriseAI*

