
import csv
import re
from pathlib import Path

# Set the input and output file paths.
input_file = Path("integration/hbase_product_metrics.txt")
output_file = Path("integration/hbase_product_metrics.csv")

# Match product metrics exported from HBase Shell.
pattern = re.compile(
    r"^\s*(prod_\d+)#(\d{8})\s+"
    r"column=m:(views|cart_quantity),\s*"
    r"timestamp=\d+,\s*value=(\d+)\s*$"
)

# Store daily metrics for each product.
metrics = {}

# Read the HBase export file.
with input_file.open("r", encoding="utf-8-sig") as file:
    for line in file:
        match = pattern.match(line)

        if not match:
            continue

        product_id, date_text, metric_name, value = match.groups()

        # Convert YYYYMMDD to YYYY-MM-DD.
        date = (
            date_text[:4] + "-"
            + date_text[4:6] + "-"
            + date_text[6:8]
        )

        key = (product_id, date)

        if key not in metrics:
            metrics[key] = {
                "views": None,
                "cart_quantity": None
            }

        metrics[key][metric_name] = int(value)

# Check that each row has both metrics.
incomplete_rows = sum(
    1 for item in metrics.values()
    if item["views"] is None
    or item["cart_quantity"] is None
)

if incomplete_rows > 0:
    raise ValueError(
        f"Found {incomplete_rows} incomplete HBase rows."
    )

# Write the extracted metrics to CSV.
with output_file.open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow([
        "product_id",
        "date",
        "views",
        "cart_quantity"
    ])

    for (product_id, date), values in sorted(metrics.items()):
        writer.writerow([
            product_id,
            date,
            values["views"],
            values["cart_quantity"]
        ])

# Display the conversion results.
print("\nHBASE TO CSV CONVERSION")
print("HBase rows converted:", len(metrics))
print("Incomplete rows:", incomplete_rows)
print("CSV file:", output_file)
print("Conversion completed successfully.")
