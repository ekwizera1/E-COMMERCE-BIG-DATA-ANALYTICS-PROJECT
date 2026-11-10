
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
    print("CONVERSION RATE BY DEVICE TYPE")
    print("-" * 60)

    # Group sessions by device type
    pipeline = [
        {
            "$group": {
                "_id": "$device_profile.type",

                # Count all sessions for each device type
                "total_sessions": {
                    "$sum": 1
                },

                # Count sessions with converted status
                "converted_sessions": {
                    "$sum": {
                        "$cond": [
                            {
                                "$eq": [
                                    "$conversion_status",
                                    "converted"
                                ]
                            },
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

    # Store totals for overall conversion rate
    all_sessions = 0
    all_converted = 0

    # Display results for every device type
    for result in results:
        device_type = result["_id"]
        total = result["total_sessions"]
        converted = result["converted_sessions"]

        # Calculate conversion rate for this device
        conversion_rate = (
            converted / total * 100
            if total > 0 else 0
        )

        # Add values to overall totals
        all_sessions += total
        all_converted += converted

        print(f"Device type: {device_type}")
        print(f"Total sessions: {total:,}")
        print(f"Converted sessions: {converted:,}")
        print(f"Conversion rate: {conversion_rate:.2f}%")
        print("-" * 60)

    # Calculate the overall conversion rate
    overall_rate = (
        all_converted / all_sessions * 100
        if all_sessions > 0 else 0
    )

    print(f"All sessions: {all_sessions:,}")
    print(f"All converted sessions: {all_converted:,}")
    print(f"Overall conversion rate: {overall_rate:.2f}%")

    print("\nSUCCESS: Device conversion analysis completed!")

except Exception as error:
    # Display an error if the analysis fails
    print("ERROR: Device conversion analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
