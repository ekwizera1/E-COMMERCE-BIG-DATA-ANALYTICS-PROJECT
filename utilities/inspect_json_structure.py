
# Import the library for reading JSON files efficiently
import ijson

# List the datasets we want to inspect
files = [
    "users.json",
    "products.json",
    "categories.json",
    "transactions.json",
    "sessions_0.json"
]

# Inspect the first record of each dataset
for filename in files:
    print(f"\nDataset: {filename}")

    # Open the JSON file without loading all records into memory
    with open(filename, "rb") as file:
        records = ijson.items(file, "item")
        first_record = next(records, None)

        # Display the fields and their data types
        if first_record is not None:
            for field, value in first_record.items():
                print(f"  {field}: {type(value).__name__}")
        else:
            print("  The dataset is empty.")
