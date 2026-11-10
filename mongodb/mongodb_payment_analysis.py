
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
    # Count all transactions
    total_transactions = transactions.count_documents({})

    # Group transactions by payment method
    pipeline = [
        {
            "$group": {
                "_id": "$payment_method",
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

    # Run the aggregation pipeline
    results = transactions.aggregate(pipeline)

    print("PAYMENT METHODS ANALYSIS")
    print("-" * 55)

    # Display results for each payment method
    for result in results:
        payment_method = result["_id"]
        count = result["transaction_count"]
        value = result["total_value"]

        # Convert MongoDB Decimal128 to Python Decimal
        if isinstance(value, Decimal128):
            value = value.to_decimal()
        else:
            value = Decimal(str(value))

        # Calculate the percentage of transactions
        percentage = (count / total_transactions) * 100

        print(f"Payment method: {payment_method}")
        print(f"Transactions: {count:,}")
        print(f"Percentage: {percentage:.2f}%")
        print(f"Total value: {value:,.2f}")
        print("-" * 55)

    print(f"Total transactions analyzed: {total_transactions:,}")
    print("\nSUCCESS: Payment methods analysis completed!")

except Exception as error:
    # Display an error if the analysis fails
    print("ERROR: Payment methods analysis failed.")
    print(error)

finally:
    # Close the MongoDB connection
    client.close()
