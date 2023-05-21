from passlib.context import CryptContext

# Setting the default hashing algorithm to passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hasher(password: str):
    return pwd_context.hash(password)


# Verify that the plain password is equal to the hashed password
def verify_pass(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)
