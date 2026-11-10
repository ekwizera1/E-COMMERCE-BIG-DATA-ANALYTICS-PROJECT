
# Import the MongoDB client
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

    print("CUSTOMER CONVERSION STATUS ANALYSIS")
    print("-" * 50)

    # Group sessions by conversion status
    pipeline = [
        {
            "$group": {
                "_id": "$conversion_status",
                "session_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "session_count": -1
            }
        }
    ]

    # Run the aggregation query
    results = sessions.aggregate(pipeline)

    # Display the count and percentage for each status
    for result in results:
        status = result["_id"]
        count = result["session_count"]

        # Calculate the percentage of total sessions
        percentage = (count / total_sessions) * 100

        print(f"Conversion status: {status}")
        print(f"Sessions: {count:,}")
        print(f"Percentage: {percentage:.2f}%")
        print("-" * 50)

    # Display the total sessions analyzed
    print(f"Total sessions analyzed: {total_sessions:,}")

    print("\nSUCCESS: Conversion status analysis completed!")

except Exception as error:
    # Display the error if the analysis fails
    print("ERROR: Conversion status analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
