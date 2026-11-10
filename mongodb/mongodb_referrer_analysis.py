
# Import MongoClient to connect Python to MongoDB
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=5000
)

# Select the e-commerce database
database = client["ecommerce_db"]

# Select the sessions collection
sessions = database["sessions"]

try:
    # Count all customer sessions
    total_sessions = sessions.count_documents({})

    print("CUSTOMER TRAFFIC SOURCE ANALYSIS")
    print("-" * 55)

    # Group sessions by traffic source
    pipeline = [
        {
            "$group": {
                "_id": "$referrer",
                "session_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "session_count": -1
            }
        }
    ]

    # Run the MongoDB aggregation
    results = sessions.aggregate(pipeline)

    # Display the count and percentage for each traffic source
    for result in results:
        source = result["_id"]
        count = result["session_count"]

        # Calculate the percentage of total sessions
        percentage = (count / total_sessions) * 100

        print(f"Traffic source: {source}")
        print(f"Sessions: {count:,}")
        print(f"Percentage: {percentage:.2f}%")
        print("-" * 55)

    # Display the total number of sessions analyzed
    print(f"Total sessions analyzed: {total_sessions:,}")

    print("\nSUCCESS: Traffic source analysis completed!")

except Exception as error:
    # Display an error if the analysis fails
    print("ERROR: Traffic source analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
