import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Fish Store Analysis", layout="wide", initial_sidebar_state="expanded")

# Function to load dataset
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, parse_dates=['Date', 'Date of Sale', 'Restock Date'])
        df['Profit'] = df['Total Sales Value (NGN)'] - df['Total Supply Cost (NGN)']
        df.set_index('Date', inplace=True)  # Set Date as index for time-series analysis
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Sidebar - Navigation
st.sidebar.title("Navigation")
options = ["Home", "Overview", "Trend Analysis", "Product Analysis", "Brand Supplier Analysis", "Customer Behavioural Analysis"]
selected_option = st.sidebar.radio("Choose a section:", options)

# Home Section
if selected_option == "Home":
    st.title("Welcome to Fish Store Analysis")
    st.write("This app provides an interactive way to explore and analyze data from your fish store.")
    st.image("fish_store_image.jpg", caption="Fish Store Analysis", use_container_width=True)
    st.write("Navigate through the sections to discover insights about trends, products, suppliers, and customer behaviors.")

# Upload dataset
uploaded_file = st.sidebar.file_uploader("Upload your fish store dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Loading dataset..."):
        df = load_data(uploaded_file)

    if df is not None:
        st.sidebar.success("Dataset loaded successfully!")

        # Sidebar Filters
        if selected_option != "Home":
            st.sidebar.title("Filters")
            date_range = st.sidebar.date_input(
                "Select Date Range", 
                [df.index.min().date(), df.index.max().date()]
            )
            fish_type_filter = st.sidebar.multiselect(
                "Select Fish Type", 
                options=df['Fish Type'].unique(), 
                default=df['Fish Type'].unique()
            )
            supplier_filter = st.sidebar.multiselect(
                "Select Supplier", 
                options=df['Supplier Information'].unique(), 
                default=df['Supplier Information'].unique()
            )

            # Apply filters
            filtered_df = df[
                (df.index.date >= date_range[0]) & 
                (df.index.date <= date_range[1]) & 
                (df['Fish Type'].isin(fish_type_filter)) & 
                (df['Supplier Information'].isin(supplier_filter))
            ]

        # Analysis Options
        if selected_option == "Overview":
            st.title("Fish Store Dataset Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Profit", f"NGN {filtered_df['Profit'].sum():,.2f}")
            col2.metric("Total Sales Value", f"NGN {filtered_df['Total Sales Value (NGN)'].sum():,.2f}")
            col3.metric("Total Quantity Sold", f"{filtered_df['Quantity Sold (kg)'].sum():,.2f} kg")

            st.markdown("### Dataset Preview")
            st.write(filtered_df.head())

            st.markdown("### Dataset Statistics")
            st.write(filtered_df.describe())

            st.markdown("### Total Sales Value Over Time")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df['Total Sales Value (NGN)'].resample('M').sum().plot(ax=ax, color='green')
            ax.set_title("Monthly Total Sales Value")
            ax.set_xlabel("Month")
            ax.set_ylabel("Sales Value (NGN)")
            st.pyplot(fig)

        elif selected_option == "Trend Analysis":
            # Your existing code for Trend Analysis
            pass

        elif selected_option == "Product Analysis":
            # Your existing code for Product Analysis
            pass

        elif selected_option == "Brand Supplier Analysis":
            # Your existing code for Brand Supplier Analysis
            pass

        elif selected_option == "Customer Behavioural Analysis":
            # Your existing code for Customer Behavioural Analysis
            pass

else:
    if selected_option == "Home":
        st.write("Please upload your dataset to begin exploring other sections.")
    else:
        st.warning("No dataset uploaded. Please upload a dataset to access this section.")
