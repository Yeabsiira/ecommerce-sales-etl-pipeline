# Olist E-Commerce Data Warehouse & ETL Pipeline

An end-to-end, production-grade Data Engineering pipeline that extracts raw Brazilian retail e-commerce datasets, applies structural business logic transformations using Pandas, and streams the records into a structured PostgreSQL Star Schema Data Warehouse. The warehouse layers feed a real-time executive analytical dashboard built using Streamlit and Plotly.

## 🏗️ Data Warehouse Architecture (Star Schema)

The pipeline converts transactional logs into a performance-optimized Star Schema built for fast analytical query executions:
* **Fact Table:** `fact_orders` (Tracks pricing, logistical metrics, performance days, and review ratings)
* **Dimension Tables:** `dim_customers`, `dim_products`, `dim_date` (Dynamic calendar lookup table built from purchase history)

## 📁 Repository Structure

Following standard software engineering principles, components are isolated by context:
* `src/extract/` - Validates and processes ingestion routines from raw CSV files.
* `src/transform/` - Performs analytical data type casting, string cleaning, and constructs entity frames.
* `src/load/` - Sequence-controlled DDL script runner and multi-chunk streaming layer.
* `sql/schema/` - Ordered DDL migration files managing primary and foreign key references.
* `sql/analysis/` - Optimized windowing and analytical reporting logic scripts.
* `dashboard/` - High-level visualization reporting tier.

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ecommerce-etl-pipeline.git](https://github.com/YOUR_USERNAME/ecommerce-etl-pipeline.git)
   cd ecommerce-etl-pipeline