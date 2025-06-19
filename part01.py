# backend/main.py
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from .dependencies import get_db
from .services import inventory_service
from .models import models, schemas
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload-csv/", response_model=schemas.UploadLog)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and process a CSV file containing inventory data.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")
    
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    upload_log = inventory_service.process_csv_upload(db, df, file.filename)
    return upload_log

@app.get("/inventory-changes/", response_model=schemas.InventoryChanges)
def get_inventory_changes(db: Session = Depends(get_db)):
    """
    Retrieve counts of new, aging, and sold inventory items.
    """
    changes = inventory_service.get_latest_inventory_changes(db)
    if not changes:
        raise HTTPException(status_code=404, detail="No inventory data found to calculate changes.")
    return changes
