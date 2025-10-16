from passlib.context import CryptContext


class PasswordHandler:
    password_context = CryptContext(schemes=["argon2"], deprecated="auto")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PasswordHandler.password_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordHandler.password_context.verify(plain_password, hashed_password)
