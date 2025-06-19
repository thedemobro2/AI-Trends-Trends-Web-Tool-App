# backend/models/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UploadLog(Base):
    __tablename__ = "upload_logs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    new_items_count = Column(Integer, default=0)
    removed_items_count = Column(Integer, default=0)
    sold_items_count = Column(Integer, default=0)
    unchanged_items_count = Column(Integer, default=0)

    parts = relationship("Part", back_populates="upload_log")

class Part(Base):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, unique=False, index=True) # item_id can repeat across snapshots
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    upload_log_id = Column(Integer, ForeignKey("upload_logs.id"))

    upload_log = relationship("UploadLog", back_populates="parts")
    price_history = relationship("PriceHistory", back_populates="part")

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("parts.id"))
    price = Column(Float, nullable=True)
    recorded_date = Column(DateTime, default=datetime.utcnow)

    part = relationship("Part", back_populates="price_history")
