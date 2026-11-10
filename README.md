# Distributed Multi-Model Analytics for E-commerce Data

**Adventist University of Central Africa (AUCA) — Big Data Analytics Final Project**  

**Implementation:** Python, MongoDB, Apache HBase (Docker), Apache Spark (PySpark), and static visualizations

> **Scope and evidence.** This README describes the implementation actually developed in `FinalProjectBD`, as documented in the final eight-page AUCA technical report and verified terminal outputs. It distinguishes the complete MongoDB dataset from the smaller HBase subset. The project is a local proof of concept, not a performance-tested multi-node cluster or an estimate of real customer conversion.

## 1. Project purpose and research question

The project evaluates how different technologies can work together in e-commerce analytics:

- **MongoDB** stores complete, nested e-commerce documents and supports aggregation pipelines.
- **HBase** stores time-oriented browsing sessions and product-by-day interaction metrics using row keys and column families.
- **Apache Spark** Data processing  include cleans, summarizes and joins datasets using DataFrames and Spark SQL.
- **Python and Matplotlib**  for visualisations  purposes.

**Integrated business question:** *Which products attract browsing interest, and how does this compare with their transaction performance?*

The solution compares product-detail views and cart quantities observed in HBase with completed-transaction item quantities derived from MongoDB. These measures cover different portions of the synthetic data, so the comparison is **descriptive**, not a matched conversion-rate calculation.

## 2. Architecture and actual workflow

```text
Lecturer-provided Python generator 
                  |
                  v
users.json | products.json | categories.json
transactions.json | sessions_0.json ... sessions_19.json
                  |
       +----------+-----------------------+
       |                                  |
       v                                  v
MongoDB: ecommerce_db            HBase in Docker: hbase-recovery
5 collections, 2,515,025 docs     fp_user_sessions: 5,000 rows
       |                           fp_product_metrics: 16,804 rows
       |                                  |
       | CSV exports                      | HBase Shell scan -> text -> CSV
       +------------------+---------------+
                          |
                          v
                  Apache Spark / PySpark
           transactions: NDJSON -> clean Parquet
            Spark SQL, cohorts and product joins
                          |
                          v
             5,000 integrated product rows
                          |
                          v
              Four charts and technical report
```

**Important:** MongoDB and HBase were connected to Spark through exported files in this implementation. Direct live Spark connectors were **not** used. HBase used the **first 5,000 sessions from `sessions_0.json`**, not a random or representative sample of all 2,000,000 sessions.

