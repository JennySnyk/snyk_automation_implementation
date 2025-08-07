#!/usr/bin/env python3
"""
Webhook Handler for Snyk Automation
Handles incoming webhook requests to trigger automated Snyk onboarding
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from threading import Thread
from enhanced_snyk_automation import SnykAutomation, TeamConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Webhook secret for security (optional but recommended)
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-webhook-secret')

def verify_webhook_signature(request_data: bytes, signature: str) -> bool:
    """Verify webhook signature for security"""
    import hmac
    import hashlib
    
    if not signature:
        return False
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        request_data,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

def process_onboarding_request(payload: dict):
    """Process the onboarding request in a separate thread"""
    try:
        logger.info("Processing onboarding request...")
        
        # Extract team information from payload
        team_data = payload.get('team', {})
        
        if not team_data:
            logger.error("No team data provided in webhook payload")
            return
        
        # Create TeamConfig from webhook payload
        team_config = TeamConfig(
            team_name=team_data.get('name', 'Unknown Team'),
            repositories=team_data.get('repositories', []),
            members=team_data.get('members', []),
            policies=team_data.get('policies'),
            testing_types=team_data.get('testing_types')
        )
        
        # Initialize automation and onboard the team
        automation = SnykAutomation()
        result = automation.onboard_team(team_config)
        
        logger.info(f"Onboarding completed for team: {team_config.team_name}")
        logger.info(f"Result: {json.dumps(result, indent=2)}")
        
        # Here you could send the result to a notification system,
        # update a database, or trigger other workflows
        
    except Exception as e:
        logger.error(f"Error processing onboarding request: {e}")

@app.route('/webhook/onboard', methods=['POST'])
def webhook_onboard():
    """Handle webhook requests for team onboarding"""
    try:
        # Get the signature from headers
        signature = request.headers.get('X-Hub-Signature-256')
        
        # Verify signature if secret is configured
        if WEBHOOK_SECRET != 'your-webhook-secret':
            if not verify_webhook_signature(request.data, signature):
                logger.warning("Invalid webhook signature")
                return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse the payload
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        logger.info(f"Received webhook request: {json.dumps(payload, indent=2)}")
        
        # Process the request asynchronously
        thread = Thread(target=process_onboarding_request, args=(payload,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'accepted',
            'message': 'Onboarding request received and processing started'
        }), 202
        
    except Exception as e:
        logger.error(f"Webhook handler error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/bulk-onboard', methods=['POST'])
def webhook_bulk_onboard():
    """Handle webhook requests for bulk team onboarding"""
    try:
        # Get the signature from headers
        signature = request.headers.get('X-Hub-Signature-256')
        
        # Verify signature if secret is configured
        if WEBHOOK_SECRET != 'your-webhook-secret':
            if not verify_webhook_signature(request.data, signature):
                logger.warning("Invalid webhook signature")
                return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse the payload
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        teams_data = payload.get('teams', [])
        if not teams_data:
            return jsonify({'error': 'No teams data provided'}), 400
        
        logger.info(f"Received bulk onboarding request for {len(teams_data)} teams")
        
        def process_bulk_onboarding():
            try:
                # Convert payload to TeamConfig objects
                teams = []
                for team_data in teams_data:
                    team_config = TeamConfig(
                        team_name=team_data.get('name', 'Unknown Team'),
                        repositories=team_data.get('repositories', []),
                        members=team_data.get('members', []),
                        policies=team_data.get('policies'),
                        testing_types=team_data.get('testing_types')
                    )
                    teams.append(team_config)
                
                # Process bulk onboarding
                automation = SnykAutomation()
                results = automation.bulk_onboard_teams(teams)
                
                logger.info(f"Bulk onboarding completed for {len(teams)} teams")
                logger.info(f"Results: {json.dumps(results, indent=2)}")
                
            except Exception as e:
                logger.error(f"Error in bulk onboarding: {e}")
        
        # Process the request asynchronously
        thread = Thread(target=process_bulk_onboarding)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'accepted',
            'message': f'Bulk onboarding request received for {len(teams_data)} teams'
        }), 202
        
    except Exception as e:
        logger.error(f"Bulk webhook handler error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'snyk-automation-webhook'}), 200

@app.route('/webhook/test', methods=['POST'])
def test_webhook():
    """Test endpoint for webhook functionality"""
    payload = request.get_json()
    logger.info(f"Test webhook received: {json.dumps(payload, indent=2)}")
    
    return jsonify({
        'status': 'success',
        'message': 'Test webhook received successfully',
        'received_payload': payload
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting webhook server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
