
# Import libraries for reading JSON files and connecting to MongoDB
import os
import ijson
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


# Define the files and import settings
session_files = [f"sessions_{number}.json" for number in range(20)]
batch_size = 1000
expected_count = 2000000

# Connect to the local MongoDB database
client = MongoClient("mongodb://127.0.0.1:27017/")
database = client["ecommerce_db"]
sessions_collection = database["sessions"]

try:
    # Check that all session files are available
    missing_files = [
        filename for filename in session_files
        if not os.path.exists(filename)
    ]

    if missing_files:
        print("ERROR: Some session files are missing.")
        print(missing_files)

    else:
        # Check existing records to prevent duplicate imports
        existing_count = sessions_collection.count_documents({})

        if existing_count > 0:
            print(f"Sessions already in MongoDB: {existing_count:,}")
            print("Import skipped to avoid duplicate records.")

        else:
            total_inserted = 0

            # Process the 20 session files one at a time
            for filename in session_files:
                print(f"\nReading {filename}")

                batch = []
                file_count = 0

                # Read sessions without loading the full file into memory
                with open(filename, "rb") as file:
                    for session in ijson.items(file, "item"):

                        # Convert decimal values before inserting
                        session = convert_decimals(session)
                        batch.append(session)

                        # Insert a batch of 1,000 sessions
                        if len(batch) == batch_size:
                            sessions_collection.insert_many(batch)

                            file_count += len(batch)
                            total_inserted += len(batch)
                            batch = []

                            # Display progress every 10,000 sessions
                            if total_inserted % 10000 == 0:
                                print(f"Inserted {total_inserted:,} sessions")

                # Insert remaining sessions from the current file
                if batch:
                    sessions_collection.insert_many(batch)
                    file_count += len(batch)
                    total_inserted += len(batch)

                print(f"Completed {filename}: {file_count:,} sessions")

            print("\nSessions import completed!")

    # Verify the total number of sessions in MongoDB
    total_sessions = sessions_collection.count_documents({})

    print(f"\nTotal sessions in MongoDB: {total_sessions:,}")

    if total_sessions == expected_count:
        print("SUCCESS: Session count matches the target.")
    else:
        print("WARNING: Session count does not match the target.")

except Exception as error:
    # Display the error if the import fails
    print("ERROR: Sessions import failed.")
    print(error)
    print("Do not restart the import before checking existing records.")

finally:
    # Close the MongoDB connection
    client.close()
