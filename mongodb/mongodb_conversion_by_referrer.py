
# Import MongoClient to connect to MongoDB
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=5000
)

# Select the database and sessions collection
database = client["ecommerce_db"]
sessions = database["sessions"]

try:
    print("CONVERSION RATE BY TRAFFIC SOURCE")
    print("-" * 60)

    # Group sessions by traffic source
    pipeline = [
        {
            "$group": {
                "_id": "$referrer",

                # Count all sessions from each source
                "total_sessions": {"$sum": 1},

                # Count only sessions marked as converted
                "converted_sessions": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$conversion_status", "converted"]},
                            1,
                            0
                        ]
                    }
                }
            }
        },
        {
            "$sort": {
                "total_sessions": -1
            }
        }
    ]

    # Run the MongoDB aggregation
    results = sessions.aggregate(pipeline)

    # Track the totals for all traffic sources
    all_sessions = 0
    all_converted = 0

    # Display the conversion rate for each traffic source
    for result in results:
        source = result["_id"]
        total = result["total_sessions"]
        converted = result["converted_sessions"]

        # Calculate the conversion rate
        conversion_rate = (converted / total) * 100

        # Update the overall totals
        all_sessions += total
        all_converted += converted

        print(f"Traffic source: {source}")
        print(f"Total sessions: {total:,}")
        print(f"Converted sessions: {converted:,}")
        print(f"Conversion rate: {conversion_rate:.2f}%")
        print("-" * 60)

    # Calculate the overall conversion rate
    overall_rate = (all_converted / all_sessions) * 100

    print(f"All sessions: {all_sessions:,}")
    print(f"All converted sessions: {all_converted:,}")
    print(f"Overall conversion rate: {overall_rate:.2f}%")

    print("\nSUCCESS: Conversion by traffic source completed!")

except Exception as error:
    # Display any error during the analysis
    print("ERROR: Conversion analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
