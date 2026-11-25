import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

DB_PATH = Path("prices.db")


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    target_price REAL NOT NULL,
                    css_selector TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    checked_at TEXT NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def add_product(self, name: str, url: str, target_price: float, css_selector: str) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO products (name, url, target_price, css_selector, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, url, target_price, css_selector, datetime.now().isoformat()),
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_products(self) -> List[Tuple]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, url, target_price, css_selector FROM products")
            return cursor.fetchall()

    def record_price(self, product_id: int, price: float) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO price_history (product_id, price, checked_at)
                VALUES (?, ?, ?)
                """,
                (product_id, price, datetime.now().isoformat()),
            )
            conn.commit()

    def get_price_history(self, product_id: int) -> List[float]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT price FROM price_history WHERE product_id = ? ORDER BY checked_at ASC",
                (product_id,),
            )
            return [row[0] for row in cursor.fetchall()]

    def delete_product(self, product_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return cursor.rowcount > 0
