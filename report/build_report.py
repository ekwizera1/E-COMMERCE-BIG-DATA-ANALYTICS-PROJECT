from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create paths
report_folder = Path("report")
report_folder.mkdir(exist_ok=True)

output_file = report_folder / "Technical_Report.docx"

# Create a new Word document
doc = Document()

# Set default font size
styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(11)

# Helper function to add a heading
def add_heading(text, level=1):
    doc.add_heading(text, level=level)

# Helper function to add a paragraph
def add_paragraph(text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    return p

# Helper function to add a bullet list
def add_bullet(text):
    doc.add_paragraph(text, style="List Bullet")

# Title page
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("E-COMMERCE BIG DATA ANALYTICS PROJECT")
run.bold = True
run.font.size = Pt(18)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("Technical Report")
run.italic = True
run.font.size = Pt(14)

doc.add_paragraph("")
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info.add_run("Student: Eric KWIZERA\n")
info.add_run("Course: Big Data / Distributed Multi-Model Analytics\n")
info.add_run("Project: FinalProjectBD\n")
info.add_run("Date: November 2026\n")

doc.add_page_break()

# 1. Introduction
add_heading("1. Introduction", level=1)
add_paragraph(
    "This project presents a complete e-commerce big data analytics workflow. "
    "The work covers synthetic data generation, data storage in MongoDB and HBase, "
    "data processing with Apache Spark, integrated analytics, and data visualization. "
    "The purpose was to build a practical multi-model analytics system and demonstrate "
    "how different big data tools can work together in one project."
)

# 2. Objectives
add_heading("2. Project Objectives", level=1)
add_bullet("Generate a realistic e-commerce dataset.")
add_bullet("Store and analyze data in MongoDB.")
add_bullet("Store session and browsing metrics in HBase.")
add_bullet("Use Apache Spark for cleaning and large-scale analytics.")
add_bullet("Integrate outputs from MongoDB and HBase.")
add_bullet("Create visualizations and final reporting deliverables.")

# 3. Dataset generation
add_heading("3. Dataset Generation", level=1)
add_paragraph(
    "The dataset was generated using a custom Python generator. "
    "The generator created users, categories, products, transactions, and browsing sessions."
)

table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Dataset"
hdr[1].text = "Count"

data_rows = [
    ("Users", "10,000"),
    ("Products", "5,000"),
    ("Categories", "25"),
    ("Transactions", "500,000"),
    ("Sessions", "2,000,000")
]

for left, right in data_rows:
    row = table.add_row().cells
    row[0].text = left
    row[1].text = right

add_paragraph(
    "The generated JSON files were validated successfully before loading into the storage systems."
)

# 4. MongoDB
add_heading("4. MongoDB Implementation", level=1)
add_paragraph(
    "MongoDB was used to store the main project data. "
    "The collections created in the ecommerce_db database were users, products, categories, transactions, and sessions."
)

table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Collection"
hdr[1].text = "Documents"

mongo_rows = [
    ("categories", "25"),
    ("products", "5,000"),
    ("sessions", "2,000,000"),
    ("transactions", "500,000"),
    ("users", "10,000")
]

for left, right in mongo_rows:
    row = table.add_row().cells
    row[0].text = left
    row[1].text = right

add_paragraph("Key MongoDB findings:", bold=True)
add_bullet("Total transactions: 500,000")
add_bullet("Overall transaction value: 466,576,163.45")
add_bullet("Completed transactions: 317,055")
add_bullet("Overall conversion rate: 20.29%")
add_bullet("Traffic sources were almost evenly distributed across social, affiliate, email, direct, and search_engine.")
add_bullet("Device conversion rates were also similar across tablet, desktop, and mobile.")

# 5. HBase
add_heading("5. HBase Implementation", level=1)
add_paragraph(
    "HBase was used to store browsing-oriented data in a column-family model. "
    "Because the full sessions dataset was very large, a sample of 5,000 sessions from sessions_0.json "
    "was loaded into HBase for this stage of the project."
)

add_paragraph("Two HBase tables were created:", bold=True)
add_bullet("fp_user_sessions: stores session details, page views, and cart data.")
add_bullet("fp_product_metrics: stores product-date browsing metrics.")

add_paragraph("HBase loading results:", bold=True)
add_bullet("fp_user_sessions rows: 5,000")
add_bullet("fp_product_metrics rows: 16,804")

add_paragraph(
    "The HBase row key for sessions used user_id, reverse timestamp logic, and session_id. "
    "This design supports user-based and recent-session access patterns."
)

# 6. Spark
add_heading("6. Apache Spark Processing and Analytics", level=1)
add_paragraph(
    "Apache Spark was used for batch analytics. "
    "The transactions dataset was converted to NDJSON format and processed with PySpark."
)

add_paragraph("Spark cleaning results:", bold=True)
add_bullet("Original transactions: 500,000")
add_bullet("Invalid transactions: 0")
add_bullet("Duplicate rows removed: 0")
add_bullet("Clean transactions: 500,000")

add_paragraph("Spark SQL query highlights:", bold=True)
add_bullet("Completed status had the highest number of transactions and highest transaction value.")
add_bullet("Monthly transaction activity was observed across August, September, and October 2026.")
add_bullet("Customer transactions were also summarized by registration month.")

add_paragraph("Monthly transaction trends:", bold=True)
table = doc.add_table(rows=1, cols=4)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Month"
hdr[1].text = "Transactions"
hdr[2].text = "Unique Customers"
hdr[3].text = "Transaction Value"

spark_months = [
    ("2026-08", "169,268", "10,000", "157,886,330.43"),
    ("2026-09", "166,157", "10,000", "154,991,898.17"),
    ("2026-10", "164,575", "10,000", "153,697,934.85")
]

for a, b, c, d in spark_months:
    row = table.add_row().cells
    row[0].text = a
    row[1].text = b
    row[2].text = c
    row[3].text = d

add_paragraph("Cohort analysis:", bold=True)
add_bullet("Registration cohorts were created from February 2026 to August 2026.")
add_bullet("The observed activity rate in the generated dataset was 100% for the available active months.")
add_bullet("Cohort results were saved successfully for reporting purposes.")

# 7. Integrated analytics
add_heading("7. Integrated Analytics", level=1)
add_paragraph(
    "The integrated analysis combined MongoDB product information, MongoDB product sales metrics, "
    "and HBase browsing metrics. The integration was performed using product_id as the common key."
)

add_bullet("MongoDB products exported: 5,000")
add_bullet("MongoDB products with transaction items: 4,766")
add_bullet("HBase product-date records: 16,804")
add_bullet("Integrated products: 5,000")

add_paragraph("Examples of integrated insights:", bold=True)
add_bullet("Top products were identified by browsing views.")
add_bullet("Top products were identified by completed transaction quantity.")
add_bullet("Browsing views and completed quantities were compared visually.")

# 8. Architecture diagram
add_heading("8. System Architecture", level=1)
add_paragraph(
    "The following architecture diagram summarizes the full project workflow from dataset generation "
    "to storage, processing, integration, visualization, and reporting."
)

architecture_path = report_folder / "architecture.png"
if architecture_path.exists():
    doc.add_picture(str(architecture_path), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
else:
    add_paragraph("Architecture diagram file not found.")

# 9. Visualizations
add_heading("9. Visualizations", level=1)
add_paragraph(
    "Four charts were created to summarize the main integrated analytics outputs."
)

chart_files = [
    ("chart1_top_views.png", "Figure 1. Top products by browsing views."),
    ("chart2_top_cart.png", "Figure 2. Top products by cart quantity."),
    ("chart3_completed_quantity.png", "Figure 3. Top products by completed transaction quantity."),
    ("chart4_views_vs_completed.png", "Figure 4. Browsing views versus completed transaction quantity.")
]

charts_folder = Path("visualizations") / "charts"

for file_name, caption in chart_files:
    chart_path = charts_folder / file_name
    if chart_path.exists():
        doc.add_picture(str(chart_path), width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = doc.add_paragraph(caption)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        add_paragraph(f"Missing chart: {file_name}")

# 10. Challenges
add_heading("10. Challenges Encountered", level=1)
add_bullet("MongoDB was not initially installed and had to be configured.")
add_bullet("The original HBase container failed because of the thrift startup issue.")
add_bullet("A recovery container had to be created to run HBase without the problematic thrift startup.")
add_bullet("Spark initially failed because of environment and Java compatibility issues.")
add_bullet("Large data volumes required careful step-by-step validation.")

# 11. Conclusion
add_heading("11. Conclusion", level=1)
add_paragraph(
    "This project successfully demonstrated a full big data analytics pipeline for e-commerce data. "
    "MongoDB handled document-based storage, HBase supported column-family browsing analytics, "
    "and Spark enabled scalable processing and reporting. The final outputs included integrated analysis, "
    "visual charts, and system documentation. The project also provided practical experience in debugging, "
    "data integration, and multi-tool analytics workflows."
)

# Save the report
doc.save(output_file)

print("Technical report created successfully.")
print("Saved to:", output_file)