## 3. Generated data and relationships
```
| Input file(s) | Records | Example fields / role |
|---|---:|---|
| `users.json` | 10,000 | `user_id`, registration date, geography |
| `products.json` | 5,000 | `product_id`, `category_id`, price history, stock |
| `categories.json` | 25 | Category/subcategory hierarchy |
| `transactions.json` | 500,000 | `transaction_id`, `user_id`, `session_id`, `items[]`, `status`, `total` |
| `sessions_0.json` to `sessions_19.json` | 2,000,000 | `session_id`, `user_id`, page views, cart contents, device, referrer |
| **Total** | **2,515,025** | 90-day synthetic activity window |

Each session chunk contains 100,000 session records. The key links are `user_id` (users, sessions and transactions), `product_id` (products, transaction items and product browsing metrics), and `session_id` where a transaction is linked to a session. **Not every transaction has a usable session link.**

The generator models weighted browsing-page transitions, cart additions (programmed probability 0.30 in the relevant flow), checkout/completion logic (programmed conditional probability 0.70), inventory checks, and optional discounts. These are **simulation settings**, not measured business conversion or discount rates.

### Safe generation on a fresh checkout

From the project root in PowerShell, install the required Python packages and use the generator only when the raw JSON files do not yet exist:

```powershell
python -m pip install faker pandas pymongo ijson matplotlib "pyspark==4.2.1"
python .\data_generation\dataset_generator.py
```

**Do not rerun the generator on the existing working dataset.** It opens JSON outputs in write mode and can overwrite the files used to produce the documented results. The complete generation is resource-intensive. To test without touching the current inputs, run the generator from a separate empty working directory, because output paths are relative to the terminal's current directory.

All 24 generated JSON datasets are included in the GitHub repository using Git Large File Storage (Git LFS). Spark NDJSON and Parquet datasets are also tracked with Git LFS. This allows users to recover the original project datasets without regenerating them. The data generator is included for reproducibility and experimentation.

## 4. Actual project structure (10 November 2026)

```text
FinalProjectBD/
|-- README.md                         # This file; only README for the full project
|-- .gitignore
|-- data_generation/
|   `-- dataset_generator.py          # One retained working generator
|-- mongodb/
|   |-- mongodb_setup.py
|   |-- test_mongodb.py
|   |-- mongodb_load.py               # User loader
|   |-- mongodb_load_categories.py
|   |-- mongodb_load_products.py
|   |-- mongodb_load_transactions.py
|   |-- mongodb_load_sessions.py
|   |-- mongodb_indexes.py
|   |-- mongodb_verify.py
|   |-- mongodb_queries.py
|   `-- mongodb_*_analysis.py / other analysis scripts and saved results
|-- hbase/
|   |-- schema.hbase
|   |-- load_hbase.py
|   |-- load_commands.hbase
|   `-- queries.hbase
|-- spark/
|   |-- prepare_transactions.py
|   |-- spark_clean.py
|   |-- spark_batch.py
|   |-- spark_sql_queries.py
|   `-- spark_cohort.py
|-- integration/
|   |-- export_mongodb.py
|   |-- convert_hbase_to_csv.py
|   `-- spark_integrated_analysis.py
|-- visualizations/
|   |-- make_charts.py
|   `-- charts/                      # Four generated PNGs
|-- utilities/
|   |-- inspect_device_profile.py
|   |-- inspect_json_structure.py
|   |-- inspect_transaction_items.py
|   `-- validate_datasets.py
|-- report/
|   |-- AUCA_Ecommerce_Big_Data_Technical_Report.docx
|   |-- Technical_Report.pdf
|   |-- Final_Project_Presentation.pptx
|   |-- make_architecture.py
|   |-- build_report.py
|   `-- build_presentation.py
|
|-- users.json                       # Stored using Git LFS
|-- products.json                    # Stored using Git LFS
|-- categories.json                  # Stored using Git LFS
|-- transactions.json                # Stored using Git LFS
`-- sessions_0.json ... sessions_19.json  # Stored using Git LFS
```

## 5. Local environment and prerequisites

The implementation was developed on **Windows with PowerShell and VS Code**, using:

