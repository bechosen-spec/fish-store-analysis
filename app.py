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

# Sidebar - Upload dataset
st.sidebar.title("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your fish store dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Loading dataset..."):
        df = load_data(uploaded_file)

    if df is not None:
        st.sidebar.success("Dataset loaded successfully!")

        # Sidebar - Filter options
        st.sidebar.title("Filters")
        date_range = st.sidebar.date_input("Select Date Range", 
                                           [df.index.min().date(), df.index.max().date()])
        fish_type_filter = st.sidebar.multiselect("Select Fish Type", 
                                                  options=df['Fish Type'].unique(), 
                                                  default=df['Fish Type'].unique())
        supplier_filter = st.sidebar.multiselect("Select Supplier", 
                                                 options=df['Supplier Information'].unique(), 
                                                 default=df['Supplier Information'].unique())

        # Apply filters
        filtered_df = df[(df.index.date >= date_range[0]) & 
                         (df.index.date <= date_range[1]) & 
                         (df['Fish Type'].isin(fish_type_filter)) & 
                         (df['Supplier Information'].isin(supplier_filter))]

        # Sidebar - Analysis options
        st.sidebar.title("Analysis Options")
        option = st.sidebar.radio("Select an Analysis", 
                                   ["Overview", "Trend Analysis", 
                                    "Product Analysis", "Brand Supplier Analysis", 
                                    "Customer Behavioural Analysis"])

        # Overview
        if option == "Overview":
            st.title("Fish Store Dataset Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Profit", f"NGN {filtered_df['Profit'].sum():,.2f}")
            col2.metric("Total Sales Value", f"NGN {filtered_df['Total Sales Value (NGN)'].sum():,.2f}")
            col3.metric("Total Quantity Sold", f"{filtered_df['Quantity Sold (kg)'].sum():,.2f} kg")
            
            st.markdown("### Dataset Preview")
            st.write(filtered_df.head())

            st.markdown("### Dataset Statistics")
            st.write(filtered_df.describe())

            # Additional Chart: Sales Value Over Time
            st.markdown("### Total Sales Value Over Time")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df['Total Sales Value (NGN)'].resample('M').sum().plot(ax=ax, color='green')
            ax.set_title("Monthly Total Sales Value")
            ax.set_xlabel("Month")
            ax.set_ylabel("Sales Value (NGN)")
            st.pyplot(fig)

            st.markdown("### Proportion of Fish Types Sold")
            fish_type_counts = filtered_df['Fish Type'].value_counts()
            fig, ax = plt.subplots()
            fish_type_counts.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, colormap='viridis')
            ax.set_ylabel("")
            ax.set_title("Fish Type Proportion")
            st.pyplot(fig)


        # Trend Analysis
        elif option == "Trend Analysis":
            st.title("Trend Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Annual Trend of Cost per Unit Supplied")
                fig, ax = plt.subplots()
                filtered_df['Cost per Unit Supply (NGN)'].resample('A').mean().plot(ax=ax, color='red', label='Annual Trend')
                ax.set_title('Annual Trend - Cost per Unit Supplied')
                ax.set_xlabel('Year')
                ax.set_ylabel('Mean Cost (NGN)')
                ax.legend()
                st.pyplot(fig)

            with col2:
                st.markdown("#### Annual Trend of Price per Unit Sold")
                fig, ax = plt.subplots()
                filtered_df['Price per Unit Sold (NGN)'].resample('A').mean().plot(ax=ax, color='blue', label='Annual Trend')
                ax.set_title('Annual Trend - Price per Unit Sold')
                ax.set_xlabel('Year')
                ax.set_ylabel('Mean Price (NGN)')
                ax.legend()
                st.pyplot(fig)

            # Additional Chart: Profit Over Time
            st.markdown("### Monthly Profit Over Time")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df['Profit'].resample('M').sum().plot(ax=ax, color='purple')
            ax.set_title("Monthly Profit Over Time")
            ax.set_xlabel("Month")
            ax.set_ylabel("Total Profit (NGN)")
            st.pyplot(fig)

        # Product Analysis
        elif option == "Product Analysis":
            st.title("Product Analysis")
            
            st.markdown("### Product Type Frequency")
            product_type_freq = filtered_df.groupby('Fish Type')['Quantity Sold (kg)'].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Quantity Sold (kg)', y='Fish Type', data=product_type_freq, palette='viridis', ax=ax)
            ax.set_title("Quantity Sold by Fish Type")
            st.pyplot(fig)
            
            st.markdown("### Fish Size Frequency")
            fish_size_freq = filtered_df.groupby('Fish Size')['Quantity Sold (kg)'].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Quantity Sold (kg)', y='Fish Size', data=fish_size_freq, palette='coolwarm', ax=ax)
            ax.set_title("Quantity Sold by Fish Size")
            st.pyplot(fig)

            # Additional Chart: Top 5 Fish Types by Revenue
            st.markdown("### Top 5 Fish Types by Total Revenue")
            top_revenue = filtered_df.groupby('Fish Type')['Total Sales Value (NGN)'].sum().nlargest(5).reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Total Sales Value (NGN)', y='Fish Type', data=top_revenue, palette='magma', ax=ax)
            ax.set_title("Top 5 Fish Types by Revenue")
            st.pyplot(fig)

        # Brand Supplier Analysis
        elif option == "Brand Supplier Analysis":
            st.title("Brand Supplier Analysis")
            
            st.markdown("### Profit by Supplier")
            supplier_profit = filtered_df.groupby('Supplier Information')['Profit'].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Profit', y='Supplier Information', data=supplier_profit, palette='Spectral', ax=ax)
            ax.set_title("Profit by Supplier")
            st.pyplot(fig)
            
            st.markdown("### Quantity Sold by Supplier")
            supplier_quantity = filtered_df.groupby('Supplier Information')['Quantity Sold (kg)'].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Quantity Sold (kg)', y='Supplier Information', data=supplier_quantity, palette='Set2', ax=ax)
            ax.set_title("Quantity Sold by Supplier")
            st.pyplot(fig)

            # Additional Chart: Supplier Performance by Average Profit
            st.markdown("### Average Profit Per Transaction by Supplier")
            avg_profit = filtered_df.groupby('Supplier Information')['Profit'].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Profit', y='Supplier Information', data=avg_profit, palette='cool', ax=ax)
            ax.set_title("Average Profit Per Supplier")
            st.pyplot(fig)

        # Customer Behavioural Analysis
        elif option == "Customer Behavioural Analysis":
            st.title("Customer Behavioural Analysis")
            
            st.markdown("### Profit by Customer Type")
            customer_profit = filtered_df.groupby('Customer Type')['Profit'].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Profit', y='Customer Type', data=customer_profit, palette='Blues', ax=ax)
            ax.set_title("Profit by Customer Type")
            st.pyplot(fig)
            
            st.markdown("### Sales Channel by Location")
            sales_channel = filtered_df.groupby(['Customer Location', 'Sales Channel'])['Quantity Sold (kg)'].sum().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Quantity Sold (kg)', y='Customer Location', hue='Sales Channel', data=sales_channel, ax=ax)
            ax.set_title("Sales Channel Usage by Location")
            st.pyplot(fig)

            # Additional Chart: Total Sales by Customer Location
            st.markdown("### Total Sales by Customer Location")
            total_sales_location = filtered_df.groupby('Customer Location')['Total Sales Value (NGN)'].sum().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Total Sales Value (NGN)', y='Customer Location', data=total_sales_location, palette='pastel', ax=ax)
            ax.set_title("Total Sales by Customer Location")
            st.pyplot(fig)

    else:
        st.title("Fish Store Dataset Analysis")
        st.write("Please upload your dataset to begin analysis.")
