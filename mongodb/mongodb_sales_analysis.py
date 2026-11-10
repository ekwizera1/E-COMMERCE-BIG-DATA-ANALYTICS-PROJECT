
# Import libraries for MongoDB and decimal values
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from decimal import Decimal

# Connect to the local MongoDB database
client = MongoClient("mongodb://127.0.0.1:27017/")
database = client["ecommerce_db"]

# Select the transactions collection
transactions = database["transactions"]

try:
    # Group transactions by their status
    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "transaction_count": {"$sum": 1},
                "total_value": {"$sum": "$total"}
            }
        },
        {
            "$sort": {
                "transaction_count": -1
            }
        }
    ]

    # Run the aggregation query
    results = transactions.aggregate(pipeline)

    print("TRANSACTION VALUE BY STATUS")
    print("-" * 50)

    grand_total = Decimal("0")
    total_count = 0

    # Display the results for each status
    for result in results:
        status = result["_id"]
        count = result["transaction_count"]
        value = result["total_value"]

        # Convert MongoDB Decimal128 to Python Decimal
        if isinstance(value, Decimal128):
            value = value.to_decimal()
        else:
            value = Decimal(str(value))

        # Calculate the overall totals
        grand_total += value
        total_count += count

        print(f"Status: {status}")
        print(f"Transactions: {count:,}")
        print(f"Total value: {value:,.2f}")
        print("-" * 50)

    # Display the overall transaction value
    print(f"Total transactions: {total_count:,}")
    print(f"Overall transaction value: {grand_total:,.2f}")

    print("\nSUCCESS: Transaction value analysis completed!")

except Exception as error:
    # Display an error if the analysis fails
    print("ERROR: Transaction value analysis failed.")
    print(error)

finally:
    # Close the database connection
    client.close()
