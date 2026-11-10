
# Import the MongoDB client
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient("mongodb://127.0.0.1:27017/")

# Select the e-commerce database
database = client["ecommerce_db"]

try:
    # Create indexes for the users collection
    database["users"].create_index("user_id")
    print("Created index on users.user_id")

    # Create indexes for the products collection
    database["products"].create_index("product_id")
    database["products"].create_index("category_id")
    print("Created indexes on products")

    # Create an index for the categories collection
    database["categories"].create_index("category_id")
    print("Created index on categories.category_id")

    # Create indexes for the transactions collection
    database["transactions"].create_index("transaction_id")
    database["transactions"].create_index("user_id")
    database["transactions"].create_index("timestamp")
    print("Created indexes on transactions")

    # Create indexes for the sessions collection
    database["sessions"].create_index("session_id")
    print("Created index on sessions.session_id")

    database["sessions"].create_index("user_id")
    print("Created index on sessions.user_id")

    database["sessions"].create_index("start_time")
    print("Created index on sessions.start_time")

    # Define all collections to check
    collection_names = [
        "users",
        "products",
        "categories",
        "transactions",
        "sessions"
    ]

    # Display indexes available in every collection
    for collection_name in collection_names:
        print(f"\nIndexes in {collection_name}:")

        # Read index information from MongoDB
        indexes = database[collection_name].list_indexes()

        # Display the name of each index
        for index in indexes:
            print(index["name"])

    # Display the final result
    print("\nSUCCESS: All MongoDB indexes created!")

except Exception as error:
    # Display an error if index creation fails
    print("ERROR: MongoDB index creation failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
