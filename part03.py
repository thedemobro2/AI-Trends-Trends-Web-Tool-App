# backend/services/inventory_service.py
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
from ..models import models, schemas

def process_csv_upload(db: Session, df: pd.DataFrame, filename: str):
    """
    Processes the uploaded CSV, normalizes data, stores a snapshot,
    and calculates inventory changes from the previous snapshot.
    """
    # 1. Data Cleaning & Normalization
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    if 'condition' in df.columns:
        df['condition'] = df['condition'].astype(str).str.lower().str.strip()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['item_id']) # Assuming 'item_id' is a critical identifier

    # 2. Store current snapshot
    new_upload = models.UploadLog(filename=filename, upload_date=datetime.utcnow())
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)

    current_snapshot_items = []
    for index, row in df.iterrows():
        part = models.Part(
            item_id=str(row['item_id']),
            name=str(row.get('name', 'N/A')),
            description=str(row.get('description', 'N/A')),
            condition=str(row.get('condition', 'N/A')),
            upload_log_id=new_upload.id
        )
        db.add(part)
        db.flush() # To get part.id before adding price history

        price_history = models.PriceHistory(
            part_id=part.id,
            price=row.get('price'),
            recorded_date=new_upload.upload_date
        )
        db.add(price_history)
        current_snapshot_items.append(part.item_id)
    db.commit()

    # 3. Inventory Change Tracking (against previous upload)
    previous_upload = db.query(models.UploadLog).filter(
        models.UploadLog.id != new_upload.id
    ).order_by(models.UploadLog.upload_date.desc()).first()

    new_items_count = 0
    removed_items_count = 0
    unchanged_items_count = 0
    sold_items_count = 0

    if previous_upload:
        previous_snapshot_items_query = db.query(models.Part.item_id).filter(
            models.Part.upload_log_id == previous_upload.id
        ).all()
        previous_snapshot_items = {item.item_id for item in previous_snapshot_items_query}

        # New items: in current but not in previous
        new_items_count = len(set(current_snapshot_items) - previous_snapshot_items)
        
        # Sold items: in previous but not in current
        sold_items_count = len(previous_snapshot_items - set(current_snapshot_items))

        # Unchanged items
        unchanged_items_count = len(set(current_snapshot_items).intersection(previous_snapshot_items))

    # Update UploadLog with counts (optional, but good for tracking)
    new_upload.new_items_count = new_items_count
    new_upload.removed_items_count = removed_items_count # Removed and sold are synonymous here for now
    new_upload.sold_items_count = sold_items_count
    new_upload.unchanged_items_count = unchanged_items_count
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)

    return schemas.UploadLog.from_orm(new_upload)

def get_latest_inventory_changes(db: Session):
    """
    Retrieves the latest inventory change summary.
    """
    latest_upload = db.query(models.UploadLog).order_by(models.UploadLog.upload_date.desc()).first()
    if not latest_upload:
        return None

    # Identify aging items (3+ months in stock)
    three_months_ago = datetime.utcnow() - timedelta(days=90)
    aging_items_count = db.query(models.Part.item_id).filter(
        models.Part.upload_log_id <= latest_upload.id, # Consider items from current and older snapshots
        ~models.Part.item_id.in_(
            db.query(models.Part.item_id).filter(
                models.Part.upload_log_id > latest_upload.id
            ).subquery()
        ) if latest_upload.id is not None else True, # Exclude items that appeared in newer uploads if this isn't the latest
        models.Part.upload_log.has(upload_date__lt=three_months_ago) # Check if their initial upload was 3+ months ago
    ).distinct().count()

    # This aging logic needs refinement to truly track if an *individual item* has been in stock for 3 months
    # A more robust approach would be to track the `first_seen_date` for each `item_id` in the `parts` table.
    # For MVP, we'll simplify: count items from uploads older than 3 months that are still in the *latest* snapshot.
    
    # Simpler MVP aging logic: count items from the current snapshot whose initial upload was > 3 months ago
    current_items_ids = db.query(models.Part.item_id).filter(models.Part.upload_log_id == latest_upload.id).all()
    current_items_ids = [item.item_id for item in current_items_ids]

    aging_items_count = 0
    if current_items_ids:
        for item_id in current_items_ids:
            first_upload = db.query(models.UploadLog).join(models.Part).filter(
                models.Part.item_id == item_id
            ).order_by(models.UploadLog.upload_date.asc()).first()
            if first_upload and (datetime.utcnow() - first_upload.upload_date).days >= 90:
                aging_items_count += 1


    return schemas.InventoryChanges(
        new_items_count=latest_upload.new_items_count,
        sold_items_count=latest_upload.sold_items_count,
        aging_items_count=aging_items_count,
        unchanged_items_count=latest_upload.unchanged_items_count
    )
