
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Create the output folder.
output_folder = Path("report")
output_folder.mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(15, 9))
ax.set_xlim(0, 15)
ax.set_ylim(0, 10)
ax.axis("off")

# Draw a labeled system component.
def draw_box(x, y, width, height, title, details, color):
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.15",
        linewidth=1.5,
        edgecolor="#334155",
        facecolor=color
    )
    ax.add_patch(box)

    ax.text(
        x + width / 2,
        y + height * 0.68,
        title,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold"
    )

    ax.text(
        x + width / 2,
        y + height * 0.32,
        details,
        ha="center",
        va="center",
        fontsize=9,
        linespacing=1.4
    )

# Draw data movement arrows.
def draw_arrow(start, end):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=1.8,
        color="#475569"
    )
    ax.add_patch(arrow)

ax.text(
    7.5, 9.6,
    "E-COMMERCE BIG DATA SYSTEM ARCHITECTURE",
    ha="center",
    fontsize=18,
    fontweight="bold"
)

# Layer 1: Data generation.
draw_box(
    5.2, 8.0, 4.6, 1.1,
    "DATA GENERATION",
    "10,000 users | 5,000 products\n500,000 transactions | 2M sessions",
    "#dbeafe"
)

# Layer 2: Storage and processing.
draw_box(
    0.5, 5.4, 4.0, 1.5,
    "MongoDB",
    "Products, users, categories\nTransactions and sessions",
    "#dcfce7"
)

draw_box(
    5.5, 5.4, 4.0, 1.5,
    "HBase",
    "5,000-session subset\nBrowsing and cart metrics",
    "#fef3c7"
)

draw_box(
    10.5, 5.4, 4.0, 1.5,
    "Apache Spark",
    "Data cleaning, Spark SQL\nJOINs and cohort analysis",
    "#fce7f3"
)

# Connections from generated data.
draw_arrow((6.2, 8.0), (2.5, 7.0))
draw_arrow((7.5, 8.0), (7.5, 7.0))
draw_arrow((8.8, 8.0), (12.5, 7.0))

# Layer 3: Data integration.
draw_box(
    4.7, 3.1, 5.6, 1.3,
    "INTEGRATED ANALYTICS",
    "MongoDB + HBase exports\nSpark JOIN using product_id",
    "#e0e7ff"
)

draw_arrow((2.5, 5.4), (5.6, 4.5))
draw_arrow((7.5, 5.4), (7.5, 4.5))
draw_arrow((12.5, 5.4), (9.4, 4.5))

# Layer 4: Results and reporting.
draw_box(
    1.3, 0.9, 5.2, 1.1,
    "VISUALIZATIONS",
    "Four product analytics charts",
    "#f1f5f9"
)

draw_box(
    8.5, 0.9, 5.2, 1.1,
    "FINAL DELIVERABLES",
    "Technical report, presentation\nSource code and study guide",
    "#f1f5f9"
)

draw_arrow((6.4, 3.1), (4.0, 2.1))
draw_arrow((8.6, 3.1), (11.0, 2.1))

ax.text(
    7.5, 0.3,
    "HBase browsing metrics use a subset; MongoDB transaction metrics use the full dataset.",
    ha="center",
    fontsize=9,
    color="#475569"
)

plt.savefig(
    output_folder / "architecture.png",
    dpi=220,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()
print("Architecture diagram created successfully.")
print("Saved to: report/architecture.png")
