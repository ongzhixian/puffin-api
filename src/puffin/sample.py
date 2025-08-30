def sample_lambda1(event:dict, context):
    """Example lambda function 2
    Use case:
        (example) This function is used to demonstrate how to handle an AWS Lambda event.
    """

    try:
        print('Example Lambda function 1 triggered with event:', event)
        import psycopg2
        import os

        conn_string = os.environ.get('PUFFIN_CONNECTIONSTRING')

        conn = psycopg2.connect(conn_string)
        print("Connection established")
        cursor = conn.cursor()
        
        # Fetch all rows from table
        cursor.execute("SELECT * FROM app_user;")
        rows = cursor.fetchall()

        # Print all rows
        for row in rows:
            print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

        # Clean up
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as error:
        print(error)
        

def sample_lambda2(event:dict, context):
    """Sample lambda function 2
    Use case:
        (example) This function is used to demonstrate how to handle an AWS Lambda event.
    """

    try:
        print('Example Lambda function 2 triggered with event:', event)
    except Exception as error:
        print(error)
        