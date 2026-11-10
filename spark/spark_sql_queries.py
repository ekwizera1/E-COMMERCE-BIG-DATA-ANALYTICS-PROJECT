
from pyspark.sql import SparkSession

# Create a Spark session.
spark = (
    SparkSession.builder
    .appName("Ecommerce_Spark_SQL")
    .master("local[2]")
    .config("spark.driver.memory", "2g")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

# Reduce Spark log messages.
spark.sparkContext.setLogLevel("ERROR")

# Read cleaned transaction data.
transactions_df = spark.read.parquet(
    "spark/data/transactions_clean.parquet"
)

# Create a SQL view for transactions.
transactions_df.createOrReplaceTempView("transactions")


# QUERY 1: TRANSACTIONS BY STATUS
print("\nQUERY 1: TRANSACTIONS BY STATUS")

status_summary = spark.sql("""
    SELECT
        status,
        COUNT(*) AS total_transactions,
        ROUND(SUM(total), 2) AS total_transaction_value
    FROM transactions
    GROUP BY status
    ORDER BY total_transactions DESC
""")

status_summary.show(truncate=False)


# QUERY 2: MONTHLY TRANSACTION TRENDS
print("\nQUERY 2: MONTHLY TRANSACTION TRENDS")

monthly_summary = spark.sql("""
    SELECT
        DATE_FORMAT(transaction_time, 'yyyy-MM') AS month,
        COUNT(*) AS total_transactions,
        COUNT(DISTINCT user_id) AS unique_customers,
        ROUND(SUM(total), 2) AS total_transaction_value
    FROM transactions
    GROUP BY DATE_FORMAT(transaction_time, 'yyyy-MM')
    ORDER BY month
""")

monthly_summary.show(truncate=False)


# QUERY 3: CUSTOMER TRANSACTIONS BY REGISTRATION MONTH
print("\nQUERY 3: CUSTOMER TRANSACTIONS BY REGISTRATION MONTH")

# Read customer profiles from the JSON file.
users_df = spark.read.option("multiLine", "true").json(
    "users.json"
)

# Create a SQL view for customers.
users_df.createOrReplaceTempView("users")

# Join customer profiles with their transactions.
customer_summary = spark.sql("""
    SELECT
        SUBSTRING(u.registration_date, 1, 7) AS registration_month,
        COUNT(DISTINCT t.user_id) AS unique_customers,
        COUNT(*) AS total_transactions,
        ROUND(SUM(t.total), 2) AS total_transaction_value
    FROM transactions t
    INNER JOIN users u
        ON t.user_id = u.user_id
    GROUP BY SUBSTRING(u.registration_date, 1, 7)
    ORDER BY registration_month
""")

customer_summary.show(20, truncate=False)


# Stop Spark after completing the analyses.
spark.stop()
