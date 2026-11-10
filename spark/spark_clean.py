
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, to_timestamp
from pyspark.sql.types import DecimalType

# Create a local Spark session.
spark = (
    SparkSession.builder
    .appName("Ecommerce_Data_Cleaning")
    .master("local[2]")
    .config("spark.driver.memory", "2g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Read the original prepared transactions.
df = spark.read.json("spark/data/transactions.ndjson")

print("\nSTEP 1: ORIGINAL DATA")
original_count = df.count()
print("Original transactions:", original_count)

# Convert money fields into numeric decimal values.
money_type = DecimalType(18, 2)

df = (
    df.withColumn("total", col("total").cast(money_type))
      .withColumn("subtotal", col("subtotal").cast(money_type))
      .withColumn("discount", col("discount").cast(money_type))
)

# Convert the transaction timestamp into a datetime value.
df = df.withColumn(
    "transaction_time",
    to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss")
)

# Standardize text values.
df = (
    df.withColumn("status", lower(trim(col("status"))))
      .withColumn("payment_method", lower(trim(col("payment_method"))))
)

print("\nSTEP 2: CHECK MISSING OR INVALID VALUES")

# Check important fields before removing invalid records.
invalid_rows = df.filter(
    col("transaction_id").isNull()
    | (trim(col("transaction_id")) == "")
    | col("user_id").isNull()
    | (trim(col("user_id")) == "")
    | col("transaction_time").isNull()
    | col("total").isNull()
    | (col("total") < 0)
)

invalid_count = invalid_rows.count()

print("Invalid transactions:", invalid_count)

print("\nSTEP 3: REMOVE INVALID AND DUPLICATE RECORDS")

# Keep only records with valid key fields and amounts.
clean_df = df.filter(
    col("transaction_id").isNotNull()
    & (trim(col("transaction_id")) != "")
    & col("user_id").isNotNull()
    & (trim(col("user_id")) != "")
    & col("transaction_time").isNotNull()
    & col("total").isNotNull()
    & (col("total") >= 0)
)

valid_count = clean_df.count()

# Keep one record for each transaction ID.
clean_df = clean_df.dropDuplicates(["transaction_id"])

clean_count = clean_df.count()

print("Valid transactions before removing duplicates:", valid_count)
print("Duplicate rows removed:", valid_count - clean_count)
print("Clean transactions:", clean_count)

print("\nSTEP 4: SAVE CLEANED DATA")

# Save the cleaned dataset in Parquet format.
clean_df.write.mode("overwrite").parquet(
    "spark/data/transactions_clean.parquet"
)

print("Cleaned data saved successfully.")

print("\nSTEP 5: DISPLAY CLEANED SCHEMA")
clean_df.printSchema()

spark.stop()
