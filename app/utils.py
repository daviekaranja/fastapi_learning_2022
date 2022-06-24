from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """
    hashes the user password
    :param password:
    :return: hashed password
    """
    return pwd_context.hash(password)


# confirm password
def verify(plain_password, hashed_password):
    """
    compares the two hashed password
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)