- **Python:** 3.11.9 in the working project environment.
- **MongoDB:** locally accessible at `mongodb://127.0.0.1:27017`; database `ecommerce_db`.
- **Docker / Apache HBase:** `hbase-recovery` container with HBase Shell, Master and RegionServer; the image used during development was `harisekhon/hbase`.
- **PySpark:** installed Python package version 4.2.1; Spark was executed locally with `local[2]` and 2 GB of driver memory in the documented runs.
- **Java:** required for Spark and the relevant HBase environment.
- **Python libraries:** `faker`, `pandas`, `pymongo`, `ijson`, `pyspark`, and `matplotlib`; report builders may additionally need `python-docx`, `python-pptx` and `Pillow` depending on the script imports.
```
**Always open PowerShell in the project root before running relative-path scripts:**

```powershell
cd C:\Users\user\Desktop\FinalProjectBD
```

If the terminal has an old `SPARK_HOME` pointing to `C:\spark` (Spark 3.5.9), clear it before running the installed PySpark 4.2.1:

## 6. Part 1A — MongoDB modeling, loading and analytics

MongoDB was selected because product details, category hierarchies, user attributes, session journeys and transaction line items are naturally represented as **nested documents**.

### Collections and observed counts

| Collection | Documents |
|---|---:|
| `users` | 10,000 |
| `products` | 5,000 |
| `categories` | 25 |
| `transactions` | 500,000 |
| `sessions` | 2,000,000 |
| **Total** | **2,515,025** |

### Existing installation: safe checks

Start MongoDB separately, then run from the project root:

```powershell
python .\mongodb\test_mongodb.py
python .\mongodb\mongodb_verify.py
python .\mongodb\mongodb_queries.py
```

The verification script was rerun after the MongoDB scripts were organized into `mongodb/` and confirmed the five expected collection counts on **10 November 2026**.

### Fresh database only: loading order

With the JSON datasets present in the project root, inspect the loader and setup scripts before running them. On a **new, empty database**, the intended stage order is:

```powershell
python .\mongodb\mongodb_setup.py
python .\mongodb\mongodb_load.py
python .\mongodb\mongodb_load_categories.py
python .\mongodb\mongodb_load_products.py
python .\mongodb\mongodb_load_transactions.py
python .\mongodb\mongodb_load_sessions.py
python .\mongodb\mongodb_indexes.py
python .\mongodb\mongodb_verify.py
```

`mongodb_load.py` is the **users** loader; the other entities have dedicated loading scripts. **Do not repeat setup/import operations on the populated database without first checking for destructive actions or duplicate insertion.**

### Aggregation and analysis scripts

The implementation includes product/sales and category analyses; status counts; conversion-related session segment analyses by device and referrer; session duration; payments; and query-result text artifacts. Examples:

```powershell
python .\mongodb\mongodb_sales_analysis.py
python .\mongodb\mongodb_category_analysis.py
python .\mongodb\mongodb_conversion_by_device.py
python .\mongodb\mongodb_conversion_by_referrer.py
python .\mongodb\mongodb_payment_analysis.py
```

The actual MongoDB design supports aggregation concepts such as `$match`, `$unwind` of transaction `items`, `$group`, `$sort`, and grouping session documents by `device_profile.type` or `referrer`.

**Verified export:** `integration/export_mongodb.py` read **5,000 product records** and processed **500,000 transactions**, finding **4,766** product IDs appearing in transaction items. The remaining **234** catalog products were absent from scanned transaction items; that does **not** mean they had no browsing views. Item subtotals exported at product level are **before transaction-level discounts**.

## 7. Part 1B — HBase modeling and queries

HBase was deployed via Docker. After an initial **Thrift startup issue**, the project used the functioning `hbase-recovery` container and existing storage volume with the problematic Thrift startup disabled.

### Schema

Defined in `hbase/schema.hbase`:

```ruby
create 'fp_user_sessions', 'info', 'pv', 'cart'
create 'fp_product_metrics', 'm'
```

| HBase table | Row key | Stored data |
|---|---|---|
| `fp_user_sessions` | `user_id#reverse_time#session_id` | `info`: metadata; `pv`: page views; `cart`: cart contents |
| `fp_product_metrics` | `product_id#YYYYMMDD` | `m:views` and `m:cart_quantity` |

`reverse_time = 9999999999 - Unix_timestamp`, allowing newer sessions to appear first within a user prefix. The metric table records **product-detail view events** and **units in final carts**. **It does not contain purchase counts**; purchases are analyzed from transactions in MongoDB.

### Loading and verification

`hbase/load_hbase.py` streamed data from `sessions_0.json` with `ijson` and generated HBase Shell `put` commands. Loading was tested in stages: **20**, then **1,000**, then **5,000** sessions. The final verified counts were:

- `fp_user_sessions`: **5,000 rows**.
- `fp_product_metrics`: **16,804 product-date rows**.

The existing sample consists of the **first 5,000 records in one session chunk**. Do not call it random or statistically representative. The production-like full 2-million-session HBase ingest was **not** performed.

To inspect the working container:

```powershell
docker ps --filter "name=hbase-recovery"
docker exec -it hbase-recovery hbase shell
```

Then, **inside HBase Shell**:

```ruby
list
count 'fp_user_sessions'
count 'fp_product_metrics'
scan 'fp_user_sessions', { LIMIT => 3 }
scan 'fp_product_metrics', { LIMIT => 3 }
```

