import sys
import logging
from pathlib import Path

# Ensure Python can resolve modules relative to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.extract.extract_data import extract_raw_data
from src.transform.clean_customers import transform_customers
from src.transform.clean_products import transform_products
from src.transform.clean_orders import transform_orders
from src.transform.clean_sellers import transform_sellers
from src.transform.build_star_schema import assemble_star_schema
from src.load.load_to_postgres import load_star_schema

# Setup structured console logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("🏁 Initiating Production ETL Pipeline Loop...")

    # 1. Extraction Phase
    try:
        logger.info("🚀 Starting Data Extraction Phase...")
        raw_data = extract_raw_data()
    except Exception as e:
        logger.error(f"❌ Pipeline Ingestion Aborted: {e}", exc_info=True)
        sys.exit(1)

    # 2. Transformation Phase
    logger.info("⚡ Running Data Transformations...")
    try:
        star_schema = assemble_star_schema(
            extracted_data=raw_data,
            clean_cust=transform_customers,
            clean_prod=transform_products,
            clean_ord=transform_orders,
            clean_sell=transform_sellers
        )
    except Exception as e:
        logger.error(f"❌ Pipeline Transformation Aborted: {e}", exc_info=True)
        sys.exit(1)

    # 3. Target Loading Phase
    logger.info("📤 Initiating Target Database Load...")
    try:
        load_star_schema(star_schema)
        logger.info("🏆 ETL Pipeline Completed and Database populated successfully!")
    except Exception as e:
        logger.error(f"❌ Pipeline Loading Operation Crashed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()