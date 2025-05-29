import streamlit as st
import pandas as pd
from utils.repayment_schedule import repayment_calender
from datetime import date, timedelta

# Set page configuration
st.set_page_config(page_title="Loan Repayment Calculator", layout="wide")

# Initialize session state variables
if 'loan_repayment_df' not in st.session_state:
    st.session_state.loan_repayment_df = pd.DataFrame({})
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'has_data' not in st.session_state:
    st.session_state.has_data = False

def display_loan_calculator():
    """
    Displays the main UI for the Loan Repayment Calculator.
    """
    st.title("Loan Repayment Calculator")
    st.markdown("Calculate your loan repayment schedule with moratorium periods")

    with st.form(key="loan_form"):
        st.header("Loan Timeline")
        col1, col2, col3 = st.columns(3)
        with col1:
            loan_disbursal_date_val = st.date_input("Loan Disbursal Date", value=date(2025, 5, 22), name="loan_disbursal_date")
        with col2:
            start_date_val = st.date_input("EMI Start Date", value=date(2025, 7, 1), name="start_date")
        with col3:
            end_of_morotorium_date_val = st.date_input("End of Moratorium", value=date(2027, 6, 1), name="end_of_morotorium_date")

        st.header("Financial Details")
        col_fin1, col_fin2 = st.columns(2)
        with col_fin1:
            principal_amount_val = st.number_input("Principal Amount (₹)", min_value=0, value=100000, name="principal_amount", type="int")
            morotorium_emi_val = st.number_input("Moratorium EMI (₹)", min_value=0, value=5000, name="morotorium_emi", type="int")
        with col_fin2:
            annual_interest_rate_val = st.number_input("Annual Interest Rate", min_value=0.0, max_value=1.0, value=0.1100, step=0.0001, format="%.4f", name="annual_interest_rate", type="float")
            after_morotorium_emi_val = st.number_input("Post-Moratorium EMI (₹)", min_value=0, value=10000, name="after_morotorium_emi", type="int")
        
        submit_button = st.form_submit_button(label="Generate Schedule")

        if submit_button:
            st.session_state.is_loading = True
            st.session_state.has_data = False # Reset data state on new submission

            try:
                df = repayment_calender(
                    loan_disbursal_date=loan_disbursal_date_val,
                    start_date=start_date_val,
                    pa=int(principal_amount_val),
                    end_of_morotorium_date=end_of_morotorium_date_val,
                    morotorium_emi=int(morotorium_emi_val),
                    after_morotorium_emi=int(after_morotorium_emi_val),
                    annual_interest=float(annual_interest_rate_val)
                )
                st.session_state.loan_repayment_df = df
                st.session_state.has_data = True
            except Exception as e:
                st.error(f"Error calculating repayment: {e}")
                st.session_state.has_data = False
            finally:
                st.session_state.is_loading = False

    if st.session_state.get('is_loading', False):
        with st.spinner("Calculating... Please wait..."):
            pass 
    elif st.session_state.get('has_data', False) and not st.session_state.loan_repayment_df.empty:
        # Calculate summary values
        total_emi = st.session_state.loan_repayment_df['emi'].sum()
        total_interest = st.session_state.loan_repayment_df['interest_comp'].sum()
        loan_duration_months = len(st.session_state.loan_repayment_df)

        # Format them for display
        formatted_total_emi = f"₹{total_emi:,.0f}"
        formatted_total_interest = f"₹{total_interest:,.0f}"
        formatted_loan_duration = f"{loan_duration_months} months"

        # Display Summary Cards
        st.markdown("### Loan Summary")
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        with col_sum1:
            st.metric(label="Total EMI Payments", value=formatted_total_emi)
        with col_sum2:
            st.metric(label="Total Interest Paid", value=formatted_total_interest)
        with col_sum3:
            st.metric(label="Loan Duration", value=formatted_loan_duration)
        
        st.markdown("<br>", unsafe_allow_html=True) # Adding some space

        # Display Data Table
        st.subheader("Repayment Schedule")
        st.dataframe(st.session_state.loan_repayment_df, use_container_width=True)
    elif st.session_state.get('has_data', False) and st.session_state.loan_repayment_df.empty:
        st.warning("Calculation resulted in an empty schedule. Please check your inputs.")

# Call the function to display the calculator
display_loan_calculator()
