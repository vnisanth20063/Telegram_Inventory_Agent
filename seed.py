from app.database import Base, engine, SessionLocal
from app.models import Inventory


# Create tables
Base.metadata.create_all(
    bind=engine
)


db = SessionLocal()


products = [
    Inventory(
        product_id="P1001",
        product_name="Rice",
        current_stock=120,
        daily_demand=30,
        lead_time_days=5,
        safety_stock=50
    ),

    Inventory(
        product_id="P1002",
        product_name="Sugar",
        current_stock=500,
        daily_demand=40,
        lead_time_days=4,
        safety_stock=100
    ),

    Inventory(
        product_id="P1003",
        product_name="Wheat",
        current_stock=80,
        daily_demand=20,
        lead_time_days=6,
        safety_stock=40
    )
]


for product in products:

    existing = (
        db.query(Inventory)
        .filter(
            Inventory.product_id
            == product.product_id
        )
        .first()
    )

    if not existing:

        db.add(product)


db.commit()

db.close()


print("Inventory data inserted successfully.")