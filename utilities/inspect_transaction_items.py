
# Import the library for reading large JSON files
import ijson

# Open the transactions dataset
with open("transactions.json", "rb") as file:

    # Read only the first transaction
    transactions = ijson.items(file, "item")
    first_transaction = next(transactions, None)

    if first_transaction is not None:

        # Get the list of purchased items
        items = first_transaction.get("items", [])

        print("TRANSACTION ITEMS STRUCTURE")
        print("-" * 45)

        # Display the number of items in the transaction
        print(f"Number of items: {len(items)}")

        # Inspect the first purchased item
        if items:
            first_item = items[0]

            print("\nFirst item:")

            # Display each field and its example value
            if isinstance(first_item, dict):
                for field, value in first_item.items():
                    print(f"{field}: {value}")
            else:
                print(first_item)

        else:
            print("This transaction has no items.")

    else:
        print("No transaction found.")
