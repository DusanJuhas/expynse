from app.db.database import get_connection

def search_transactions(query):
    conn = get_connection()
    cur = conn.cursor()

    # Let FTS tokenize naturally
    safe_query = query.strip()

    cur.execute("""
        SELECT t.*
        FROM transactions_fts
        JOIN transactions t ON t.id = transactions_fts.rowid
        WHERE transactions_fts MATCH ?
    """, (safe_query,))

    rows = cur.fetchall()
    conn.close()
    return rows