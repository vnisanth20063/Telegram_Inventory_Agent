from .database import SessionLocal
from .models import Inventory


def check_inventory(product_id: str):

    db = SessionLocal()

    try:

        product = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == product_id
            )
            .first()
        )

        if not product:
            return (
                f"Product {product_id} "
                f"was not found in the inventory database."
            )

        return (
            f"Product ID: {product.product_id}\n"
            f"Product Name: {product.product_name}\n"
            f"Current Stock: {product.current_stock} units\n"
            f"Daily Demand: {product.daily_demand} units/day\n"
            f"Lead Time: {product.lead_time_days} days\n"
            f"Safety Stock: {product.safety_stock} units"
        )

    finally:
        db.close()


def calculate_replenishment(
    current_stock: int,
    daily_demand: int,
    lead_time_days: int,
    safety_stock: int
):

    reorder_point = (
        daily_demand * lead_time_days
    ) + safety_stock

    if current_stock <= reorder_point:

        suggested_order = (
            reorder_point * 2
        ) - current_stock

        return (
            "REPLENISHMENT REQUIRED\n"
            f"Current stock: {current_stock} units\n"
            f"Reorder point: {reorder_point} units\n"
            f"Suggested order quantity: "
            f"{suggested_order} units"
        )

    return (
        "NO REPLENISHMENT REQUIRED\n"
        f"Current stock: {current_stock} units\n"
        f"Reorder point: {reorder_point} units\n"
        "Current stock is above the reorder point."
    )


def list_low_stock_products():

    db = SessionLocal()

    try:

        products = db.query(Inventory).all()

        low_stock = []

        for product in products:

            reorder_point = (
                product.daily_demand *
                product.lead_time_days
            ) + product.safety_stock

            if product.current_stock <= reorder_point:

                low_stock.append(
                    f"{product.product_id} - "
                    f"{product.product_name} | "
                    f"Stock: {product.current_stock} | "
                    f"Reorder Point: {reorder_point}"
                )

        if not low_stock:

            return (
                "No products currently "
                "require replenishment."
            )

        return "\n".join(low_stock)

    finally:
        db.close()