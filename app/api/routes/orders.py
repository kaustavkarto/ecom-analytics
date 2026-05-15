from fastapi import APIRouter, HTTPException
from app.models.order import OrderCreate, OrderStatusUpdate
from app.db.mysql import get_mysql_connection

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(order: OrderCreate):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (order.user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        # Calculate total amount
        total_amount = 0
        items_data = []
        for item in order.items:
            cursor.execute("SELECT price, stock_quantity FROM products WHERE id = %s", (item.product_id,))
            product = cursor.fetchone()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product[1] < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
            total_amount += product[0] * item.quantity
            items_data.append((item.product_id, item.quantity, product[0]))

        # Insert order
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
            (order.user_id, round(total_amount, 2))
        )
        order_id = cursor.lastrowid

        # Insert order items
        for product_id, quantity, unit_price in items_data:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                (order_id, product_id, quantity, unit_price)
            )

        conn.commit()
        return {"message": "Order created successfully", "order_id": order_id, "total_amount": round(total_amount, 2)}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/{order_id}")
def get_order(order_id: int):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
        items = cursor.fetchall()
        order['items'] = items
        return order

    finally:
        cursor.close()
        conn.close()


@router.patch("/{order_id}/status")
def update_order_status(order_id: int, update: OrderStatusUpdate):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM orders WHERE id = %s", (order_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Order not found")

        cursor.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (update.status.value, order_id)
        )
        conn.commit()
        return {"message": "Order status updated", "order_id": order_id, "status": update.status}

    finally:
        cursor.close()
        conn.close()