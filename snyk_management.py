import os
import requests
import json

# --- Configuration ---
SNYK_API_TOKEN = os.getenv('SNYK_API_TOKEN', 'YOUR_SNYK_API_TOKEN')
SNYK_API_URL = 'https://api.snyk.io/v1'
GROUP_ID = os.getenv('SNYK_GROUP_ID', 'YOUR_SNYK_GROUP_ID') # Your Snyk Group ID

# --- Helper Functions ---
def snyk_request(method, path, payload=None):
    """Helper function to make requests to the Snyk API."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {SNYK_API_TOKEN}'
    }
    url = f"{SNYK_API_URL}{path}"
    try:
        if payload:
            response = requests.request(method, url, headers=headers, data=json.dumps(payload))
        else:
            response = requests.request(method, url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print(f"Response content: {err.response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

# --- Core Functions ---
def create_organization(org_name):
    """Creates a new Snyk organization."""
    print(f"Creating organization: {org_name}...")
    payload = {'name': org_name}
    path = f'/group/{GROUP_ID}/org'
    return snyk_request('POST', path, payload)

def invite_member(org_id, email, role='collaborator'):
    """Invites a member to a Snyk organization."""
    print(f"Inviting {email} to organization ID: {org_id}...")
    payload = {'email': email, 'role': role}
    path = f'/org/{org_id}/invite'
    return snyk_request('POST', path, payload)

def setup_integration(org_id, integration_type='github', integration_token=None):
    """Sets up an integration for a Snyk organization."""
    print(f"Setting up {integration_type} integration for organization ID: {org_id}...")
    if integration_type == 'github' and integration_token:
        # This is a simplified example. The actual payload might differ.
        # Please refer to the Snyk API documentation for the correct payload structure.
        # For GitHub, you usually need to provide a personal access token.
        payload = {
            'token': integration_token
        }
        path = f'/org/{org_id}/integrations/github'
        return snyk_request('POST', path, payload)
    else:
        print(f"Integration type '{integration_type}' not supported or token missing.")
        return None

# --- Main Execution ---
if __name__ == '__main__':
    # 1. Create a new organization
    new_org_name = 'My New Snyk Org'
    new_org = create_organization(new_org_name)
    if new_org and 'id' in new_org:
        org_id = new_org['id']
        print(f"Successfully created organization with ID: {org_id}")

        # 2. Invite a member
        member_email = 'user@example.com'
        invite_result = invite_member(org_id, member_email)
        if invite_result:
            print(f"Successfully sent invitation to {member_email}")

        # 3. Set up an integration (e.g., GitHub)
        # IMPORTANT: You'll need a GitHub Personal Access Token with the correct permissions.
        github_token = os.getenv('GITHUB_TOKEN', 'YOUR_GITHUB_TOKEN')
        if github_token != 'YOUR_GITHUB_TOKEN':
            integration_result = setup_integration(org_id, 'github', github_token)
            if integration_result:
                print("Successfully set up GitHub integration.")
        else:
            print("\nSkipping GitHub integration setup. Please set the GITHUB_TOKEN environment variable.")

    else:
        print("Failed to create organization. Please check your SNYK_API_TOKEN and SNYK_GROUP_ID.")
