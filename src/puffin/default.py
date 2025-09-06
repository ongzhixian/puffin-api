# API Lambdas
# ut_get_favicon_ico: Redirect to favicon.ico URL hosted on S3 (accessible via CloudFront CDN)

import logging
from typing import Dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_favicon_ico(event: Dict, context: object) -> Dict:
    """
    Redirects API Gateway requests to the application's favicon.ico file hosted on S3.

    This function is an AWS Lambda handler that returns a 302 HTTP status code
    with a 'Location' header pointing to the favicon.ico file's URL. This
    approach allows a custom domain API Gateway endpoint to serve the favicon
    from a dedicated CDN (CloudFront) backed by S3, leveraging S3's low-cost
    storage and CloudFront's global, high-performance delivery.

    The 302 (Found) redirect is used to indicate a temporary redirection. This is
    beneficial because it tells clients (like web browsers) to follow the redirect
    to get the file but not to cache the new location. This allows for future
    changes to the favicon's URL without a risk of clients being stuck with a
    stale, cached location.

    Args:
        event (Dict): The API Gateway event object containing request details.
        context (object): The Lambda context object, which provides methods and
                          properties about the invocation, function, and execution environment.

    Returns:
        Dict: An API Gateway-compatible response dictionary with a 302 status code
              and the 'Location' header set to the favicon URL.
    """
    # Define the permanent URL of the favicon.ico file, hosted via CloudFront
    # for optimal performance and global accessibility.
    FAVICON_URL = "https://puffin.readyperfectly.com/favicon.ico"

    # Construct the API Gateway response for a temporary redirect (302).
    # This status code prompts the client to follow the URL in the 'Location' header.
    # We use a 302 redirect so that the browser does not permanently cache the
    # redirection, allowing for easier updates to the favicon's location later.
    return {
        "statusCode": 302,
        "headers": {
            "Location": FAVICON_URL
        }
    }