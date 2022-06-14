from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "postas"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullabe=False)
    published = Column(Boolean, server_default=True)
