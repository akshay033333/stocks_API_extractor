import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Stock Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def load_csv_files():
    """Load all CSV files from the current directory"""
    csv_files = glob.glob("*.csv")
    return sorted(csv_files, reverse=True)  # Most recent first

def load_data(file_path):
    """Load CSV data into pandas DataFrame"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading file {file_path}: {str(e)}")
        return None

def get_file_info(file_path):
    """Get file information"""
    stat = os.stat(file_path)
    size_mb = stat.st_size / (1024 * 1024)
    modified_time = datetime.fromtimestamp(stat.st_mtime)
    return {
        'size_mb': round(size_mb, 2),
        'modified': modified_time.strftime("%Y-%m-%d %H:%M:%S"),
        'rows': len(pd.read_csv(file_path)) if os.path.exists(file_path) else 0
    }

def create_market_distribution_chart(df):
    """Create market distribution pie chart"""
    if 'market' in df.columns:
        market_counts = df['market'].value_counts()
        fig = px.pie(
            values=market_counts.values,
            names=market_counts.index,
            title="Market Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    return None

def create_exchange_distribution_chart(df):
    """Create exchange distribution bar chart"""
    if 'primary_exchange' in df.columns:
        exchange_counts = df['primary_exchange'].value_counts().head(10)
        fig = px.bar(
            x=exchange_counts.index,
            y=exchange_counts.values,
            title="Top 10 Exchanges by Ticker Count",
            labels={'x': 'Exchange', 'y': 'Number of Tickers'},
            color=exchange_counts.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    return None

def create_type_distribution_chart(df):
    """Create security type distribution chart"""
    if 'type' in df.columns:
        type_counts = df['type'].value_counts()
        fig = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Security Type Distribution",
            labels={'x': 'Security Type', 'y': 'Count'},
            color=type_counts.values,
            color_continuous_scale='Viridis'
        )
        return fig
    return None

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Stock Data Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load available CSV files
    csv_files = load_csv_files()
    
    if not csv_files:
        st.warning("No CSV files found in the current directory.")
        st.info("Run the Script.py to generate stock data CSV files first.")
        return
    
    # Sidebar for file selection
    st.sidebar.header("📁 File Selection")
    selected_file = st.sidebar.selectbox(
        "Choose a CSV file to analyze:",
        csv_files,
        help="Select a CSV file to view and analyze its contents"
    )
    
    # File information
    if selected_file:
        file_info = get_file_info(selected_file)
        st.sidebar.markdown("### 📋 File Information")
        st.sidebar.metric("File Size", f"{file_info['size_mb']} MB")
        st.sidebar.metric("Total Rows", f"{file_info['rows']:,}")
        st.sidebar.metric("Last Modified", file_info['modified'])
    
    # Load data
    if selected_file:
        df = load_data(selected_file)
        
        if df is not None:
            # Main content area
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Tickers", f"{len(df):,}")
            
            with col2:
                unique_exchanges = df['primary_exchange'].nunique() if 'primary_exchange' in df.columns else 0
                st.metric("Unique Exchanges", unique_exchanges)
            
            with col3:
                unique_types = df['type'].nunique() if 'type' in df.columns else 0
                st.metric("Security Types", unique_types)
            
            with col4:
                if 'currency_name' in df.columns:
                    currencies = df['currency_name'].nunique()
                    st.metric("Currencies", currencies)
                else:
                    st.metric("Currencies", "N/A")
            
            st.markdown("---")
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Data Explorer", "📈 Analytics", "📋 Raw Data"])
            
            with tab1:
                st.subheader("Data Overview")
                
                # Display basic statistics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Column Information:**")
                    st.write(f"- Total Columns: {len(df.columns)}")
                    st.write(f"- Total Rows: {len(df):,}")
                    st.write(f"- Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                
                with col2:
                    st.write("**Data Types:**")
                    dtype_counts = df.dtypes.value_counts()
                    for dtype, count in dtype_counts.items():
                        st.write(f"- {dtype}: {count} columns")
                
                # Show sample data
                st.subheader("Sample Data (First 10 Rows)")
                st.dataframe(df.head(10), use_container_width=True)
            
            with tab2:
                st.subheader("Data Explorer")
                
                # Filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if 'primary_exchange' in df.columns:
                        exchanges = ['All'] + sorted(df['primary_exchange'].unique().tolist())
                        selected_exchange = st.selectbox("Filter by Exchange:", exchanges)
                    else:
                        selected_exchange = 'All'
                
                with col2:
                    if 'type' in df.columns:
                        types = ['All'] + sorted(df['type'].unique().tolist())
                        selected_type = st.selectbox("Filter by Type:", types)
                    else:
                        selected_type = 'All'
                
                with col3:
                    if 'market' in df.columns:
                        markets = ['All'] + sorted(df['market'].unique().tolist())
                        selected_market = st.selectbox("Filter by Market:", markets)
                    else:
                        selected_market = 'All'
                
                # Apply filters
                filtered_df = df.copy()
                
                if selected_exchange != 'All':
                    filtered_df = filtered_df[filtered_df['primary_exchange'] == selected_exchange]
                
                if selected_type != 'All':
                    filtered_df = filtered_df[filtered_df['type'] == selected_type]
                
                if selected_market != 'All':
                    filtered_df = filtered_df[filtered_df['market'] == selected_market]
                
                st.write(f"**Filtered Results: {len(filtered_df):,} tickers**")
                
                # Search functionality
                search_term = st.text_input("Search tickers:", placeholder="Enter ticker symbol or company name...")
                
                if search_term:
                    if 'ticker' in df.columns and 'name' in df.columns:
                        search_mask = (
                            df['ticker'].str.contains(search_term, case=False, na=False) |
                            df['name'].str.contains(search_term, case=False, na=False)
                        )
                        filtered_df = filtered_df[search_mask]
                        st.write(f"**Search Results: {len(filtered_df):,} tickers**")
                
                # Display filtered data
                if len(filtered_df) > 0:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.info("No data matches the selected filters.")
            
            with tab3:
                st.subheader("Data Analytics")
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    market_chart = create_market_distribution_chart(df)
                    if market_chart:
                        st.plotly_chart(market_chart, use_container_width=True)
                
                with col2:
                    exchange_chart = create_exchange_distribution_chart(df)
                    if exchange_chart:
                        st.plotly_chart(exchange_chart, use_container_width=True)
                
                # Type distribution
                type_chart = create_type_distribution_chart(df)
                if type_chart:
                    st.plotly_chart(type_chart, use_container_width=True)
                
                # Summary statistics
                st.subheader("Summary Statistics")
                
                if 'primary_exchange' in df.columns:
                    st.write("**Top 10 Exchanges:**")
                    exchange_summary = df['primary_exchange'].value_counts().head(10)
                    st.dataframe(exchange_summary.reset_index().rename(columns={'index': 'Exchange', 'primary_exchange': 'Count'}))
                
                if 'type' in df.columns:
                    st.write("**Security Types:**")
                    type_summary = df['type'].value_counts()
                    st.dataframe(type_summary.reset_index().rename(columns={'index': 'Type', 'type': 'Count'}))
            
            with tab4:
                st.subheader("Raw Data")
                
                # Data download
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Display all data
                st.write(f"**Complete Dataset: {len(df):,} rows**")
                
                # Pagination
                page_size = st.selectbox("Rows per page:", [50, 100, 500, 1000], index=1)
                total_pages = (len(df) - 1) // page_size + 1
                
                if total_pages > 1:
                    page = st.number_input("Page:", min_value=1, max_value=total_pages, value=1)
                    start_idx = (page - 1) * page_size
                    end_idx = start_idx + page_size
                    st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
                    st.write(f"Showing rows {start_idx + 1} to {min(end_idx, len(df))} of {len(df)}")
                else:
                    st.dataframe(df, use_container_width=True)
        
        else:
            st.error("Failed to load the selected file.")

if __name__ == "__main__":
    main()
