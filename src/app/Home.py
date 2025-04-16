import streamlit as st
from rds_utils import check_user_exists, insert_user_into_rds
from s3_utils import upload_user_data_to_s3
import random
import pandas as pd

#Setting icon and tab label
st.set_page_config(
    page_title="Home",
    page_icon="⚓",
)


def generate_customer_id():
    return f"USR_{random.randint(100000, 999999)}"


#Title for home page
st.write("# FinClad: A Data Cleaner for Finances")

#Intro text
st.write("Welcome to FinClad, a data cleaner and visualization tool for your personal finances!")
st.write("If you have an already-created ID, simply type it into the field called ID and click the Enter button.")
st.write("If you do not have an account, please type your information into the designated fields and the click Enter!")


#Button to proceed with financial data:
customer_id = st.text_input("User ID")

if st.button("Enter"):
    user = check_user_exists(customer_id)

    if user:
        st.success(f"Welcome back, {user['firstName']} {user['lastName']}!")
        st.write("You're already registered. No need to fill the form.")
        # Optionally: show more user data
    else:
        customer_id = generate_customer_id()
        st.warning("Looks like you're new. Please fill out the registration form.")


# allow user to upload csv file
uploaded_files = st.file_uploader("...or upload a CSV with your information", type=["csv"], accept_multiple_files=True)
# Store all CSVs in one list
monthly_data = []

# Populate form from the first file
csv_data = {}

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        try:
            df = pd.read_csv(file)
            if df.empty:
                st.warning(f"File {file.name} is empty.")
            else:
                monthly_data.append((file.name, df))

                # Populate form from first file only
                if i == 0:
                    row = df.iloc[0]
                    csv_data = {
                        "firstName": row.get("First Name", ""),
                        "lastName": row.get("Last Name", ""),
                        "age": str(row.get("Age", "")),
                        "city": row.get("City", ""),
                        "email": row.get("Email", ""),
                        "accountBalance": str(row.get("Account Balance", "")),
                        "creditLimit": str(row.get("Credit Limit", "")),
                        "creditCardBalance": str(row.get("Credit Card Balance", ""))
                    }

        except Exception as e:
            st.error(f"❌ Failed to process {file.name}: {e}")

    st.success(f"{len(monthly_data)} file(s) processed successfully.")




#Begin process of collecting information based on user input:
first_name = st.text_input("First Name:", value=csv_data.get("firstName", ""))
last_name = st.text_input("Last Name:", value=csv_data.get("lastName", ""))
age = st.text_input("Age:", value=csv_data.get("age", ""))
city = st.text_input("City:", value=csv_data.get("city", ""))
email = st.text_input("Email:", value=csv_data.get("email", ""))
account_balance = st.text_input("Account Balance:", value=csv_data.get("accountBalance", ""))
credit_limit = st.text_input("Credit Limit:", value=csv_data.get("creditLimit", ""))
credit_card_balance = st.text_input("Credit Card Balance:", value=csv_data.get("creditCardBalance", ""))


# Submit button
if st.button("Submit"):
    user_data = {
            "customerId": customer_id,
            "firstName": first_name,
            "lastName": last_name,
            "age": age,
            "city": city,
            "email": email,
            "accountBalance": account_balance,
            "creditLimit": credit_limit,
            "creditCardBalance": credit_card_balance
        }

    try:

        # Upload each file to S3
        for file_name, df in monthly_data:
            record_dict = df.to_dict(orient="records")
            upload_key = f"{customer_id}/{file_name}"
            s3_key = upload_user_data_to_s3(record_dict, identifier=upload_key)
        
            # Insert to RDS
            insert_user_into_rds(record_dict)

        st.success(f"✅ Uploaded to S3 and inserted into RDS!")
    except Exception as e:
        st.error(f"❌ Upload failed: {e}")






