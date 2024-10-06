from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hashes the password using bcrypt

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the password using bcrypt
    Args:
        plain_password (str): The plain password
        hashed_password (str): The hashed password
    Returns:
        bool: True if the password is valid, False otherwise
    """
    return password_context.verify(plain_password, hashed_password)
