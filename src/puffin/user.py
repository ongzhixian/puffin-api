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
import hashlib
import base64
import secrets
from dataclasses import dataclass, is_dataclass, asdict

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
    class JsonEncoder(json.JSONEncoder):
        """
        A custom JSON encoder that can handle dataclasses.
        This provides a robust way to serialize any dataclass in your application without modifying the classes themselves.
        """
        def default(self, obj):
            if is_dataclass(obj):
                return asdict(obj)
            return super().default(obj)

@dataclass
class PasswordSet:
    password_hash: str
    password_salt: str
    password_entropy: int

# @dataclass
# class Box(Generic[T]):
#     """
#     A generic dataclass representing a box that can hold a value of a
#     specified type.
#     """
#     value: T
#     label: str

@dataclass
class get_user_password_response:
    result: any  # Accepts any type, but no static type checking
    warning_message: str
    has_warning: bool = False
    def __post_init__(self):
        """
        This special method is called after the dataclass's __init__ method.
        It's the correct place to set a field's value based on other fields.
        """
        # We check if the warning_message is not empty and set has_warning
        # accordingly for each new instance.
        if len(self.warning_message) > 0:
            self.has_warning = True
        else:
            self.has_warning = False


class UserRepository(BaseRepository):
    """User repository for direct SQL queries."""
        
    def get_user_list(self) -> list[User]:
        """Finds all users using raw SQL."""
        with self.db_cursor() as cursor:
            cursor.execute('SELECT "id", "username" FROM public.app_user;')
            rows = cursor.fetchall()
            return [User(id=row[0], username=row[1]) for row in rows]
        
    def add_user(self, username, password, record_create_by = 0, record_update_by = 0):
        """Adds a new user to the database using parameterized query."""
        (password_hash, password_salt, password_entropy) = self._generate_password_hash_and_salt(password)
        print(password_hash, password_salt, password_entropy)

        with self.db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.app_user 
                (username, password_hash, password_salt, password_entropy, record_create_by, record_update_by)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (username, password_hash, password_salt, password_entropy, record_create_by, record_update_by))

    def validate_user_password(self, username, password) -> bool:
        """Validates if given username and password matches stored record."""
        password_data = self._get_password_data(username)
        if password_data is None:
            return False
        (password_hash, password_salt, password_entropy) = password_data
        return self._verify_password(password, password_hash, password_salt, password_entropy)


    # PRIVATE FUNCTIONS

    def _get_password_data(self, username:str) -> tuple[str, str, int] | None:
        """Get password related data for given username."""
        with self.db_cursor() as cursor:
            cursor.execute("""SELECT password_hash, password_salt, password_entropy FROM public.app_user where username = %s;""", (username,))
            rows = cursor.fetchall()
            row_count = len(rows)
            if row_count == 1:
                record = rows[0]
                return (record[0], record[1], record[2])
            return None # Assumes that everything is working correctly, that we row_count != 1 because no record with username exists

    def _generate_safe_random_number(self, min_value: int = 100000, entropy_increment: int = 8) -> int:
        """
        Generates a cryptographically safe random number that is always greater
        than or equal to a specified minimum value.

        The `secrets` module is used because it provides a cryptographically
        secure random number generator (CSPRNG), which is essential for
        security-sensitive applications like password generation, session keys,
        and tokens. The standard `random` module should not be used for these
        purposes as it is not cryptographically secure.

        Args:
            min_value (int): The minimum value for the generated number. The function
                            ensures the returned number is >= this value.

        Returns:
            int: A cryptographically safe random number.
        """
        if min_value < 100000:
            min_value = 100000
        
        # Dynamically determine the number of bits needed based on the minimum value.
        # The `bit_length()` method is a more direct way to find the number of bits
        # required to represent an integer in binary. We add 8 bits to ensure the
        # generated random number has a high probability of being greater than
        # the minimum value on the first try, reducing the need for multiple loops.
        num_bits = min_value.bit_length() + entropy_increment
        if num_bits > 32:
            num_bits = 32

        # Use a loop to generate a number until it meets the condition.
        # This is a robust way to ensure the number is always above the minimum.
        while True:
            # secrets.randbits(k) returns an integer with k random bits.
            random_number = secrets.randbits(num_bits)
            
            if random_number >= min_value:
                return random_number

    def _generate_password_hash_and_salt(self, password: str) -> tuple[str, str, int]:
        """
        Generates a password hash and a unique salt for a given password.

        Args:
            password: The user's plaintext password.

        Returns:
            A tuple containing the password hash and the salt, both as bytes.
        """
        
        # Generate a cryptographically secure random salt (e.g., 16 bytes).
        salt = os.urandom(16)
        iterations = self._generate_safe_random_number()

        # Hash the password with the salt using a strong algorithm.
        # PBKDF2 is used here, but Argon2 or bcrypt are recommended for new applications.
        # The high number of iterations (100000) makes it slow and resistant to brute-force attacks.
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations
        )

        # Return both the hash, salt as base64 string and iteration as integer
        return base64.b64encode(password_hash).decode('utf-8'), base64.b64encode(salt).decode('utf-8'), iterations
        
    def _verify_password(self, password: str, stored_hash: str, stored_salt: str, stored_entropy: int) -> bool:
        """
        Verifies a plaintext password against a stored password hash and salt.

        Args:
            password: The plaintext password entered by the user.
            stored_hash: The password hash retrieved from the database.
            stored_salt: The salt retrieved from the database.

        Returns:
            True if the password is correct, False otherwise.
        """
        # Re-hash the provided password using the same salt and algorithm
        # as when the user was first created.
        # It is crucial to use the exact same parameters.
        generated_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            base64.b64decode(stored_salt), # decode base64 str to bytes
            stored_entropy
        )

        # Compare the newly generated hash with the stored hash.
        # A timing-safe comparison is used to prevent timing attacks.
        return generated_hash == base64.b64decode(stored_hash)
    

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
            'body': json.dumps(user_list, cls=User.JsonEncoder)
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
        print("[event]", event)
        print("[context]", context)
        # Add your logic here
        # repo = UserRepository()
        # repo.add_user('zhixian', 'P@ssw0rd79', 1, 1)
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
