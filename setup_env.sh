#!/bin/bash

# Snyk Automation Environment Setup Script
# This script helps set up the required environment variables for the demo

echo "🔧 Snyk Automation Environment Setup"
echo "====================================="

# Function to prompt for input with validation
prompt_for_input() {
    local var_name="$1"
    local description="$2"
    local is_secret="$3"
    
    echo ""
    echo "Setting up: $var_name"
    echo "Description: $description"
    
    if [ "$is_secret" = "true" ]; then
        echo "⚠️  This is sensitive information - input will be hidden"
        read -s -p "Enter value: " value
        echo ""
    else
        read -p "Enter value: " value
    fi
    
    if [ -z "$value" ]; then
        echo "❌ Value cannot be empty"
        return 1
    fi
    
    export "$var_name"="$value"
    echo "✅ $var_name set successfully"
    return 0
}

# Check if .env file exists
ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    echo "📁 Found existing .env file"
    read -p "Do you want to load existing values? (y/n): " load_existing
    if [ "$load_existing" = "y" ] || [ "$load_existing" = "Y" ]; then
        source "$ENV_FILE"
        echo "✅ Loaded existing environment variables"
    fi
fi

echo ""
echo "🔑 Required Environment Variables"
echo "================================"

# Snyk API Token
if [ -z "$SNYK_API_TOKEN" ]; then
    echo ""
    echo "1. SNYK_API_TOKEN"
    echo "   Get this from: https://app.snyk.io/account (Account Settings > API Token)"
    while ! prompt_for_input "SNYK_API_TOKEN" "Your Snyk API token" "true"; do
        echo "Please try again"
    done
else
    echo "✅ SNYK_API_TOKEN already set"
fi

# Snyk Group ID
if [ -z "$SNYK_GROUP_ID" ]; then
    echo ""
    echo "2. SNYK_GROUP_ID"
    echo "   Get this from: https://app.snyk.io/manage/groups (Group Settings > Group ID)"
    while ! prompt_for_input "SNYK_GROUP_ID" "Your Snyk Group ID" "false"; do
        echo "Please try again"
    done
else
    echo "✅ SNYK_GROUP_ID already set"
fi

echo ""
echo "🔑 Optional Environment Variables"
echo "================================"

# GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "3. GITHUB_TOKEN (Optional but recommended)"
    echo "   Get this from: https://github.com/settings/tokens"
    echo "   Required scopes: repo, admin:org"
    read -p "Do you want to set GitHub token? (y/n): " set_github
    if [ "$set_github" = "y" ] || [ "$set_github" = "Y" ]; then
        while ! prompt_for_input "GITHUB_TOKEN" "Your GitHub Personal Access Token" "true"; do
            echo "Please try again"
        done
    else
        echo "⚠️  GitHub integration will be skipped"
    fi
else
    echo "✅ GITHUB_TOKEN already set"
fi

# Webhook Secret
if [ -z "$WEBHOOK_SECRET" ]; then
    echo ""
    echo "4. WEBHOOK_SECRET (Optional)"
    echo "   A secret key for webhook security"
    read -p "Do you want to set webhook secret? (y/n): " set_webhook
    if [ "$set_webhook" = "y" ] || [ "$set_webhook" = "Y" ]; then
        # Generate a random secret if not provided
        read -p "Enter webhook secret (leave empty to generate): " webhook_secret
        if [ -z "$webhook_secret" ]; then
            webhook_secret=$(openssl rand -hex 32)
            echo "🔐 Generated random webhook secret"
        fi
        export WEBHOOK_SECRET="$webhook_secret"
        echo "✅ WEBHOOK_SECRET set successfully"
    fi
else
    echo "✅ WEBHOOK_SECRET already set"
fi

# Save to .env file
echo ""
echo "💾 Saving Environment Variables"
echo "==============================="

cat > "$ENV_FILE" << EOF
# Snyk Automation Environment Variables
# Generated on $(date)

# Required Variables
SNYK_API_TOKEN=$SNYK_API_TOKEN
SNYK_GROUP_ID=$SNYK_GROUP_ID

# Optional Variables
EOF

if [ ! -z "$GITHUB_TOKEN" ]; then
    echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> "$ENV_FILE"
fi

if [ ! -z "$WEBHOOK_SECRET" ]; then
    echo "WEBHOOK_SECRET=$WEBHOOK_SECRET" >> "$ENV_FILE"
fi

echo ""
echo "✅ Environment variables saved to $ENV_FILE"
echo ""
echo "🚀 Setup Complete!"
echo "=================="
echo ""
echo "To use these variables in your current session:"
echo "  source $ENV_FILE"
echo ""
echo "To run the demo:"
echo "  python demo_runner.py"
echo ""
echo "To start the webhook server:"
echo "  python webhook_handler.py"
echo ""
echo "To run the automation directly:"
echo "  python enhanced_snyk_automation.py"
echo ""
echo "⚠️  Remember to:"
echo "   - Keep your .env file secure and don't commit it to version control"
echo "   - Add .env to your .gitignore file"
echo "   - Set up GitHub repository secrets for CI/CD workflows"
