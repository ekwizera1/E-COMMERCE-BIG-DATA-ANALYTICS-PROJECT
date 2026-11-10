
from pyspark.sql import SparkSession

# Start a local Spark session.
spark = (
    SparkSession.builder
    .appName("Ecommerce_Cohort_Analysis")
    .master("local[2]")
    .config("spark.driver.memory", "2g")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Read cleaned transactions.
transactions = spark.read.parquet(
    "spark/data/transactions_clean.parquet"
)

# Read customer information.
users = spark.read.option("multiLine", "true").json(
    "users.json"
)

# Create temporary SQL views.
transactions.createOrReplaceTempView("transactions")
users.createOrReplaceTempView("users")

print("\nSTEP 1: REGISTRATION COHORT SIZES")

# Count all registered customers in each cohort.
cohort_sizes = spark.sql("""
    SELECT
        SUBSTRING(registration_date, 1, 7) AS cohort_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM users
    GROUP BY SUBSTRING(registration_date, 1, 7)
""")

cohort_sizes.show(20, truncate=False)
cohort_sizes.createOrReplaceTempView("cohort_sizes")

print("\nSTEP 2: MONTHLY ACTIVE CUSTOMERS BY COHORT")

# Count customers who made a transaction each month.
monthly_activity = spark.sql("""
    SELECT
        SUBSTRING(u.registration_date, 1, 7) AS cohort_month,
        DATE_FORMAT(t.transaction_time, 'yyyy-MM') AS activity_month,
        COUNT(DISTINCT t.user_id) AS active_customers,
        COUNT(*) AS transactions
    FROM transactions t
    INNER JOIN users u
        ON t.user_id = u.user_id
    GROUP BY
        SUBSTRING(u.registration_date, 1, 7),
        DATE_FORMAT(t.transaction_time, 'yyyy-MM')
""")

monthly_activity.createOrReplaceTempView("monthly_activity")

print("\nSTEP 3: COHORT ACTIVITY RATES")

# Calculate the percentage of each cohort active each month.
cohort_result = spark.sql("""
    SELECT
        a.cohort_month,
        a.activity_month,
        s.cohort_size,
        a.active_customers,
        a.transactions,
        ROUND(
            100.0 * a.active_customers / s.cohort_size,
            2
        ) AS active_rate_pct
    FROM monthly_activity a
    INNER JOIN cohort_sizes s
        ON a.cohort_month = s.cohort_month
    ORDER BY a.cohort_month, a.activity_month
""")

cohort_result.show(30, truncate=False)

print("\nSTEP 4: SAVE COHORT RESULTS")

# Save results for charts and the final report.
cohort_result.coalesce(1).write.mode("overwrite").option(
    "header", True
).csv("spark/output/cohort_analysis")

print("Cohort analysis saved successfully.")

# Close Spark.
spark.stop()
