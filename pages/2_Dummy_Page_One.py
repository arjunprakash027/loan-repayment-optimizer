import streamlit as st
from datetime import date

st.set_page_config(page_title="Dummy Page One", layout="centered") # Or "wide" if preferred

st.title("Dummy Page One")

st.markdown("This is the first dummy page. Functionality will be added later.")

st.subheader("Sample Inputs")
text_input_val = st.text_input("Enter some text", placeholder="Type here...")
number_input_val = st.number_input("Enter a number", value=42, step=1)
date_input_val = st.date_input("Select a date", value=date.today())

st.write(f"Text input: {text_input_val}")
st.write(f"Number input: {number_input_val}")
st.write(f"Date input: {date_input_val}")
