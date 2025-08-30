# Business logic related lambdas
# get_account_list: Fetches a list of financial accounts for the authenticated user from the Neon database.
# get_account_transaction_list: Retrieves the details and transaction history for a specific account.
# add_account_transaction: Inserts a new transaction record into the database.
# update_account_transaction: Modifies an existing transaction.
# delete_account_transaction: Removes a transaction record.

import json
import logging
# import os
# import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# s3_client = boto3.client('s3')

def TODO_get_account_list(event:dict, context):
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
    
def TODO_get_account_transaction_list(event:dict, context):
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
    
def TODO_add_account_transaction(event:dict, context):
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

def TODO_update_account_transaction(event:dict, context):
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
    
def TODO_delete_account_transaction(event:dict, context):
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

def main():
    import psycopg2

    conn_string = ''

    conn = psycopg2.connect(conn_string)
    print("Connection established")
    cursor = conn.cursor()
    
    # Fetch all rows from table
    cursor.execute("SELECT * FROM app_user;")
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))


    # # Drop previous table of same name if one exists
    # cursor.execute("DROP TABLE IF EXISTS inventory;")
    # print("Finished dropping table (if existed)")

    # # Create a table
    # cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    # print("Finished creating table")

    # # Insert some data into the table
    # cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
    # cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
    # cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
    # print("Inserted 3 rows of data")

    # Clean up
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()