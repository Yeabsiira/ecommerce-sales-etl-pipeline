import sys
from pathlib import Path

# Ensure Python can resolve modules relative to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.extract.extract_data import extract_raw_data
from src.transform.clean_customers import transform_customers
from src.transform.clean_products import transform_products
from src.transform.clean_orders import transform_orders
from src.transform.build_star_schema import assemble_star_schema
from src.load.load_to_postgres import load_star_schema

def run_complete_etl():
    print("🏁 Initiating Production ETL Pipeline Loop...\n")
    
    # 1. Extraction Phase
    try:
        raw_data = extract_raw_data()
    except Exception as e:
        print(f"❌ Pipeline Ingestion Aborted: {e}")
        return

    # 2. Transformation Phase
    print("\n⚡ Running Data Transformations...")
    try:
        star_schema = assemble_star_schema(
            extracted_data=raw_data,
            clean_cust=transform_customers,
            clean_prod=transform_products,
            clean_ord=transform_orders
        )
    except Exception as e:
        print(f"❌ Pipeline Transformation Aborted: {e}")
        return

    # 3. Target Loading Phase
    print("\n📤 Initiating Target Database Load...")
    try:
        load_star_schema(star_schema)
        print("\n🏆 ETL Pipeline Completed and Database populated successfully!")
    except Exception as e:
        print(f"❌ Pipeline Loading Operation Crashed: {e}")

if __name__ == "__main__":
    run_complete_etl()