
# Import libraries for MongoDB and decimal values
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from decimal import Decimal

# Connect to the local MongoDB server
client = MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=5000
)

# Select the e-commerce database
database = client["ecommerce_db"]
transactions = database["transactions"]

try:
    print("TRANSACTION VALUE BY PRODUCT CATEGORY")
    print("-" * 60)

    # Create the MongoDB aggregation pipeline
    pipeline = [
        # Separate purchased items into individual records
        {
            "$unwind": "$items"
        },

        # Match each purchased item with its product
        {
            "$lookup": {
                "from": "products",
                "localField": "items.product_id",
                "foreignField": "product_id",
                "as": "product"
            }
        },

        # Keep the product information for each item
        {
            "$unwind": {
                "path": "$product",
                "preserveNullAndEmptyArrays": True
            }
        },

        # Calculate the totals for each product category
        {
            "$group": {
                "_id": "$product.category_id",
                "item_count": {"$sum": 1},
                "units_sold": {"$sum": "$items.quantity"},
                "gross_item_value": {
                    "$sum": "$items.subtotal"
                }
            }
        },

        # Find the category name
        {
            "$lookup": {
                "from": "categories",
                "localField": "_id",
                "foreignField": "category_id",
                "as": "category"
            }
        },

        # Extract the category information
        {
            "$unwind": {
                "path": "$category",
                "preserveNullAndEmptyArrays": True
            }
        },

        # Sort categories by gross item value
        {
            "$sort": {
                "gross_item_value": -1
            }
        }
    ]

    # Run the aggregation and allow disk use if needed
    results = transactions.aggregate(
        pipeline,
        allowDiskUse=True
    )

    total_value = Decimal("0")
    total_units = 0
    total_items = 0
    category_count = 0

    # Display the analysis results
    for result in results:
        category_id = result["_id"]
        category = result.get("category", {})
        category_name = category.get("name", "Unknown")

        item_count = result["item_count"]
        units_sold = result["units_sold"]
        value = result["gross_item_value"]

        # Convert MongoDB Decimal128 into Python Decimal
        if isinstance(value, Decimal128):
            value = value.to_decimal()
        else:
            value = Decimal(str(value))

        # Update the overall totals
        total_value += value
        total_units += units_sold
        total_items += item_count
        category_count += 1

        print(f"Category: {category_name}")
        print(f"Category ID: {category_id}")
        print(f"Transaction items: {item_count:,}")
        print(f"Units sold: {units_sold:,}")
        print(f"Gross item value: {value:,.2f}")
        print("-" * 60)

        # Report missing product or category matches
        if category_id is None or category_name == "Unknown":
            print("WARNING: An item has no matching category.")

    # Display the overall results
    print(f"Category groups: {category_count}")
    print(f"Total transaction items: {total_items:,}")
    print(f"Total units sold: {total_units:,}")
    print(f"Overall gross item value: {total_value:,.2f}")

    print("\nSUCCESS: Product category analysis completed!")

except Exception as error:
    # Display any error during the analysis
    print("ERROR: Product category analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
