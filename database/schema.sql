-- BikeFlow database schema
-- SQLite database: bikeflow.db

CREATE TABLE IF NOT EXISTS repair_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL CHECK (length(trim(customer_name)) > 0),
    customer_phone TEXT NOT NULL CHECK (length(trim(customer_phone)) > 0),
    bicycle_type TEXT NOT NULL CHECK (length(trim(bicycle_type)) > 0),
    bicycle_brand TEXT NOT NULL CHECK (length(trim(bicycle_brand)) > 0),
    problem_description TEXT NOT NULL CHECK (length(trim(problem_description)) > 0),
    status TEXT NOT NULL DEFAULT 'Registered'
        CHECK (status IN (
            'Registered',
            'Scheduled',
            'In Progress',
            'Waiting for Parts',
            'Completed',
            'Cancelled'
        )),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Record the history of repair order status changes
CREATE TABLE IF NOT EXISTS status_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    old_status TEXT,
    new_status TEXT NOT NULL,
    changed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id)
        REFERENCES repair_orders(id)
        ON DELETE CASCADE
);