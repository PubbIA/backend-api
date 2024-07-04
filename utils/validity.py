import re

def is_gmail_password_structure(password: str) -> bool:
    """
    Check if the given password follows a specific structure.

    Parameters:
    - password (str): The password string to be validated.

    Returns:
    - bool: True if the password follows the structure, False otherwise.

    The password structure is defined as follows:
    - It must be a string.
    - It must consist of four segments separated by spaces.
    - Each segment must be exactly four characters long.

    Example:
    >>> is_password_structure("abcd efgh ijkl mnop")
    True
    >>> is_password_structure("abcd efgh ijkl")
    False
    >>> is_password_structure("abc defg ijkl mnop")
    False
    """
    if not isinstance(password, str):
        return False
    return all([len(item) == 4 for item in password.split(" ")]) if len(password.split(" ")) == 4 else False


def is_valid_email(email):
    """
    Check if the email address has a valid structure.

    Parameters:
    - email (str): The email address to validate.

    Returns:
    - bool: True if the email address is valid, False otherwise.
    """
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Check if the email matches the pattern
    return bool(re.match(pattern, email))

def is_valid_password(password):
    """
    Check if a password meets the following criteria:
    - Contains at least one lowercase character
    - Contains at least one uppercase character
    - Contains at least one digit
    - Has a minimum length of 8 characters
    
    Args:
        password (str): The password to be checked.
        
    Returns:
        bool: True if the password meets all criteria, False otherwise.
        
    Examples:
        >>> is_valid_password("Abcd1234")
        True
        >>> is_valid_password("abcd1234")
        False
        >>> is_valid_password("ABCD1234")
        False
        >>> is_valid_password("Abcd")
        False
        >>> is_valid_password("12345678")
        False
    """
    if (
        re.search(r"[a-z]", password) and  # At least one lowercase character
        re.search(r"[A-Z]", password) and  # At least one uppercase character
        re.search(r"\d", password) and     # At least one digit
        len(password) >= 8                 # Length >= 8
    ):
        return True
    else:
        return False

