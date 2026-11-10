
# Import the library for reading large JSON files
import ijson

# Define the expected number of records in each dataset
expected_counts = {
    "users.json": 10000,
    "products.json": 5000,
    "categories.json": 25,
    "transactions.json": 500000
}

# Add the 20 session files, each containing 100,000 records
for number in range(20):
    filename = f"sessions_{number}.json"
    expected_counts[filename] = 100000

# Check each JSON file without loading it fully into memory
all_valid = True

for filename, expected_count in expected_counts.items():
    record_count = 0

    # Read the JSON records one at a time
    with open(filename, "rb") as file:
        for record in ijson.items(file, "item"):
            record_count += 1

    # Compare the actual count with the expected count
    if record_count == expected_count:
        print(f"PASS: {filename} - {record_count:,} records")
    else:
        print(f"FAIL: {filename} - Expected {expected_count:,}, found {record_count:,}")
        all_valid = False

# Display the final validation result
if all_valid:
    print("\nSUCCESS: All datasets passed validation!")
else:
    print("\nWARNING: Some datasets did not pass validation.")
