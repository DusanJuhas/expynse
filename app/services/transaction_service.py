from app.db.database import get_connection
from app.services.category_service import apply_category_rules


def insert_transactions(transactions):
    conn = get_connection()
    cur = conn.cursor()

    for tx in transactions:
        tx["user_category"] = apply_category_rules(tx)

        try:
            cur.execute("""
            INSERT INTO transactions (
                date, amount, currency,
                bank_category, transaction_type,
                counter_account, counter_name,
                transaction_code, description, user_category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tx["date"], tx["amount"], tx["currency"],
                tx["bank_category"], tx["transaction_type"],
                tx["counter_account"], tx["counter_name"],
                tx["transaction_code"], tx["description"], tx["user_category"]
            ))

        except Exception:
            # duplicate → ignore
            continue

    conn.commit()
    conn.close()


def get_all_transactions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows