
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
    print("SESSION DURATION ANALYSIS")
    print("-" * 55)

    # Group sessions by conversion status
    pipeline = [
        {
            "$group": {
                "_id": "$conversion_status",
                "session_count": {"$sum": 1},
                "average_duration": {
                    "$avg": "$duration_seconds"
                },
                "minimum_duration": {
                    "$min": "$duration_seconds"
                },
                "maximum_duration": {
                    "$max": "$duration_seconds"
                }
            }
        },
        {
            "$sort": {
                "average_duration": -1
            }
        }
    ]

    # Run the MongoDB aggregation
    results = sessions.aggregate(pipeline)

    # Display the results for each conversion status
    for result in results:
        status = result["_id"]
        count = result["session_count"]
        average = result["average_duration"]
        minimum = result["minimum_duration"]
        maximum = result["maximum_duration"]

        # Convert average duration from seconds to minutes
        average_minutes = average / 60

        print(f"Conversion status: {status}")
        print(f"Total sessions: {count:,}")
        print(f"Average duration: {average:.2f} seconds")
        print(f"Average duration: {average_minutes:.2f} minutes")
        print(f"Minimum duration: {minimum} seconds")
        print(f"Maximum duration: {maximum} seconds")
        print("-" * 55)

    print("\nSUCCESS: Session duration analysis completed!")

except Exception as error:
    # Display any error during the analysis
    print("ERROR: Session duration analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
