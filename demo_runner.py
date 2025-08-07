#!/usr/bin/env python3
"""
Demo Runner for Snyk Automation
Provides interactive demonstration of the automation capabilities
"""

import os
import json
import time
import requests
from typing import Dict, Any
from enhanced_snyk_automation import SnykAutomation, TeamConfig

class SnykAutomationDemo:
    """Interactive demo for Snyk automation"""
    
    def __init__(self):
        self.automation = None
        self.webhook_url = "http://localhost:5000"
    
    def check_prerequisites(self) -> bool:
        """Check if all required environment variables are set"""
        required_vars = ['SNYK_API_TOKEN', 'SNYK_GROUP_ID']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print("❌ Missing required environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\nPlease set these variables and try again.")
            return False
        
        print("✅ All required environment variables are set")
        return True
    
    def initialize_automation(self) -> bool:
        """Initialize the Snyk automation"""
        try:
            self.automation = SnykAutomation()
            print("✅ Snyk automation initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Snyk automation: {e}")
            return False
    
    def demo_single_team_onboarding(self):
        """Demonstrate single team onboarding"""
        print("\n" + "="*60)
        print("DEMO: Single Team Onboarding")
        print("="*60)
        
        # Create a demo team configuration
        team_config = TeamConfig(
            team_name="Demo Frontend Team",
            repositories=["demo-org/react-app", "demo-org/component-lib"],
            members=["demo-lead@company.com", "demo-dev@company.com"],
            policies=["high-severity-policy", "license-policy"],
            testing_types=["sast", "sca"]
        )
        
        print(f"Onboarding team: {team_config.team_name}")
        print(f"Repositories: {', '.join(team_config.repositories)}")
        print(f"Members: {', '.join(team_config.members)}")
        print(f"Testing types: {', '.join(team_config.testing_types)}")
        
        # Simulate the onboarding process
        print("\n🚀 Starting onboarding process...")
        
        try:
            result = self.automation.onboard_team(team_config)
            self.print_onboarding_result(result)
        except Exception as e:
            print(f"❌ Onboarding failed: {e}")
    
    def demo_bulk_onboarding(self):
        """Demonstrate bulk team onboarding"""
        print("\n" + "="*60)
        print("DEMO: Bulk Team Onboarding")
        print("="*60)
        
        # Create multiple demo teams
        teams = [
            TeamConfig(
                team_name="Demo Backend Team",
                repositories=["demo-org/api-service", "demo-org/auth-service"],
                members=["backend-lead@company.com", "api-dev@company.com"],
                policies=["high-severity-policy", "container-policy"],
                testing_types=["sast", "sca", "container"]
            ),
            TeamConfig(
                team_name="Demo DevOps Team",
                repositories=["demo-org/infrastructure", "demo-org/ci-cd"],
                members=["devops-lead@company.com", "sre@company.com"],
                policies=["iac-policy", "container-policy"],
                testing_types=["iac", "container"]
            )
        ]
        
        print(f"Onboarding {len(teams)} teams:")
        for team in teams:
            print(f"  - {team.team_name} ({len(team.repositories)} repos, {len(team.members)} members)")
        
        print("\n🚀 Starting bulk onboarding process...")
        
        try:
            results = self.automation.bulk_onboard_teams(teams)
            
            print("\n📊 Bulk Onboarding Results:")
            for result in results:
                self.print_onboarding_result(result)
                
        except Exception as e:
            print(f"❌ Bulk onboarding failed: {e}")
    
    def demo_webhook_trigger(self):
        """Demonstrate webhook-triggered onboarding"""
        print("\n" + "="*60)
        print("DEMO: Webhook-Triggered Onboarding")
        print("="*60)
        
        # Check if webhook server is running
        try:
            response = requests.get(f"{self.webhook_url}/health", timeout=5)
            if response.status_code != 200:
                raise requests.RequestException("Health check failed")
        except requests.RequestException:
            print("❌ Webhook server is not running")
            print("To start the webhook server, run:")
            print("   python webhook_handler.py")
            return
        
        print("✅ Webhook server is running")
        
        # Prepare webhook payload
        payload = {
            "team": {
                "name": "Demo Webhook Team",
                "repositories": ["demo-org/webhook-app"],
                "members": ["webhook-dev@company.com"],
                "policies": ["high-severity-policy"],
                "testing_types": ["sast", "sca"]
            }
        }
        
        print(f"Sending webhook request to: {self.webhook_url}/webhook/onboard")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                f"{self.webhook_url}/webhook/onboard",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 202:
                print("✅ Webhook request accepted")
                print("🔄 Onboarding process started asynchronously")
                print("Check the webhook server logs for progress")
            else:
                print(f"❌ Webhook request failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.RequestException as e:
            print(f"❌ Failed to send webhook request: {e}")
    
    def demo_github_actions_trigger(self):
        """Demonstrate GitHub Actions workflow trigger"""
        print("\n" + "="*60)
        print("DEMO: GitHub Actions Workflow Trigger")
        print("="*60)
        
        print("To trigger the GitHub Actions workflow, you can:")
        print("\n1. Manual Trigger (workflow_dispatch):")
        print("   - Go to your repository's Actions tab")
        print("   - Select 'Snyk Team Onboarding Automation' workflow")
        print("   - Click 'Run workflow' and fill in the parameters")
        
        print("\n2. Repository Dispatch API:")
        print("   curl -X POST \\")
        print("     -H 'Authorization: token YOUR_GITHUB_TOKEN' \\")
        print("     -H 'Accept: application/vnd.github.v3+json' \\")
        print("     https://api.github.com/repos/YOUR_ORG/YOUR_REPO/dispatches \\")
        print("     -d '{")
        print('       "event_type": "snyk-onboard-team",')
        print('       "client_payload": {')
        print('         "team_name": "API Triggered Team",')
        print('         "repositories": "org/repo1,org/repo2",')
        print('         "members": "dev1@company.com,dev2@company.com",')
        print('         "testing_types": "sast,sca",')
        print('         "policies": "high-severity-policy"')
        print("       }")
        print("     }'")
        
        print("\n3. Automatic Triggers:")
        print("   - Repository creation events")
        print("   - Organization member addition events")
        print("   - Custom webhook events")
    
    def print_onboarding_result(self, result: Dict[str, Any]):
        """Print formatted onboarding result"""
        team_name = result.get('team_name', 'Unknown')
        print(f"\n📋 Results for {team_name}:")
        
        # Organization creation
        if result.get('org_created'):
            print(f"  ✅ Organization created (ID: {result.get('org_id')})")
        else:
            print("  ❌ Organization creation failed")
        
        # Testing enablement
        if result.get('testing_enabled'):
            print("  ✅ Security testing enabled")
        else:
            print("  ❌ Security testing enablement failed")
        
        # Policy application
        if result.get('policies_applied'):
            print("  ✅ Security policies applied")
        else:
            print("  ❌ Security policy application failed")
        
        # Member invitations
        if result.get('members_invited'):
            print("  ✅ Team members invited")
        else:
            print("  ❌ Member invitation failed")
        
        # GitHub integration
        if result.get('github_integration'):
            print("  ✅ GitHub integration configured")
        else:
            print("  ❌ GitHub integration failed")
        
        # Repository imports
        repo_results = result.get('repositories_imported', {})
        if repo_results:
            print("  📦 Repository imports:")
            for repo, success in repo_results.items():
                status = "✅" if success else "❌"
                print(f"    {status} {repo}")
        
        if 'error' in result:
            print(f"  ❌ Error: {result['error']}")
    
    def run_interactive_demo(self):
        """Run interactive demo menu"""
        print("🎯 Snyk Automation Demo")
        print("=" * 50)
        
        if not self.check_prerequisites():
            return
        
        if not self.initialize_automation():
            return
        
        while True:
            print("\nSelect a demo option:")
            print("1. Single Team Onboarding")
            print("2. Bulk Team Onboarding")
            print("3. Webhook-Triggered Onboarding")
            print("4. GitHub Actions Integration Info")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.demo_single_team_onboarding()
            elif choice == '2':
                self.demo_bulk_onboarding()
            elif choice == '3':
                self.demo_webhook_trigger()
            elif choice == '4':
                self.demo_github_actions_trigger()
            elif choice == '5':
                print("👋 Thanks for trying the Snyk Automation Demo!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
            
            input("\nPress Enter to continue...")

def main():
    """Main execution function"""
    demo = SnykAutomationDemo()
    demo.run_interactive_demo()

if __name__ == '__main__':
    main()
