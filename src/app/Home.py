import streamlit as st
from app.rds_utils import check_user_exists, insert_user_into_rds
from app.s3_utils import upload_user_data_to_s3
import random

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

#Begin process of collecting information based on user input:
first_name = st.text_input("First Name: ")
last_name = st.text_input("Last Name: ")
age = st.text_input("Age: ")
city = st.text_input("City: ")
email = st.text_input("Email: ")
account_balance = st.text_input("Account Balance: ")
credit_limit = st.text_input("Credit Limit: ")
credit_card_balance = st.text_input("Credit Card Balance: ")

# Submit button
if st.button("Submit"):
    if not email:
        st.error("Email is required.")
    else:
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

            # upload to S3
            s3_key = upload_user_data_to_s3(user_data, identifier=customer_id)
            
            # Insert to RDS
            insert_user_into_rds(user_data)

            st.success(f"✅ Uploaded to S3 and inserted into RDS!")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")






