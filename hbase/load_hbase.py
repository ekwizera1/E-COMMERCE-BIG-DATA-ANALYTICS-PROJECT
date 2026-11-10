
import ijson
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Input dataset and output commands
INPUT_FILE = Path("sessions_0.json")
OUTPUT_FILE = Path("hbase") / "load_commands.hbase"

# Start with 20 sessions to test the loading process.
MAX_SESSIONS = 5000


def safe_text(value):
    # Escape text for HBase Shell commands.
    return str(value).replace("\\", "\\\\").replace("'", "\\'")


def write_put(output, table, row_key, column, value):
    # Write one HBase put command.
    values = [table, row_key, column, value]
    quoted = ["'" + safe_text(v) + "'" for v in values]
    output.write("put " + ", ".join(quoted) + "\n")


def make_row_key(session):
    # Use reverse time to keep recent sessions first.
    start = datetime.fromisoformat(session["start_time"])
    start = start.replace(tzinfo=timezone.utc)
    reverse_time = 9999999999 - int(start.timestamp())

    return (
        session["user_id"]
        + "#"
        + str(reverse_time)
        + "#"
        + session["session_id"]
    )


def main():
    metrics = defaultdict(lambda: {"views": 0, "cart_quantity": 0})
    loaded = 0

    with INPUT_FILE.open("rb") as source:
        with OUTPUT_FILE.open("w", encoding="utf-8") as output:

            for session in ijson.items(source, "item"):
                if loaded >= MAX_SESSIONS:
                    break

                row_key = make_row_key(session)
                user_id = session["user_id"]
                session_date = session["start_time"][:10].replace("-", "")
                device = session["device_profile"]

                # Save session information.
                information = {
                    "user_id": user_id,
                    "session_id": session["session_id"],
                    "start_time": session["start_time"],
                    "duration": session["duration_seconds"],
                    "device_type": device["type"],
                    "browser": device["browser"],
                    "referrer": session["referrer"],
                    "conversion_status": session["conversion_status"]
                }

                for column, value in information.items():
                    write_put(
                        output,
                        "fp_user_sessions",
                        row_key,
                        "info:" + column,
                        value
                    )

                # Save page views.
                for index, page in enumerate(session["page_views"]):
                    page_value = "|".join([
                        str(page.get("timestamp") or ""),
                        str(page.get("page_type") or ""),
                        str(page.get("product_id") or ""),
                        str(page.get("category_id") or ""),
                        str(page.get("view_duration") or "")
                    ])

                    write_put(
                        output,
                        "fp_user_sessions",
                        row_key,
                        "pv:" + str(index).zfill(3),
                        page_value
                    )

                    # Count product-detail views by product and date.
                    product_id = page.get("product_id")
                    if page.get("page_type") == "product_detail" and product_id:
                        key = (product_id, session_date)
                        metrics[key]["views"] += 1

                # Save the final shopping cart contents.
                for product_id, item in session["cart_contents"].items():
                    quantity = int(item["quantity"])
                    cart_value = str(quantity) + "|" + str(item["price"])

                    write_put(
                        output,
                        "fp_user_sessions",
                        row_key,
                        "cart:" + product_id,
                        cart_value
                    )

                    key = (product_id, session_date)
                    metrics[key]["cart_quantity"] += quantity

                loaded += 1

            # Save daily product metrics.
            for (product_id, date), values in metrics.items():
                metric_key = product_id + "#" + date

                for metric_name, metric_value in values.items():
                    write_put(
                        output,
                        "fp_product_metrics",
                        metric_key,
                        "m:" + metric_name,
                        metric_value
                    )

    print("Sessions prepared:", loaded)
    print("Product-date metrics prepared:", len(metrics))
    print("Commands saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