`hbase/queries.hbase` contains additional sample queries, including user-key-oriented retrieval. **Only create tables from `schema.hbase` when they do not exist.** Replaying full `put` statements or creating tables on the populated HBase instance can change or conflict with existing results. The command-generation and HBase Shell loading approach should be followed from `load_hbase.py` and `load_commands.hbase`; the shell scripts were not converted into a direct Python Thrift loader.

## 8. Part 2 — Spark batch processing, SQL and cohort analysis

### Preparation and cleaning

The original `transactions.json` is a large JSON array. `spark/prepare_transactions.py` used streaming `ijson` processing to produce approximately **203 MB** of newline-delimited JSON (`spark/data/transactions.ndjson`). PySpark then loaded, validated and transformed the transaction data into Parquet.

From project root, after checking Spark configuration:

```powershell
Remove-Item Env:SPARK_HOME -ErrorAction SilentlyContinue
python .\spark\prepare_transactions.py
python .\spark\spark_clean.py
python .\spark\spark_batch.py
python .\spark\spark_sql_queries.py
python .\spark\spark_cohort.py
```

`prepare_transactions.py` and cleaning must run before scripts that consume their generated artifacts. These commands document the script sequence; run them only with their inputs available and check each script's output requirements on a fresh machine.

The cleaning stage standardized timestamp and text fields, converted top-level monetary totals to `decimal(18,2)`, validated IDs/timestamps/non-negative totals and removed duplicate transaction IDs. **Verified:**

| Check | Observed result |
|---|---:|
| Source transactions | 500,000 |
| Invalid under implemented rules | 0 |
| Duplicate transaction IDs | 0 |
| Cleaned transactions | 500,000 |

Nested item monetary fields were not all converted to decimals inside that particular cleaned schema; product-level monetary exports were handled in the MongoDB integration stage.

### Observed Spark SQL results

| Status | Transactions | Sum of transaction totals |
|---|---:|---:|
| `completed` | 317,055 | 264,428,273.18 |
| `delivered` | 61,226 | 67,830,723.08 |
| `processing` | 60,933 | 67,191,918.13 |
| `shipped` | 60,786 | 67,125,249.06 |
| **Total** | **500,000** | **466,576,163.45** |

The amount **466,576,163.45** includes multiple transaction statuses and is **not verified realized revenue or cash received**.

| Activity month | Transactions | Unique customers | Sum of transaction totals |
|---|---:|---:|---:|
| 2026-08 | 169,268 | 10,000 | 157,886,330.43 |
| 2026-09 | 166,157 | 10,000 | 154,991,898.17 |
| 2026-10 | 164,575 | 10,000 | 153,697,934.85 |

The SQL scripts also join user profiles and transactions on `user_id` to summarize customer registration cohorts.

### Cohort definition and limitation

Users were grouped by **registration month**. For each observed transaction month, the analysis computed distinct active users divided by total cohort users. The observed August–October cohort-month combinations all returned **100% activity**. This is a property of the synthetic data and a limited time window, **not** a validated 100% customer retention rate or a month-zero retention curve. Any transaction status counted as activity under the implemented definition.

## 9. Part 3 — Integration across MongoDB, HBase and Spark

**Question:** Which products attract browsing interest, and how does that compare with their completed-transaction quantity?

The project used a **file-mediated integration** rather than claiming live cross-database queries.

1. Run a full HBase Shell scan/export of `fp_product_metrics` to the text input consumed by `integration/convert_hbase_to_csv.py`. The project used `integration/hbase_product_metrics.txt`; the full export contained **16,804** rows.
2. Convert the HBase scan text into a structured CSV (all **16,804** rows were complete).
3. Export MongoDB products and transaction-item aggregates: **5,000** product rows and **4,766** product-sales rows.
4. With Spark, aggregate HBase product-day views/cart units by `product_id`, then left-join these metrics and MongoDB sales metrics onto the full **5,000-product catalog**.
5. Fill missing activity with zero and write the **5,000-row integrated product output**.

From the project root, **after the complete HBase text export exists**, the processing scripts are:

