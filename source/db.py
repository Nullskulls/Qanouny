import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import String
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
    token: Mapped[str] = mapped_column(String(200), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

Base.metadata.create_all(engine)