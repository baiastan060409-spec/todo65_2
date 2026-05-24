from db.main_db import get_connection
from typing import List, Dict, Any


def add_item(name: str, quantity: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, quantity) VALUES (?, ?)",
        (name.strip(), quantity.strip())
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id


def get_all_items() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items ORDER BY created_at DESC")
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]


def get_bought_items() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE is_bought = 1 ORDER BY created_at DESC")
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]


def get_not_bought_items() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE is_bought = 0 ORDER BY created_at DESC")
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]


def toggle_bought(item_id: int, is_bought: bool) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET is_bought = ? WHERE id = ?",
        (1 if is_bought else 0, item_id)
    )
    conn.commit()
    conn.close()


def delete_item(item_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def get_bought_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items WHERE is_bought = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return count