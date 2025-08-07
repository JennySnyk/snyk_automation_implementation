# Snyk Automation Demo Project

This project demonstrates how to programmatically onboard hundreds of teams and repositories to Snyk, eliminating manual setup and making security a default part of your ecosystem.

## 🎯 Goal

Demonstrate automated Snyk onboarding that:
- Creates new Snyk organizations for teams
- Automatically enables security testing (Code, Open Source, IaC, Container)
- Applies specific security policies
- Invites team members
- Imports repositories into Snyk
- Integrates with existing development workflows

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions  │───▶│  Snyk API       │
│   Creation      │    │  Workflow        │    │  Integration    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Webhook       │───▶│  Flask Server    │───▶│  Enhanced       │
│   Trigger       │    │  Handler         │    │  Automation     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Manual        │───▶│  Demo Runner     │───▶│  Bulk           │
│   Execution     │    │  Interactive     │    │  Onboarding     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
snyk_automation/
├── README_DEMO.md                    # This file
├── requirements.txt                  # Python dependencies
├── setup_env.sh                     # Environment setup script
├── .env.example                     # Environment variables template
├── teams_config.json               # Team configuration file
├── 
├── Core Scripts:
├── enhanced_snyk_automation.py      # Main automation engine
├── snyk_management.py              # Original base script
├── webhook_handler.py              # Webhook server
├── demo_runner.py                  # Interactive demo
├── 
├── GitHub Integration:
└── .github/
    └── workflows/
        └── snyk-onboarding.yml     # GitHub Actions workflow
```

## 🚀 Quick Start

### 1. Environment Setup

Run the setup script to configure your environment:

```bash
chmod +x setup_env.sh
./setup_env.sh
```

This will prompt you for:
- **Snyk API Token** (required) - Get from [Snyk Account Settings](https://app.snyk.io/account)
- **Snyk Group ID** (required) - Get from [Snyk Group Settings](https://app.snyk.io/manage/groups)
- **GitHub Token** (optional) - Get from [GitHub Settings](https://github.com/settings/tokens)
- **Webhook Secret** (optional) - For webhook security

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Interactive Demo

```bash
python demo_runner.py
```

## 🎮 Demo Options

### Option 1: Interactive Demo
The interactive demo provides a menu-driven experience:

```bash
python demo_runner.py
```

**Features:**
- Single team onboarding demonstration
- Bulk team onboarding (multiple teams at once)
- Webhook-triggered automation
- GitHub Actions integration information

### Option 2: Direct Script Execution
Run the automation directly with the provided configuration:

```bash
python enhanced_snyk_automation.py
```

This uses the `teams_config.json` file to onboard multiple teams.

### Option 3: Webhook Server
Start the webhook server to handle HTTP requests:

```bash
python webhook_handler.py
```

**Endpoints:**
- `POST /webhook/onboard` - Single team onboarding
- `POST /webhook/bulk-onboard` - Bulk team onboarding
- `GET /health` - Health check
- `POST /webhook/test` - Test endpoint

**Example webhook payload:**
```json
{
  "team": {
    "name": "Frontend Team",
    "repositories": ["company/react-app", "company/ui-lib"],
    "members": ["lead@company.com", "dev@company.com"],
    "policies": ["high-severity-policy", "license-policy"],
    "testing_types": ["sast", "sca"]
  }
}
```

### Option 4: GitHub Actions Integration
The project includes a GitHub Actions workflow that can be triggered:

1. **Manually** via workflow_dispatch
2. **Automatically** via repository_dispatch API
3. **On events** like push or pull requests

## 🔧 Configuration

### Team Configuration Format
Teams are configured in `teams_config.json`:

```json
{
  "teams": [
    {
      "team_name": "Frontend Development Team",
      "repositories": [
        "company/react-dashboard",
        "company/component-library"
      ],
      "members": [
        "frontend-lead@company.com",
        "react-dev@company.com"
      ],
      "policies": [
        "high-severity-policy",
        "license-policy"
      ],
      "testing_types": [
        "sast",
        "sca",
        "iac"
      ]
    }
  ]
}
```

### Environment Variables
Create a `.env` file or set these environment variables:

```bash
# Required
SNYK_API_TOKEN=your_snyk_api_token
SNYK_GROUP_ID=your_snyk_group_id

