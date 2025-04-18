import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from rds_utils import check_user_exists

# Setting icon and tab label
st.set_page_config(page_title="Finances", page_icon="🌆")

# Show information:
# Consider changing "Your" below to the name of the person according to their ID
st.write("# Your Personal Finances")
st.write("If there seem to be any discrepancies in your information, please email the team behind this page!")
st.write("We would be glad to help fix and bolster your experience on FinClad!")

# Retrieve customer ID from session state
customer_id = st.session_state.get('customer_id')

if customer_id:
    user = check_user_exists(customer_id)

    if user:
        st.success(f"Welcome, {user['firstName']}!")

        # Prepare user financial data for graphing
        user_data = {
            "Account Balance": float(user["accountBalance"]),
            "Credit Limit": float(user["creditLimit"]),
            "Credit Card Balance": float(user["creditCardBalance"])
        }

        # Convert user financial data into a DataFrame
        user_df = pd.DataFrame(user_data.items(), columns=["Category", "Amount"])

        # Create a barplot for the financial summary
        fig, ax = plt.subplots()
        sns.barplot(data=user_df, x="Category", y="Amount", ax=ax, palette="Blues_d")
        ax.set_title("Your Financial Summary")
        st.pyplot(fig)

        # Display the raw data as a table
        st.dataframe(user_df.set_index("Category"))

    else:
        st.error("User ID not found. Please register on the Home page first.")
else:
    st.error("No user ID found. Please ensure you're logged in properly.")
