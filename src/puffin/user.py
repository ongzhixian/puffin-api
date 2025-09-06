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
from dataclasses import dataclass

# import boto3
import psycopg2

from database import BaseRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# s3_client = boto3.client('s3')


@dataclass
class User:
    id: int
    username: str

class UserRepository(BaseRepository):
    """User repository for direct SQL queries."""
        
    def get_user_list(self) -> list[User]:
        """Finds all users using raw SQL."""
        with self.db_cursor() as cursor:
            cursor.execute('SELECT "id", "username" FROM public.app_user;')
            rows = cursor.fetchall()
            return [User(id=row[0], username=row[1]) for row in rows]

    # EXAMPLES

    def _get_all_generic(self) -> list[tuple]:
        """Example of generic Finds all users using raw SQL."""
        with self.db_cursor() as cursor:
            cursor.execute("SELECT * FROM app_user;")
            rows = cursor.fetchall()
            return rows            

    # def get_by_id(self, user_id: int) -> Dict[str, Any] | None:
    #     """Finds a user by ID using raw SQL."""
    #     with get_db_cursor() as cur:
    #         cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    #         user = cur.fetchone()
    #         if user:
    #             # Return a dictionary for consistency
    #             return dict(zip([desc[0] for desc in cur.description], user))
    #         return None

    # def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
    #     """Creates a new user and returns the created record."""
    #     with get_db_cursor() as cur:
    #         # We explicitly define columns to prevent SQL injection with a dictionary
    #         cur.execute(
    #             "INSERT INTO users (name, email, hashed_password) VALUES (%s, %s, %s) RETURNING id, name, email",
    #             (user_data["name"], user_data["email"], user_data["hashed_password"])
    #         )
    #         new_user = cur.fetchone()
    #         return dict(zip([desc[0] for desc in cur.description], new_user))

    # def get_by_email(self, email: str) -> Dict[str, Any] | None:
    #     """Finds a user by email."""
    #     with get_db_cursor() as cur:
    #         cur.execute("SELECT id, name, email FROM users WHERE email = %s", (email,))
    #         user = cur.fetchone()
    #         if user:
    #             return dict(zip([desc[0] for desc in cur.description], user))
    #         return None

# ENDPOINT: /user

def get_user_list(event:dict, context) -> list[User]:
    """
    Authenticates given credentials and return JWT
    
    Args:
        event (dict): The API Gateway event payload.
        context (object): The Lambda context object.
    
    Returns:
        dict: A response indicating success or failure.
    """
    try:
        repo = UserRepository()
        user_list = repo.get_user_list()
        return {
            'statusCode': 200,
            'body': json.dumps(user_list)
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
