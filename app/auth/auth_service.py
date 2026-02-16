from app.models.users import User
from app.core.security import verify_password


def validate_user(db, username: str, password: str):
    all_users = db.query(User.username).all()
    print(f"Searching for: '{username}'")
    print(f"Existing users in DB: {all_users}")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    print("user found:", user.username)
    return user


def get_current_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user
