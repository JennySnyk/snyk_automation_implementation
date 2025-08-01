# Snyk Management Script

This script automates the creation of a Snyk organization, inviting members, and setting up integrations using the Snyk API.

## Prerequisites

- Python 3.6+
- A Snyk account with access to an API token.
- Your Snyk Group ID.

## Setup

1.  **Clone the repository or download the files.**

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    You need to provide your Snyk API token and Group ID. You can do this by setting environment variables:

    ```bash
    export SNYK_API_TOKEN='your_snyk_api_token_here'
    export SNYK_GROUP_ID='your_snyk_group_id_here'
    ```

    To set up an integration (e.g., with GitHub), you will also need to provide an access token for that service:

    ```bash
    export GITHUB_TOKEN='your_github_personal_access_token_here'
    ```

    Alternatively, you can hardcode these values in the `snyk_management.py` script, but using environment variables is recommended for security.

## Usage

1.  **Customize the script:**

    Open `snyk_management.py` and modify the following variables in the `if __name__ == '__main__':` block if needed:

    - `new_org_name`: The name of the new organization you want to create.
    - `member_email`: The email of the member you want to invite.

2.  **Run the script:**

    ```bash
    python snyk_management.py
    ```

The script will then:
- Create a new Snyk organization.
- Invite the specified member to the new organization.
- Set up a GitHub integration if a `GITHUB_TOKEN` is provided.
