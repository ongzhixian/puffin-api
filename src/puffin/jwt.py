# Security related Lambdas
# authenticate: Authenticates given credentials and return JWT
# get_user_list: Get list of users.
# add_user: Add user.
# update_user_password: Update user password.
# update_user_status: Update user status (activation/deactivation); consider specific accounts for each scenario.

# Routes planning
# POST  /jwt            -- TODO_post_jwt
# GET   /user           -- TODO_get_user
# POST  /user           -- TODO_add_user
# PATCH /user/password  -- TODO_update_user_password
# PATCH /user/status    -- TODO_update_user_status


import json
import logging
# import os
# import boto3
from jwcrypto.jwk import JWK

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# s3_client = boto3.client('s3')


# ENDPOINT: /authenticate

def post_jwt(event:dict, context):
    """
    Authenticates given credentials and return JWT
    
    Args:
        event (dict): The API Gateway event payload.
        context (object): The Lambda context object.
    
    Returns:
        dict: A response indicating success or failure.
    """
    try:
        # Add your logic here
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'TODO: .'})
        }
    
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
