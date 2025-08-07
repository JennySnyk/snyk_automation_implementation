#!/usr/bin/env python3
"""
Enhanced Snyk Automation Script
Demonstrates bulk onboarding of teams and repositories to Snyk
"""

import os
import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TeamConfig:
    """Configuration for a team to be onboarded"""
    team_name: str
    repositories: List[str]
    members: List[str]
    policies: List[str] = None
    testing_types: List[str] = None

class SnykAutomation:
    """Enhanced Snyk automation for bulk onboarding"""
    
    def __init__(self):
        self.snyk_token = os.getenv('SNYK_API_TOKEN')
        self.group_id = os.getenv('SNYK_GROUP_ID')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.snyk_api_url = 'https://api.snyk.io/v1'
        self.github_api_url = 'https://api.github.com'
        
        if not self.snyk_token or not self.group_id:
            raise ValueError("SNYK_API_TOKEN and SNYK_GROUP_ID must be set")
    
    def _snyk_request(self, method: str, path: str, payload: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated request to Snyk API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'token {self.snyk_token}'
        }
        url = f"{self.snyk_api_url}{path}"
        
        try:
            if payload:
                response = requests.request(method, url, headers=headers, json=payload)
            else:
                response = requests.request(method, url, headers=headers)
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Snyk API request failed: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def _github_request(self, method: str, path: str, payload: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated request to GitHub API"""
        if not self.github_token:
            logger.warning("GitHub token not provided, skipping GitHub operations")
            return None
            
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        url = f"{self.github_api_url}{path}"
        
        try:
            if payload:
                response = requests.request(method, url, headers=headers, json=payload)
            else:
                response = requests.request(method, url, headers=headers)
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {e}")
            return None
    
    def create_organization(self, org_name: str) -> Optional[str]:
        """Create a new Snyk organization"""
        logger.info(f"Creating Snyk organization: {org_name}")
        
        payload = {'name': org_name}
        result = self._snyk_request('POST', f'/group/{self.group_id}/org', payload)
        
        if result and 'id' in result:
            org_id = result['id']
            logger.info(f"Successfully created organization with ID: {org_id}")
            return org_id
        else:
            logger.error(f"Failed to create organization: {org_name}")
            return None
    
    def enable_testing_types(self, org_id: str, testing_types: List[str]) -> bool:
        """Enable specific testing types for the organization"""
        logger.info(f"Enabling testing types {testing_types} for org {org_id}")
        
        # Note: This is a simplified example. Actual API endpoints may vary
        success = True
        for test_type in testing_types:
            payload = {'type': test_type, 'enabled': True}
            result = self._snyk_request('PUT', f'/org/{org_id}/settings/testing', payload)
            if not result:
                success = False
                logger.error(f"Failed to enable {test_type} testing")
        
        return success
    
    def apply_policies(self, org_id: str, policies: List[str]) -> bool:
        """Apply security policies to the organization"""
        logger.info(f"Applying policies {policies} to org {org_id}")
        
        success = True
        for policy in policies:
            # This is a simplified example - actual policy application may be more complex
            payload = {'policy': policy, 'enabled': True}
            result = self._snyk_request('PUT', f'/org/{org_id}/policies', payload)
            if not result:
                success = False
                logger.error(f"Failed to apply policy: {policy}")
        
        return success
    
    def invite_members(self, org_id: str, members: List[str], role: str = 'collaborator') -> bool:
        """Invite multiple members to the organization"""
        logger.info(f"Inviting {len(members)} members to org {org_id}")
        
        success = True
        for email in members:
            payload = {'email': email, 'role': role}
            result = self._snyk_request('POST', f'/org/{org_id}/invite', payload)
            if result:
                logger.info(f"Successfully invited {email}")
            else:
                success = False
                logger.error(f"Failed to invite {email}")
            
            # Rate limiting
            time.sleep(0.5)
        
        return success
    
    def setup_github_integration(self, org_id: str) -> bool:
        """Set up GitHub integration for the organization"""
        if not self.github_token:
            logger.warning("GitHub token not provided, skipping integration setup")
            return False
            
        logger.info(f"Setting up GitHub integration for org {org_id}")
        
        payload = {'token': self.github_token}
        result = self._snyk_request('POST', f'/org/{org_id}/integrations/github', payload)
        
        if result:
            logger.info("Successfully set up GitHub integration")
            return True
        else:
            logger.error("Failed to set up GitHub integration")
            return False
    
    def import_repositories(self, org_id: str, repositories: List[str]) -> Dict[str, bool]:
        """Import multiple repositories into Snyk"""
        logger.info(f"Importing {len(repositories)} repositories to org {org_id}")
        
        results = {}
        for repo in repositories:
            logger.info(f"Importing repository: {repo}")
            
            # Parse owner/repo from full repository name
            if '/' in repo:
                owner, repo_name = repo.split('/', 1)
            else:
                logger.error(f"Invalid repository format: {repo}")
                results[repo] = False
                continue
            
            payload = {
                'target': {
                    'owner': owner,
                    'name': repo_name,
                    'branch': 'main'  # Default to main branch
                }
            }
            
            result = self._snyk_request('POST', f'/org/{org_id}/integrations/github/import', payload)
            results[repo] = result is not None
            
            if results[repo]:
                logger.info(f"Successfully imported {repo}")
            else:
                logger.error(f"Failed to import {repo}")
            
            # Rate limiting
            time.sleep(1)
        
        return results
    
    def onboard_team(self, team_config: TeamConfig) -> Dict[str, Any]:
        """Complete onboarding process for a team"""
        logger.info(f"Starting onboarding for team: {team_config.team_name}")
        
        results = {
            'team_name': team_config.team_name,
            'org_created': False,
            'org_id': None,
            'testing_enabled': False,
            'policies_applied': False,
            'members_invited': False,
            'github_integration': False,
            'repositories_imported': {}
        }
        
        # Step 1: Create organization
        org_id = self.create_organization(team_config.team_name)
        if not org_id:
            logger.error(f"Failed to create organization for team {team_config.team_name}")
            return results
        
        results['org_created'] = True
        results['org_id'] = org_id
        
        # Step 2: Enable testing types
        if team_config.testing_types:
            results['testing_enabled'] = self.enable_testing_types(org_id, team_config.testing_types)
        else:
            # Default testing types
            default_types = ['sast', 'sca', 'iac', 'container']
            results['testing_enabled'] = self.enable_testing_types(org_id, default_types)
        
        # Step 3: Apply policies
        if team_config.policies:
            results['policies_applied'] = self.apply_policies(org_id, team_config.policies)
        else:
            # Apply default policies
            default_policies = ['high-severity-policy', 'license-policy']
            results['policies_applied'] = self.apply_policies(org_id, default_policies)
        
        # Step 4: Invite members
        if team_config.members:
            results['members_invited'] = self.invite_members(org_id, team_config.members)
        
        # Step 5: Set up GitHub integration
        results['github_integration'] = self.setup_github_integration(org_id)
        
        # Step 6: Import repositories
        if team_config.repositories:
            results['repositories_imported'] = self.import_repositories(org_id, team_config.repositories)
        
        logger.info(f"Completed onboarding for team: {team_config.team_name}")
        return results
    
    def bulk_onboard_teams(self, teams: List[TeamConfig]) -> List[Dict[str, Any]]:
        """Onboard multiple teams in bulk"""
        logger.info(f"Starting bulk onboarding for {len(teams)} teams")
        
        results = []
        for team in teams:
            try:
                result = self.onboard_team(team)
                results.append(result)
                
                # Brief pause between teams to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to onboard team {team.team_name}: {e}")
                results.append({
                    'team_name': team.team_name,
                    'error': str(e),
                    'org_created': False
                })
        
        logger.info("Bulk onboarding completed")
        return results

def load_teams_from_config(config_file: str) -> List[TeamConfig]:
    """Load team configurations from JSON file"""
    try:
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        teams = []
        for team_data in data.get('teams', []):
            team = TeamConfig(
                team_name=team_data['team_name'],
                repositories=team_data.get('repositories', []),
                members=team_data.get('members', []),
                policies=team_data.get('policies'),
                testing_types=team_data.get('testing_types')
            )
            teams.append(team)
        
        return teams
    except Exception as e:
        logger.error(f"Failed to load teams configuration: {e}")
        return []

def main():
    """Main execution function"""
    try:
        automation = SnykAutomation()
        
        # Check if config file exists
        config_file = 'teams_config.json'
        if os.path.exists(config_file):
            logger.info(f"Loading teams from {config_file}")
            teams = load_teams_from_config(config_file)
        else:
            # Demo configuration
            logger.info("Using demo configuration")
            teams = [
                TeamConfig(
                    team_name="Frontend Team Demo",
                    repositories=["myorg/frontend-app", "myorg/ui-components"],
                    members=["frontend-lead@company.com", "ui-dev@company.com"],
                    policies=["high-severity-policy", "license-policy"],
                    testing_types=["sast", "sca"]
                ),
                TeamConfig(
                    team_name="Backend Team Demo",
                    repositories=["myorg/api-service", "myorg/database-migrations"],
                    members=["backend-lead@company.com", "api-dev@company.com"],
                    policies=["high-severity-policy", "container-policy"],
                    testing_types=["sast", "sca", "container"]
                )
            ]
        
        if not teams:
            logger.error("No teams to onboard")
            return
        
        # Perform bulk onboarding
        results = automation.bulk_onboard_teams(teams)
        
        # Print summary
        print("\n" + "="*50)
        print("ONBOARDING SUMMARY")
        print("="*50)
        
        for result in results:
            print(f"\nTeam: {result['team_name']}")
            print(f"  Organization Created: {result.get('org_created', False)}")
            if result.get('org_id'):
                print(f"  Organization ID: {result['org_id']}")
            print(f"  Testing Enabled: {result.get('testing_enabled', False)}")
            print(f"  Policies Applied: {result.get('policies_applied', False)}")
            print(f"  Members Invited: {result.get('members_invited', False)}")
            print(f"  GitHub Integration: {result.get('github_integration', False)}")
            
            repo_results = result.get('repositories_imported', {})
            if repo_results:
                print(f"  Repositories Imported:")
                for repo, success in repo_results.items():
                    print(f"    {repo}: {'✓' if success else '✗'}")
            
            if 'error' in result:
                print(f"  Error: {result['error']}")
        
        print("\n" + "="*50)
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        raise

if __name__ == '__main__':
    main()