```powershell
python .\integration\convert_hbase_to_csv.py
python .\integration\export_mongodb.py
Remove-Item Env:SPARK_HOME -ErrorAction SilentlyContinue
python .\integration\spark_integrated_analysis.py
```

A full HBase Shell export is a prerequisite, not a step automatically performed by `convert_hbase_to_csv.py`. The text export format must match the parser's expected scan format. Inputs produced on the local PC were not all included in Git because generated/raw files may be large. For fresh-clone reproduction, first recreate/export these inputs.

### Independently verified integrated findings

| Comparison | Product | HBase sample views | HBase cart units | MongoDB completed-transaction units |
|---|---|---:|---:|---:|
| Most HBase product-detail views | `prod_01411` | 13 | 12 | 276 |
| Most units in completed transactions | `prod_01951` | 9 | 11 | 403 |

The leading product differs depending on the metric. **Do not calculate a purchase-conversion rate by dividing these completed units by HBase views**: the views come from 5,000 chosen sessions and purchases from the full 500,000-transaction dataset. The project did not establish causal effects or matched-session conversion.

## 10. Part 4 — Static visualizations

Run after integrated output exists:

```powershell
python .\visualizations\make_charts.py
```

The four produced charts are in `visualizations/charts/`:

| Chart | File | Meaning |
|---|---|---|
| 1 | `chart1_top_views.png` | Highest observed product-detail views in the HBase subset |
| 2 | `chart2_top_cart.png` | Cart quantities for the selected top-viewed products (not necessarily the global cart top ten) |
| 3 | `chart3_completed_quantity.png` | Highest completed-transaction quantities from MongoDB exports |
| 4 | `chart4_views_vs_completed.png` | HBase subset views vs full-data completed quantities (descriptive scatter) |

Among the ten highest-viewed products, observed views ranged from **10 to 13**; `prod_02399` had **17 cart units** with **11 detail views**. Cart units can exceed view events because a cart can contain multiple units. The scatter plot contains repeated integer view counts and broad differences in completed units; it is **not** a conversion model.

## 11. Report, presentation and study materials

The locally observed project structure included:

- `report/Technical_Report.pdf` — local PDF submission artifact; **confirm it is the current version of the final eight-page report**, rather than an earlier PDF.
- `report/make_architecture.py`, `report/build_report.py`, `report/build_presentation.py` — supporting artifact generation scripts.


Supporting build commands, when their expected inputs and packages are available:

```powershell
python .\report\make_architecture.py
python .\report\build_report.py
python .\report\build_presentation.py
```

The final report discusses data modeling, staged implementation, verified results, limitations, and scaling considerations; it is the reference for deeper explanation of the workflow. Verify the PDF's **6–8-page assignment requirement**, and ensure the official student name/ID are completed before submission.

## 12. Troubleshooting and decisions recorded during development

| Issue or decision | Actual approach |
|---|---|
| Original generator needed a correction | Retained the working fixed generator as the single `data_generation/dataset_generator.py`; original backed up outside the project |
| Very large JSON input | Used streaming `ijson`; split session generation into 20 chunks |
| MongoDB script reorganization | Moved `mongodb_*` scripts into `mongodb/`; verification still passed when launched from the project root |
| HBase Thrift startup issue | Used `hbase-recovery` and the existing storage volume; HBase Shell worked |
| HBase setup scale | Loaded 20, then 1,000, then 5,000 deterministic sessions instead of claiming 2 million loaded |
| Spark installation/version conflict | Cleared `SPARK_HOME` referring to Spark 3.5.9; used installed PySpark 4.2.1 |
| Integration without live connectors | Exported HBase and MongoDB results to files and joined in Spark |
| Project organization | Kept one root `README.md`; moved inspection scripts into `utilities/`; kept raw JSON inputs at root for relative paths |

These decisions matter for reproducibility; they also define what this prototype **did not** demonstrate (production scalability or end-to-end real-time data streaming).

## 13. Reproducibility and submission checks

A new reader should run the stages in this order, not skip prerequisites:

