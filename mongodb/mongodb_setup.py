
# Import the MongoDB client
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient("mongodb://127.0.0.1:27017/")

# Select the e-commerce database
database = client["ecommerce_db"]

# Define the collections needed for the project
collection_names = [
    "users",
    "products",
    "categories",
    "transactions",
    "sessions"
]

# Get the collections that already exist
existing_collections = database.list_collection_names()

# Create only the collections that do not exist
for collection_name in collection_names:
    if collection_name not in existing_collections:
        database.create_collection(collection_name)
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection already exists: {collection_name}")

# Display all collections in the database
print("\nDatabase:", database.name)
print("Collections:", database.list_collection_names())

# Close the MongoDB connection
client.close()
