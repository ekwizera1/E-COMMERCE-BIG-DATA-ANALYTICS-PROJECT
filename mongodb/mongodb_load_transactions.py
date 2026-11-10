
# Import libraries for reading JSON and using MongoDB
import ijson
from decimal import Decimal
from bson.decimal128 import Decimal128
from pymongo import MongoClient


# Convert decimal numbers to MongoDB Decimal128
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
transactions_collection = database["transactions"]

# Set the batch size and expected number of transactions
batch_size = 1000
expected_count = 500000

try:
    # Check for existing records to prevent duplicate imports
    existing_count = transactions_collection.count_documents({})

    if existing_count > 0:
        print(f"Collection already contains {existing_count:,} transactions.")
        print("Import skipped to avoid duplicate records.")
        print("Check existing records before retrying.")

    else:
        # Store a small batch of transactions in memory
        batch = []
        inserted_count = 0

        # Read transactions one at a time from the JSON file
        with open("transactions.json", "rb") as file:
            for transaction in ijson.items(file, "item"):

                # Convert decimal values before inserting
                transaction = convert_decimals(transaction)

                # Add the transaction to the current batch
                batch.append(transaction)

                # Insert the batch when it reaches 1,000 records
                if len(batch) == batch_size:
                    transactions_collection.insert_many(batch)

                    inserted_count += len(batch)
                    batch = []

                    # Display import progress
                    if inserted_count % 10000 == 0:
                        print(f"Inserted {inserted_count:,} transactions")

            # Insert any remaining transactions
            if batch:
                transactions_collection.insert_many(batch)
                inserted_count += len(batch)

        print("\nTransactions import completed!")

    # Verify the total number of transactions in MongoDB
    total_transactions = transactions_collection.count_documents({})

    print(f"Total transactions in MongoDB: {total_transactions:,}")

    if total_transactions == expected_count:
        print("SUCCESS: Transaction count matches the target.")
    else:
        print("WARNING: Transaction count does not match the target.")

except Exception as error:
    # Display any error that occurs during the import
    print("ERROR: Transaction import failed.")
    print(error)

finally:
    # Close the database connection
    client.close()
