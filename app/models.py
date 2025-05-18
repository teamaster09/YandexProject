from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    context = Column(Text)  # JSON-строка с контекстом пользователя


class UserFile(Base):
    __tablename__ = 'user_files'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    file_type = Column(String(20))  # 'image' или 'music'
    file_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)