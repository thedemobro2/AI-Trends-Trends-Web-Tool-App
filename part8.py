# db/schema.sql
CREATE TABLE IF NOT EXISTS upload_logs (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    new_items_count INTEGER DEFAULT 0,
    removed_items_count INTEGER DEFAULT 0,
    sold_items_count INTEGER DEFAULT 0,
    unchanged_items_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS parts (
    id SERIAL PRIMARY KEY,
    item_id VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    description TEXT,
    condition VARCHAR(255),
    upload_log_id INTEGER NOT NULL,
    FOREIGN KEY (upload_log_id) REFERENCES upload_logs (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    part_id INTEGER NOT NULL,
    price NUMERIC,
    recorded_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (part_id) REFERENCES parts (id) ON DELETE CASCADE
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_parts_item_id ON parts (item_id);
CREATE INDEX IF NOT EXISTS idx_parts_upload_log_id ON parts (upload_log_id);
CREATE INDEX IF NOT EXISTS idx_price_history_part_id ON price_history (part_id);
CREATE INDEX IF NOT EXISTS idx_upload_logs_upload_date ON upload_logs (upload_date DESC);
