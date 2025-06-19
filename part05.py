# backend/models/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UploadLogBase(BaseModel):
    filename: str
    upload_date: datetime

class UploadLogCreate(UploadLogBase):
    pass

class UploadLog(UploadLogBase):
    id: int
    new_items_count: int
    removed_items_count: int
    sold_items_count: int
    unchanged_items_count: int

    class Config:
        orm_mode = True

class PartBase(BaseModel):
    item_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[str] = None

class PartCreate(PartBase):
    upload_log_id: int

class Part(PartBase):
    id: int
    upload_log_id: int

    class Config:
        orm_mode = True

class PriceHistoryBase(BaseModel):
    price: Optional[float] = None
    recorded_date: datetime

class PriceHistoryCreate(PriceHistoryBase):
    part_id: int

class PriceHistory(PriceHistoryBase):
    id: int
    part_id: int

    class Config:
        orm_mode = True

class InventoryChanges(BaseModel):
    new_items_count: int
    sold_items_count: int
    aging_items_count: int
    unchanged_items_count: int
