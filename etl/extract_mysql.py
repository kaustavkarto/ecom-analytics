from app.db.mysql import get_mysql_connection

def extract_orders():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                o.id as order_id,
                o.user_id,
                o.total_amount,
                o.status,
                o.created_at,
                u.city,
                oi.product_id,
                oi.quantity,
                oi.unit_price,
                p.name as product_name,
                p.category
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
        """)
        rows = cursor.fetchall()
        print(f"Extracted {len(rows)} order rows from MySQL")
        return rows

    finally:
        cursor.close()
        conn.close()