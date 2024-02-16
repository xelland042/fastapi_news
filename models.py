from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./database.sqlite3', connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(engine)

Base = declarative_base()
metadata = Base.metadata


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())


class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String, unique=True)
    first_name = Column(String, default=None, nullable=True)
    last_name = Column(String, default=None, nullable=True)
    email = Column(String, unique=True)
    hashed_password = Column(String, default=None, nullable=True)

    def __repr__(self):
        return f'{self.id} - {self.username}'


class News(BaseModel):
    __tablename__ = 'new'

    title = Column(String, unique=True)
    content = Column(Text)
    author = Column(ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.id} - {self.title} - {self.author}'
