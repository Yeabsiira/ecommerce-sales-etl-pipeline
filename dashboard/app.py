import streamlit as pd
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import sys
from pathlib import Path

# Ensure the app can import config from src/
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.config import Config

# Set up page configurations
st.set_page_config(
    page_title="Olist E-Commerce Data Warehouse Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def get_db_connection():
    """Establishes a cached connection engine to the Postgres warehouse."""
    return create_engine(Config.get_connection_string())

engine = get_db_connection()

st.title("📊 Olist E-Commerce Executive Dashboard")
st.markdown("This dashboard reflects real-time analytics streamed from our structured PostgreSQL Star Schema.")

# --- DATA FETCHING LAYER ---
@st.cache_data(ttl=600)
def fetch_dashboard_data():
    """Queries warehouse tables to fetch aggregate data frames for visualization."""
    # 1. Fetch Monthly Revenue Trend
    revenue_query = """
        SELECT d.year, d.month, SUM(f.payment_value) as revenue, COUNT(DISTINCT f.order_id) as orders
        FROM fact_orders f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.year, d.month ORDER BY d.year, d.month;
    """
    df_rev = pd.read_sql(revenue_query, engine)
    df_rev["period"] = df_rev["year"].astype(str) + "-" + df_rev["month"].astype(str).str.zfill(2)

    # 2. Fetch Top Performing Categories
    category_query = """
        SELECT p.product_category, ROUND(SUM(f.price)::numeric, 2) as total_sales
        FROM fact_orders f
        JOIN dim_products p ON f.product_id = p.product_id
        GROUP BY p.product_category ORDER BY total_sales DESC LIMIT 10;
    """
    df_cat = pd.read_sql(category_query, engine)

    # 3. Fetch KPI Highlights
    kpi_query = """
        SELECT 
            ROUND(SUM(payment_value)::numeric, 2) as total_revenue,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(AVG(review_score)::numeric, 2) as avg_rating
        FROM fact_orders;
    """
    df_kpi = pd.read_sql(kpi_query, engine)
    
    return df_rev, df_cat, df_kpi

# Execute data fetching
try:
    df_rev, df_cat, df_kpi = fetch_dashboard_data()
    
    # --- METRICS BAR ---
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"${df_kpi['total_revenue'][0]:,}")
    col2.metric("📦 Total Orders", f"{df_kpi['total_orders'][0]:,}")
    col3.metric("⭐ Avg Review Score", f"{df_kpi['avg_rating'][0]} / 5.0")
    
    st.markdown("---")
    
    # --- CHARTS LAYER ---
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("📈 Monthly Revenue Trend")
        fig_rev = px.line(df_rev, x="period", y="revenue", labels={"revenue": "Revenue ($)", "period": "Month"}, markers=True)
        st.plotly_chart(fig_rev, use_container_width=True)
        
    with right_col:
        st.subheader("🏆 Top 10 Product Categories by Sales")
        fig_cat = px.bar(df_cat, x="total_sales", y="product_category", orientation='h', labels={"total_sales": "Sales ($)", "product_category": "Category"})
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)

except Exception as e:
    st.error(f"❌ Failed to render dashboard widgets: {e}")