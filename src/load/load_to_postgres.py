from sqlalchemy import text
from pathlib import Path
from src.load.db_connection import get_db_engine

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCHEMA_DIR = BASE_DIR / "sql" / "schema"

def execute_sql_file(conn, file_path):
    """Helper function to read and execute statements within a specific SQL file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Missing required schema script at: {file_path}")
    
    with open(file_path, "r") as file:
        sql_script = file.read()
        
    for statement in sql_script.split(";"):
        clean_statement = statement.strip()
        if clean_statement:
            conn.execute(text(clean_statement))

def load_star_schema(star_schema_dfs):
    """Executes DDL schemas sequentially and streams dataframes into PostgreSQL."""
    engine = get_db_engine()
    
    # 1. Execute SQL definitions in absolute order
    print("🔨 Setting up database tables sequentially...")
    with engine.connect() as conn:
        print("➡️ Creating Dimension Tables (01_create_dimensions.sql)...")
        execute_sql_file(conn, SCHEMA_DIR / "01_create_dimensions.sql")
        
        print("➡️ Creating Fact Tables (02_create_facts.sql)...")
        execute_sql_file(conn, SCHEMA_DIR / "02_create_facts.sql")
        
    print("✅ Schema architecture successfully deployed to PostgreSQL.")

    # 2. Bulk stream dimensions first (order matters for FK constraints)
    dimensions = ["dim_customers", "dim_products", "dim_sellers", "dim_date"]
    for dim in dimensions:
        print(f"📥 Streaming dataframe into dimension table: {dim}...")
        star_schema_dfs[dim].to_sql(name=dim, con=engine, if_exists="append", index=False, method="multi", chunksize=10000)
        print(f"🎉 Completed {dim} load.")

    # 3. Stream the central fact table last
    print("📥 Streaming dataframe into fact table: fact_orders...")
    star_schema_dfs["fact_orders"].to_sql(name="fact_orders", con=engine, if_exists="append", index=False, method="multi", chunksize=10000)
    print("🎉 Completed fact_orders load.")
    
    print("\n📦 Target Database Loading Phase 100% Finalized!")