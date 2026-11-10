
# Import the MongoDB client
from pymongo import MongoClient

# Connect to the local MongoDB database
client = MongoClient("mongodb://127.0.0.1:27017/")
database = client["ecommerce_db"]

# Define the expected number of documents
expected_counts = {
    "users": 10000,
    "products": 5000,
    "categories": 25,
    "transactions": 500000,
    "sessions": 2000000
}

# Track the total number of documents
total_documents = 0
all_valid = True

try:
    # Check each collection in MongoDB
    for collection_name, expected_count in expected_counts.items():

        # Count the documents stored in this collection
        actual_count = database[collection_name].count_documents({})

        # Add the count to the database total
        total_documents += actual_count

        # Compare the actual count with the expected count
        if actual_count == expected_count:
            print(f"PASS: {collection_name} - {actual_count:,} documents")
        else:
            print(f"FAIL: {collection_name} - {actual_count:,} documents")
            all_valid = False

    # Display the total number of documents
    print(f"\nTotal documents: {total_documents:,}")

    # Display the final verification result
    if all_valid:
        print("SUCCESS: All MongoDB collections passed verification!")
    else:
        print("WARNING: Some collections have incorrect counts.")

finally:
    # Close the MongoDB connection
    client.close()
