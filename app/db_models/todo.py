from datetime import datetime,timedelta
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Float
# from app.db.base_class import Base




class ToDo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    isComplete = Column((Boolean(), default=False)
    dateDue = Column(DateTime, default=datetime.now + timedelta(days=30))
    dateCreate = Column(Integer, index=True)
    dateUpdate = Column(Integer, default=d)
    dateComplete = Column(Integer, index=True)
    # id = Column(Integer, primary_key=True, index=True)
    # full_name = Column(String, index=True)
    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # is_active = Column(Boolean(), default=True)
    # is_superuser = Column(Boolean(), default=False)