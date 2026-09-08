import os
from dotenv import load_dotenv
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "wipey"}

    id: Mapped[int] = mapped_column(primary_key=True)
    slack_user_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    encrypted_token: Mapped[str] = mapped_column(String(200), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

Base.metadata.create_all(engine)

class DatabaseMethods:
    def __init__(self, session):
        self.session = session

    def add_user(self, slack_user_id, encrypted_token, is_admin=False):
        new_user = User(slack_user_id=slack_user_id, encrypted_token=encrypted_token, is_admin=is_admin)
        try:
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(str(e.orig))

    def get_user(self, slack_user_id):
        stmt = select(User).where(User.slack_user_id == slack_user_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def update_user_token(self, slack_user_id, new_encrypted_token):
        if not (user:= self.get_user(slack_user_id)):
            raise ValueError(f"User with Slack ID: {slack_user_id} not found")

        user.encrypted_token = new_encrypted_token
        self.session.commit()
        return user


    def delete_user(self, slack_user_id):
        if not (user:= self.get_user(slack_user_id)):
            raise ValueError(f"User with Slack ID: {slack_user_id} not found")

        self.session.delete(user)
        self.session.commit()


    