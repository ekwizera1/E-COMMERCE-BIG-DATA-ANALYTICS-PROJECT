
from pyspark.sql import SparkSession

# Create a Spark session for local processing.
spark = (
    SparkSession.builder
    .appName("Ecommerce_Big_Data_Analytics")
    .master("local[2]")
    .config("spark.driver.memory", "2g")
    .getOrCreate()
)

# Reduce unnecessary Spark messages.
spark.sparkContext.setLogLevel("ERROR")

# Read the prepared transaction dataset.
transactions = spark.read.json("spark/data/transactions.ndjson")

# Display the structure of the dataset.
print("\nTRANSACTIONS DATASET SCHEMA")
transactions.printSchema()

# Count all transactions.
total_transactions = transactions.count()
print("\nTotal transactions:", total_transactions)

# Show a few important columns.
print("\nSAMPLE TRANSACTIONS")
transactions.select(
    "transaction_id",
    "user_id",
    "timestamp",
    "total",
    "status"
).show(5, truncate=False)

# Stop Spark after processing.
spark.stop()
