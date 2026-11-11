"""SQLite connection and CRUD helpers for the BikeFlow application."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3

DATABASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = DATABASE_DIR / "bikeflow.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"

VALID_STATUSES = {
    "Registered",
    "Scheduled",
    "In Progress",
    "Waiting for Parts",
    "Completed",
    "Cancelled",
}


def get_connection():
    """Return a connection to the persistent BikeFlow SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    # Enforce foreign-key constraints if foreign keys are added later.
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def database_connection():
    """Yield a connection; commit on success and roll back on error."""
    connection = get_connection()
    try:
        yield connection
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    """Create the database and tables if they do not already exist."""
    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        with database_connection() as connection:
            connection.executescript(schema)
    except (OSError, sqlite3.Error) as error:
        raise RuntimeError(f"Could not initialize BikeFlow database: {error}") from error


def create_repair_order(
    customer_name,
    customer_phone,
    bicycle_type,
    bicycle_brand,
    problem_description,
):
    """Insert a repair order and return its newly assigned ID."""
    sql = """
        INSERT INTO repair_orders (
            customer_name,
            customer_phone,
            bicycle_type,
            bicycle_brand,
            problem_description
        ) VALUES (?, ?, ?, ?, ?)
    """
    values = (
        customer_name,
        customer_phone,
        bicycle_type,
        bicycle_brand,
        problem_description,
    )

    try:
        with database_connection() as connection:
            cursor = connection.execute(sql, values)
            return cursor.lastrowid
    except sqlite3.IntegrityError as error:
        raise ValueError(f"Invalid repair order data: {error}") from error


def get_all_repair_orders():
    """Return all repair orders as dictionaries, newest first."""
    with database_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM repair_orders ORDER BY created_at DESC, id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_repair_order_by_id(order_id):
    """Return one repair order as a dictionary, or None if not found."""
    with database_connection() as connection:
        row = connection.execute(
            "SELECT * FROM repair_orders WHERE id = ?",
            (order_id,),
        ).fetchone()
        return dict(row) if row else None

def search_repair_orders_by_customer(customer_name):
    """Find repair orders matching a customer name."""
    with database_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM repair_orders
            WHERE customer_name LIKE ?
            ORDER BY created_at DESC, id DESC
            """,
            (f"%{customer_name}%",),
        ).fetchall()

        return [dict(row) for row in rows]


def update_repair_order_status(order_id, new_status):
    """Update an order status; return True if a row was updated."""
    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status. Choose one of: {', '.join(sorted(VALID_STATUSES))}"
        )

    try:
        with database_connection() as connection:
            cursor = connection.execute(
                "UPDATE repair_orders SET status = ? WHERE id = ?",
                (new_status, order_id),
            )
            return cursor.rowcount > 0
    except sqlite3.IntegrityError as error:
        raise ValueError(f"Could not update repair order: {error}") from error


if __name__ == "__main__":
    initialize_database()
    print(f"BikeFlow database is ready: {DATABASE_PATH}")
