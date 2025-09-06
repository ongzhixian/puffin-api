# Security related Lambdas
# authenticate: Authenticates given credentials and return JWT
# get_user_list: Get list of users.
# add_user: Add user.
# update_user_password: Update user password.
# update_user_status: Update user status (activation/deactivation); consider specific accounts for each scenario.

# Routes planning
# GET   /user           -- TODO_get_user
# POST  /user           -- TODO_add_user
# PATCH /user/password  -- TODO_update_user_password
# PATCH /user/status    -- TODO_update_user_status


import json
import logging
import os
# import os
# import boto3
import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# s3_client = boto3.client('s3')


# ENDPOINT: /user

def get_user_list(event:dict, context):
    """
    Authenticates given credentials and return JWT
    
    Args:
        event (dict): The API Gateway event payload.
        context (object): The Lambda context object.
    
    Returns:
        dict: A response indicating success or failure.
    """
    try:
        PUFFIN_DB_CONNECTION_STRING = os.environ.get('PUFFIN_DB_CONNECTION_STRING', '')

        db = psycopg2.connect(PUFFIN_DB_CONNECTION_STRING)
        print("Connection established")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM app_user;")
        rows = cursor.fetchall()

        for row in rows:
            print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

        cursor.close()
        db.close()

        # Add your logic here
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'TODO: OK TAKE 2'})
        }
    
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
    
def add_user(event:dict, context):
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
    

# ENDPOINT: /user/password

def TODO_update_user_password(event:dict, context):
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
    

# ENDPOINT: /user/status

def TODO_update_user_status(event:dict, context):
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