# Optional
GITHUB_TOKEN=your_github_token
WEBHOOK_SECRET=your_webhook_secret
PORT=5000
DEBUG=false
```

## 🔄 Automation Workflow

For each team, the automation performs these steps:

1. **🏢 Create Organization**
   - Creates a new Snyk organization for the team
   - Returns organization ID for subsequent operations

2. **🔍 Enable Testing Types**
   - Enables specified security testing types:
     - `sast` - Static Application Security Testing
     - `sca` - Software Composition Analysis
     - `iac` - Infrastructure as Code scanning
     - `container` - Container image scanning

3. **📋 Apply Policies**
   - Applies security policies to the organization
   - Examples: severity thresholds, license policies, compliance rules

4. **👥 Invite Members**
   - Sends invitations to team members
   - Assigns appropriate roles (collaborator, admin, etc.)

5. **🔗 Setup Integrations**
   - Configures GitHub integration
   - Enables automatic scanning of repositories

6. **📦 Import Repositories**
   - Imports specified repositories into Snyk
   - Starts initial security scans

## 🌐 API Integration Examples

### Trigger via cURL (Webhook)
```bash
# Single team onboarding
curl -X POST http://localhost:5000/webhook/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "team": {
      "name": "API Team",
      "repositories": ["company/api-service"],
      "members": ["api-lead@company.com"],
      "testing_types": ["sast", "sca"]
    }
  }'
```

### Trigger via GitHub API (Repository Dispatch)
```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_ORG/YOUR_REPO/dispatches \
  -d '{
    "event_type": "snyk-onboard-team",
    "client_payload": {
      "team_name": "Mobile Team",
      "repositories": "company/ios-app,company/android-app",
      "members": "mobile-lead@company.com,ios-dev@company.com",
      "testing_types": "sast,sca",
      "policies": "high-severity-policy"
    }
  }'
```

## 📊 Expected Results

After successful onboarding, you should see:

### In Snyk Dashboard:
- ✅ New organization created for each team
- ✅ Security testing enabled for all specified types
- ✅ Policies applied and active
- ✅ Team members invited and added
- ✅ Repositories imported and scanning
- ✅ GitHub integration configured

### In Console Output:
```
📋 Results for Frontend Development Team:
  ✅ Organization created (ID: abc123-def456)
  ✅ Security testing enabled
  ✅ Security policies applied
  ✅ Team members invited
  ✅ GitHub integration configured
  📦 Repository imports:
    ✅ company/react-dashboard
    ✅ company/component-library
```

## 🔒 Security Considerations

1. **API Tokens**: Store securely and rotate regularly
2. **Webhook Security**: Use webhook secrets for verification
3. **Environment Variables**: Never commit sensitive data to version control
4. **Access Control**: Use least-privilege principles for API tokens
5. **Audit Logging**: Monitor automation activities

## 🚨 Troubleshooting

### Common Issues:

**Authentication Errors**
```
❌ HTTP Error: 401 Unauthorized
```
- Check your `SNYK_API_TOKEN` is correct and active
- Verify token has necessary permissions

**Group ID Issues**
```
❌ Failed to create organization
```
- Verify `SNYK_GROUP_ID` is correct
- Ensure you have admin permissions on the group

**Rate Limiting**
```
❌ HTTP Error: 429 Too Many Requests
```
- The script includes rate limiting delays
- Consider reducing batch sizes for large deployments

**GitHub Integration Failures**
```
❌ GitHub integration failed
```
- Check `GITHUB_TOKEN` permissions (repo, admin:org scopes)
- Verify token is not expired

## 📈 Scaling for Production

For production deployments:

1. **Use a queue system** (Redis, RabbitMQ) for processing requests
2. **Implement proper error handling** and retry mechanisms
3. **Add monitoring and alerting** for automation health
4. **Use database storage** for tracking onboarding status
5. **Implement webhook signature verification**
6. **Add comprehensive logging** and audit trails
7. **Consider using Kubernetes** for scalable deployment

## 🤝 Contributing

To extend this demo:

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is provided as a demonstration and learning resource. Please review Snyk's API terms of service and your organization's policies before using in production.

## 🆘 Support

For questions about this demo:
- Check the troubleshooting section above
- Review Snyk API documentation
- Open an issue in this repository

For Snyk-specific support:
- Visit [Snyk Support](https://support.snyk.io/)
- Check [Snyk Documentation](https://docs.snyk.io/)
- Join the [Snyk Community](https://community.snyk.io/)
