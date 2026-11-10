
# Import libraries for JSON and MongoDB
import json
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient("mongodb://127.0.0.1:27017/")

# Select the database and categories collection
database = client["ecommerce_db"]
categories_collection = database["categories"]

try:
    # Check if categories have already been imported
    existing_count = categories_collection.count_documents({})

    if existing_count > 0:
        print("Categories already exist. Import skipped.")

    else:
        # Read the categories JSON file
        with open("categories.json", "r", encoding="utf-8") as file:
            categories = json.load(file)

        # Insert all categories into MongoDB
        categories_collection.insert_many(categories)

        print("Categories imported successfully!")

    # Verify the total number of categories
    total_categories = categories_collection.count_documents({})
    print(f"Total categories in MongoDB: {total_categories:,}")

except Exception as error:
    # Display an error if the import fails
    print("ERROR: Categories import failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
