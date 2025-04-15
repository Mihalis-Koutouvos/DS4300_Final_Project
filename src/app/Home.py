import streamlit as st

#Setting icon and tab label
st.set_page_config(
    page_title="Home",
    page_icon="⚓",
)

#Title for home page
st.write("# FinClad: A Data Cleaner for Finances")

#Intro text
st.write("Welcome to FinClad, a data cleaner and visualization tool for your personl finances!")
st.write("If you have an already-created ID, simply type it into the field called ID and click the Enter button.")
st.write("If you do not have an account, please type your information into the designated fields and the click Enter!")


#Button to proceed with financial data:
st.text_input("User ID")
st.button("Enter", type="primary")

#Begin process of collecting information based on user input:
first_name = st.text_input("First Name: ")
last_name = st.text_input("Last Name: ")
age = st.text_input("Age: ")
city = st.text_input("City: ")
email = st.text_input("Email: ")
account_balance = st.text_input("Account Balance: ")
credit_limit = st.text_input("Credit Limit: ")
credit_card_balance = st.text_input("Credit Card Balance: ")

