from sqlalchemy.orm import DeclarativeBase

from extension import SQLAlchemy


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
