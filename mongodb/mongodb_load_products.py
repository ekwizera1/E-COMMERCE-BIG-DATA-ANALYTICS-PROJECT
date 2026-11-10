
# Import the libraries needed for MongoDB and JSON data
import json
from decimal import Decimal
from bson.decimal128 import Decimal128
from pymongo import MongoClient


# Convert decimal values into MongoDB Decimal128
def convert_decimals(value):
    if isinstance(value, Decimal):
        return Decimal128(value)

    if isinstance(value, list):
        return [convert_decimals(item) for item in value]

    if isinstance(value, dict):
        return {
            key: convert_decimals(item)
            for key, item in value.items()
        }

    return value


# Connect to the local MongoDB database
client = MongoClient("mongodb://127.0.0.1:27017/")
database = client["ecommerce_db"]
products_collection = database["products"]

batch_size = 1000

try:
    # Check whether products already exist
    existing_count = products_collection.count_documents({})

    if existing_count > 0:
        print(f"Products collection already contains {existing_count:,} records.")
        print("Import skipped to avoid duplicate records.")

    else:
        # Read product prices as decimals
        with open("products.json", "r", encoding="utf-8") as file:
            products = json.load(file, parse_float=Decimal)

        # Convert decimal prices to MongoDB Decimal128
        products = convert_decimals(products)

        # Insert products in batches of 1,000
        for start in range(0, len(products), batch_size):
            batch = products[start:start + batch_size]
            products_collection.insert_many(batch)

            inserted_count = start + len(batch)
            print(f"Inserted {inserted_count:,} products")

        print("\nProducts import completed successfully!")

    # Verify the number of products in MongoDB
    total_products = products_collection.count_documents({})
    print(f"Total products in MongoDB: {total_products:,}")

except Exception as error:
    # Display the error if the import fails
    print("ERROR: Products import failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
