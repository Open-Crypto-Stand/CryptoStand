import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def register_user():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("Registration successful!")
            else:
                st.error(f"Error: {response.json()['detail']}")
        else:
            st.error("Please fill in both fields.")


def login_user():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("Login successful!")
            else:
                st.error(f"Error: {response.json()['detail']}")
        else:
            st.error("Please fill in both fields.")

st.title("User Authentication")

auth_option = st.radio("Choose an option", ("Register", "Login"))

if auth_option == "Register":
    register_user()
else:
    login_user()