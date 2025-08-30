def sample_lambda1(event:dict, context):
    """Example lambda function 2
    Use case:
        (example) This function is used to demonstrate how to handle an AWS Lambda event.
    """

    try:
        print('Example Lambda function 1 triggered with event:', event)
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
        