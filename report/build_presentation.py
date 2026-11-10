
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image

# Set project folders.
output_dir = Path("report")
output_dir.mkdir(exist_ok=True)

charts_dir = Path("visualizations/charts")
architecture = Path("report/architecture.png")

# Create a widescreen PowerPoint presentation.
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BLUE = RGBColor(20, 55, 95)
DARK = RGBColor(45, 55, 70)
LIGHT = RGBColor(245, 248, 252)

# Add text to a slide.
def add_text(slide, text, x, y, w, h, size=20, bold=False):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    frame = box.text_frame
    frame.word_wrap = True
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = DARK
    return box

# Create a slide with a title and bullet points.
def add_bullet_slide(title, bullet_points):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_text(slide, title, 0.7, 0.4, 12, 0.7, 29, True)

    y = 1.5
    for item in bullet_points:
        add_text(slide, "- " + item, 1.0, y, 11.3, 0.85, 20)
        y += 0.9

    return slide

# Add an image without changing its proportions.
def add_image_fit(slide, path, x, y, max_w, max_h):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Missing image: {path}")

    with Image.open(path) as img:
        image_w, image_h = img.size

    ratio = min(max_w / image_w, max_h / image_h)
    width = image_w * ratio
    height = image_h * ratio

    left = x + (max_w - width) / 2
    top = y + (max_h - height) / 2

    slide.shapes.add_picture(
        str(path),
        Inches(left),
        Inches(top),
        width=Inches(width)
    )

# Add a chart slide.
def add_chart_slide(title, image_name, explanation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_text(slide, title, 0.7, 0.3, 12, 0.6, 27, True)

    add_image_fit(
        slide,
        charts_dir / image_name,
        0.8, 1.0, 11.7, 5.1
    )

    add_text(slide, explanation, 0.9, 6.25, 11.5, 0.85, 15)
    return slide


# SLIDE 1: TITLE
slide = prs.slides.add_slide(prs.slide_layouts[6])

add_text(
    slide,
    "DISTRIBUTED MULTI-MODEL ANALYTICS",
    1.1, 1.5, 11.3, 0.9, 33, True
)

add_text(
    slide,
    "FOR E-COMMERCE DATA",
    1.1, 2.4, 11.3, 0.8, 30, True
)

add_text(
    slide,
    "MongoDB | HBase | Apache Spark | Data Visualization",
    1.1, 3.7, 11.2, 0.8, 21
)

add_text(
    slide,
    "Final Big Data Project - November 2026\n"
    "Student / Group: Add names and IDs",
    1.1, 5.4, 11.2, 1.0, 17
)


# SLIDE 2: PROJECT OBJECTIVES
add_bullet_slide(
    "Project Objectives",
    [
        "Generate and validate a large e-commerce dataset.",
        "Store document data in MongoDB.",
        "Store browsing and cart metrics in HBase.",
        "Process transactions using Apache Spark.",
        "Integrate data sources and visualize business findings."
    ]
)


# SLIDE 3: SYSTEM ARCHITECTURE
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, "System Architecture", 0.7, 0.3, 12, 0.7, 29, True)
add_image_fit(slide, architecture, 0.6, 1.0, 12.1, 6.1)


# SLIDE 4: DATASET AND MONGODB
add_bullet_slide(
    "Dataset Generation and MongoDB",
    [
        "Generated 10,000 users and 5,000 products.",
        "Generated 25 categories and 500,000 transactions.",
        "Generated 2,000,000 browsing sessions.",
        "Stored 2,515,025 documents in MongoDB.",
        "Used document collections and aggregation queries."
    ]
)


# SLIDE 5: HBASE
add_bullet_slide(
    "HBase Implementation",
    [
        "Created fp_user_sessions and fp_product_metrics tables.",
        "Loaded 5,000 browsing sessions as a deterministic subset.",
        "Stored 16,804 product-date metric records.",
        "Recorded product-detail views and cart quantities.",
        "Designed row keys to support user and product access."
    ]
)


# SLIDE 6: APACHE SPARK
add_bullet_slide(
    "Apache Spark Data Processing",
    [
        "Processed 500,000 transactions using PySpark.",
        "Converted transaction JSON to NDJSON for Spark.",
        "Checked invalid records and duplicate transaction IDs.",
        "Found zero invalid and zero duplicate transactions.",
        "Saved cleaned data in Parquet format."
    ]
)


# SLIDE 7: SPARK SQL AND COHORT ANALYSIS
add_bullet_slide(
    "Spark SQL and Cohort Analysis",
    [
        "Completed transactions: 317,055.",
        "Total transaction value: 466,576,163.45.",
        "Analyzed August, September and October 2026.",
        "Joined customers with transactions using user_id.",
        "Monthly cohort activity rate was 100% in the synthetic dataset."
    ]
)


# SLIDE 8: INTEGRATED ANALYTICS
add_bullet_slide(
    "Integrated Analytics: MongoDB + HBase + Spark",
    [
        "Business question: Which products attract browsing interest?",
        "Exported product and transaction metrics from MongoDB.",
        "Exported product views and cart quantities from HBase.",
        "Joined datasets in Spark using product_id.",
        "Successfully integrated all 5,000 products."
    ]
)


# SLIDE 9: CHART 1
add_chart_slide(
    "Top Products by Browsing Views",
    "chart1_top_views.png",
    "Product prod_01411 had the highest observed views (13) "
    "in the 5,000-session HBase subset."
)


# SLIDE 10: CHART 2
add_chart_slide(
    "Top Products by Cart Quantity",
    "chart2_top_cart.png",
    "This chart compares product quantities recorded in "
    "shopping carts in the HBase subset."
)


# SLIDE 11: CHART 3
add_chart_slide(
    "Top Products by Completed Quantity",
    "chart3_completed_quantity.png",
    "Product prod_01951 had the highest completed "
    "transaction quantity (403 units)."
)


# SLIDE 12: CHART 4
add_chart_slide(
    "Browsing Views vs Completed Quantity",
    "chart4_views_vs_completed.png",
    "Browsing uses a 5,000-session subset while transactions "
    "use the full data. This is not a conversion rate."
)


# SLIDE 13: CHALLENGES AND CONCLUSION
add_bullet_slide(
    "Challenges, Limitations and Conclusion",
    [
        "HBase startup required troubleshooting and recovery.",
        "Spark configuration conflicts were resolved.",
        "HBase sampling limits direct conversion comparisons.",
        "Synthetic cohort results do not prove real customer retention.",
        "The project demonstrates integrated multi-model analytics."
    ]
)


# Save the PowerPoint presentation.
output_file = output_dir / "Final_Project_Presentation.pptx"
prs.save(output_file)

print("PowerPoint presentation created successfully.")
print("Total slides:", len(prs.slides))
print("Saved to:", output_file)
