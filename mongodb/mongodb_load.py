
# Import libraries for JSON files and MongoDB
import json
from pymongo import MongoClient

# Connect to the local MongoDB database
client = MongoClient("mongodb://127.0.0.1:27017/")
database = client["ecommerce_db"]

# Select the users collection
users_collection = database["users"]

# Set the number of records inserted at a time
batch_size = 1000

try:
    # Avoid inserting the same dataset twice
    existing_count = users_collection.count_documents({})

    if existing_count > 0:
        print(f"Users collection already contains {existing_count:,} records.")
        print("Import skipped to avoid duplicate records.")

    else:
        # Read the users dataset
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)

        # Insert users into MongoDB in small batches
        for start in range(0, len(users), batch_size):
            batch = users[start:start + batch_size]
            users_collection.insert_many(batch)

            # Display the number of inserted users
            inserted_count = start + len(batch)
            print(f"Inserted {inserted_count:,} users")

        print("\nUsers import completed successfully!")

    # Verify the number of users stored in MongoDB
    total_users = users_collection.count_documents({})
    print(f"Total users in MongoDB: {total_users:,}")

except Exception as error:
    # Display an error if the import fails
    print("ERROR: Users import failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
