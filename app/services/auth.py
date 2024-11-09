import re


def validate_password(password: str):
    """
    Validate the given password against security criteria.

    This function checks if the password meets the following requirements:
    - At least 8 characters long
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one digit
    - Contains at least one special character from !@#$%^&*(),.?":{}|<>

    Args:
        password (str): The password to validate.

    Returns:
        str: The validated password if it meets all criteria.

    Raises:
        ValueError: If the password does not meet any of the specified criteria.
    """
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long')

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter')

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter')

    # Check for at least one digit
    if not re.search(r'\d', password):
        raise ValueError('Password must contain at least one digit')

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError('Password must contain at least one special character')

    return password
