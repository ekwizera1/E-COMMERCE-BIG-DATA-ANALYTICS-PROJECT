
import json
import ijson
from pathlib import Path

# Input file from the dataset generator
INPUT_FILE = Path("transactions.json")

# Output file for Apache Spark
OUTPUT_FILE = Path("spark/data/transactions.ndjson")


def main():
    # Create the output folder if it does not exist.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total_records = 0

    # Read transactions one at a time to save memory.
    with INPUT_FILE.open("rb") as source:
        with OUTPUT_FILE.open("w", encoding="utf-8") as output:

            for transaction in ijson.items(source, "item"):

                # Convert each transaction into one JSON line.
                # Decimal values are stored as strings to preserve precision.
                json_line = json.dumps(
                    transaction,
                    default=str,
                    ensure_ascii=False
                )

                output.write(json_line + "\n")
                total_records += 1

                # Show progress after every 100,000 transactions.
                if total_records % 100000 == 0:
                    print("Transactions prepared:", total_records)

    print("Preparation completed.")
    print("Total transactions:", total_records)
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
