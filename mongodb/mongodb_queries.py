
# Import the MongoDB client
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=5000
)

# Select the e-commerce database
database = client["ecommerce_db"]

# Select the transactions collection
transactions = database["transactions"]

try:
    # Query 1: Display one transaction as an example
    print("QUERY 1: SAMPLE TRANSACTION")

    sample = transactions.find_one(
        {},
        {
            "_id": 0,
            "transaction_id": 1,
            "user_id": 1,
            "status": 1,
            "payment_method": 1,
            "total": 1
        }
    )

    if sample:
        for field, value in sample.items():
            print(f"{field}: {value}")
    else:
        print("No transactions found.")

    # Query 2: Count all transactions
    print("\nQUERY 2: TOTAL TRANSACTIONS")

    total_transactions = transactions.count_documents({})
    print(f"Total transactions: {total_transactions:,}")

    # Query 3: Count transactions by status
    print("\nQUERY 3: TRANSACTIONS BY STATUS")

    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    # Execute the aggregation pipeline
    results = transactions.aggregate(pipeline)

    # Display the results
    for result in results:
        status = result["_id"]
        count = result["count"]

        percentage = (count / total_transactions) * 100

        print(
            f"{status}: {count:,} transactions "
            f"({percentage:.2f}%)"
        )

    print("\nSUCCESS: MongoDB queries completed!")

except Exception as error:
    # Display an error if a query fails
    print("ERROR: MongoDB query failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
