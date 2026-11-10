
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from pymongo import MongoClient

# Connect to the existing MongoDB database.
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

# Create the output directory.
output_dir = Path("integration")
output_dir.mkdir(exist_ok=True)

print("\nSTEP 1: EXPORT PRODUCT INFORMATION")

# Export products without modifying MongoDB.
products = db.products.find(
    {},
    {"_id": 0, "product_id": 1, "name": 1, "category_id": 1}
)

product_count = 0

with (output_dir / "mongodb_products.csv").open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow(["product_id", "name", "category_id"])

    for product in products:
        writer.writerow([
            product["product_id"],
            product.get("name", ""),
            product.get("category_id", "")
        ])
        product_count += 1

print("Products exported:", product_count)


print("\nSTEP 2: ANALYZE TRANSACTION ITEMS")

# Store product-level transaction metrics.
metrics = defaultdict(lambda: {
    "transaction_count": 0,
    "quantity_all": 0,
    "item_value_all": Decimal("0"),
    "completed_quantity": 0,
    "completed_item_value": Decimal("0")
})

# Read transactions one at a time.
transactions = db.transactions.find(
    {},
    {"_id": 0, "status": 1, "items": 1},
    batch_size=1000
)

transaction_count = 0

for transaction in transactions:
    transaction_count += 1
    status = str(transaction.get("status", "")).lower().strip()

    for item in transaction.get("items", []):
        product_id = item["product_id"]
        quantity = int(item["quantity"])

        # Convert MongoDB Decimal128 to Python Decimal.
        item_value = item["subtotal"].to_decimal()

        row = metrics[product_id]
        row["transaction_count"] += 1
        row["quantity_all"] += quantity
        row["item_value_all"] += item_value

        if status == "completed":
            row["completed_quantity"] += quantity
            row["completed_item_value"] += item_value

print("Transactions processed:", transaction_count)
print("Products with transaction items:", len(metrics))


print("\nSTEP 3: EXPORT TRANSACTION METRICS")

# Save product-level metrics for Spark integration.
output_file = output_dir / "mongodb_product_sales.csv"

with output_file.open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow([
        "product_id",
        "transaction_count",
        "quantity_all",
        "item_value_all",
        "completed_quantity",
        "completed_item_value"
    ])

    for product_id, row in sorted(metrics.items()):
        writer.writerow([
            product_id,
            row["transaction_count"],
            row["quantity_all"],
            row["item_value_all"],
            row["completed_quantity"],
            row["completed_item_value"]
        ])

print("Sales metrics CSV:", output_file)
print("MongoDB export completed successfully.")

client.close()