1. Install Python dependencies, MongoDB, Docker/HBase, Java and PySpark; check versions and connectivity.
2. From the **project root**, generate the raw JSON files only if they do not already exist; validate them using `utilities/validate_datasets.py` and inspection scripts as appropriate.
3. On a **fresh MongoDB database**, run setup/loaders and verify the five collection counts; run aggregation scripts.
4. Create the two HBase tables **if missing**; generate/load the chosen 5,000-session sample and verify both row counts.
5. Convert transactions to NDJSON, clean them to Parquet, then run Spark SQL and cohort analyses.
6. Scan/export all HBase product metrics, convert that export to CSV, export MongoDB product metrics, and execute the Spark integrated analysis.
7. Produce four charts and check that they match the scope of the source data.
8. Confirm Word/PDF technical report, architecture, PowerPoint, project source, and evidence/screenshots.
9. Review `.gitignore`, ensure no secrets or large generated data are being committed, then upload the repository and an accompanying matching ZIP if required.

### Safe local verification commands

```powershell
# Confirm critical source and deliverables.
Test-Path .\data_generation\dataset_generator.py
Test-Path .\mongodb\mongodb_verify.py
Test-Path .\hbase\schema.hbase
Test-Path .\spark\spark_clean.py
Test-Path .\integration\spark_integrated_analysis.py
Test-Path .\report\Technical_Report.pdf
Test-Path .\report\Final_Project_Presentation.pptx
Get-ChildItem .\visualizations\charts\*.png

# Confirm services and existing MongoDB records.
docker ps --filter "name=hbase-recovery"
python .\mongodb\mongodb_verify.py

# Check what Git plans to upload, after initializing the repository.
git status --short
git check-attr filter -- users.json products.json transactions.json sessions_0.json spark/data/transactions.ndjson
```

**How to restore the project from GitHub**

Install Git and Git LFS, then run:

```powershell
git lfs install
git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
git lfs pull
```

Replace the placeholders with the actual GitHub repository URL and folder name.

After downloading the repository, the original JSON and Spark datasets should be available locally if all Git LFS uploads were completed successfully.

**Important reproducibility notes**

- MongoDB collections and HBase tables must be recreated or restored separately using the provided data, scripts, and schema.
- GitHub does not automatically back up running database services or Docker volumes.
- The saved analytical results correspond to the original synthetic datasets. Regenerating random datasets may produce different results.
- The integrated analysis compares browsing metrics from 5,000 selected HBase sessions with transaction quantities from MongoDB. It does not calculate a validated purchase conversion rate.
- The reported 20.29% overall conversion rate must not be presented as verified unless independently established.
- Before submission, confirm that the final PDF matches the eight-page technical report and includes the student's correct identification.
- Verify that the Git push and all Git LFS uploads finish successfully before deleting any local data.

## 14. Technology trade-offs and limitations

- **MongoDB**: flexible documents and embedded arrays aid application-style queries and aggregation; indexes and sharding would matter at larger scale.
- **HBase**: sorted row-key access fits user-history and product-day time series; row-key hotspots, RegionServer distribution and bulk ingestion require attention in a real deployment.
- **Spark**: DataFrames/SQL efficiently express cleaning, grouping and joins; the documented local run was **not** a multi-node Spark benchmark.
- **CSV bridging**: transparent and practical for this local demonstration, but adds manual file-export steps and is not a real-time database integration mechanism.
- **Synthetic data**: observed purchase statuses, activity rates and product rankings are illustrative. HBase browsing and MongoDB transactions differ in population, so cross-source views/purchases cannot establish causal effects or true conversion.

## 15. Conclusion

The project implemented an end-to-end, **multi-model e-commerce analytics proof of concept**. MongoDB held **2,515,025** documents; HBase held **5,000** chosen session records and **16,804** product-date metrics; Spark cleaned and analyzed **500,000** transactions; the integrated output retained **5,000** products and supported four visualizations. The implementation demonstrates appropriate storage-model choices, joins by shared identifiers, staged validation and evidence-aware interpretation, with clearly stated local-scale and data-coverage limitations.
