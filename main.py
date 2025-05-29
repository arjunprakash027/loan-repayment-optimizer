import streamlit as st

# Set a global page config
st.set_page_config(page_title="Loan Repayment Optimizer", layout="wide")

# Add a title for the main page
st.title("Welcome to the Loan Repayment Optimizer!")

# Add some introductory text
st.markdown("Select a tool from the sidebar to get started.")

# No session state initializations needed here as they are page-specific.
# No main execution block needed for simple Streamlit page like this.
# Streamlit runs the script from top to bottom.
