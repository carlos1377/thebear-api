import bcrypt
from app.db.models import User as UserModel

# TODO: IS THIS A STATIC METHOD?


def encrypt_password(self, password: str) -> bytes:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def check_password(self, password: str, _id: int) -> bool:
    user = self.db_session.query(
        UserModel).filter_by(id=_id).one_or_none()

    if user is None:
        return False

    check = bcrypt.checkpw(
        password=password.encode(),
        hashed_password=user.password
    )

    return check
