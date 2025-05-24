"""
This is where we calculate the repayment schedule
"""

import numpy as np
import pandas as pd
from datetime import datetime
from utils.calculations import calculate_interest_per_month, calculate_pre_emi_interest
import math

def smart_round(number: float) -> float:
    """Round up if decimal >= 0.5, round down if < 0.5"""
    decimal_part = number - math.floor(number)
    if decimal_part >= 0.5:
        return math.ceil(number)
    return math.floor(number)

def repayment_calender(
    loan_disbursal_date: str | datetime,
    start_date: str | datetime,
    pa: int,
    end_of_morotorium_date: str | datetime,
    morotorium_emi: int,
    after_morotorium_emi: int,
    annual_interest: float = 0.1175
) -> pd.DataFrame:

    """
    Repayment Schedule calculation happens here, 
    Give the Start Date of interest ,Principle amount, Annual Interest
    end of morotorium date, morotorim payment emi and after morotorium emi amount

    Returns a dataframe with full schedule
    """

    
    repayment_schedule_df = pd.DataFrame(
        columns=[
            "instal_no",
            "due_date",
            "opening_principal",
            "emi",
            "principal_comp",
            "interest_comp",
            "closing_principal"
        ]
    )

    installment_no = 1
    start_date = pd.to_datetime(start_date)
    current_date = start_date
    end_of_morotorium_date = pd.to_datetime(end_of_morotorium_date)
    loan_disbursal_date = pd.to_datetime(loan_disbursal_date)
    opening_pa = smart_round(pa)


    while True:
        current_installment = {
            "instal_no": installment_no,
            "due_date": current_date,
            "opening_principal": opening_pa,
            "emi": 0,
            "principal_comp": 0,
            "interest_comp": 0,
            "closing_principal": 0
        }


        # Current interest
        if current_date != start_date:
            interest = smart_round(
                calculate_interest_per_month(
                    pa=opening_pa,
                    interest_per_annum=annual_interest
                )
            )
        else:
            interest = smart_round(
                calculate_pre_emi_interest(
                    loan_disbursal_date=loan_disbursal_date,
                    emi_start_date=start_date,
                    pa=opening_pa,
                    interest_per_annum=annual_interest
                )
            )
        current_installment['interest_comp'] = interest

        # Update the EMI based on before/after moratorium
        if current_date <= end_of_morotorium_date:
            emi = smart_round(morotorium_emi)
        else:
            emi = smart_round(after_morotorium_emi)

        if emi <= opening_pa:
            current_installment['emi'] = emi
        else:
            emi = smart_round(opening_pa + interest)
            current_installment['emi'] = emi

        # Current principal that will be added to opening principal to create next principal
        current_principal = smart_round(emi - interest)

        current_installment['principal_comp'] = current_principal

        # Closing principal
        closing_pa = smart_round(opening_pa - current_principal)

        current_installment['closing_principal'] = closing_pa

        # Append the current installment to the DataFrame
        repayment_schedule_df = pd.concat(
            [repayment_schedule_df, pd.DataFrame([current_installment])],
            ignore_index=True
        )

        # Update for next iteration
        installment_no += 1
        current_date = current_date + pd.DateOffset(months=1)
        opening_pa = closing_pa

        # Break condition
        if opening_pa <= 0:
            break

    return repayment_schedule_df

if __name__ == "__main__":
    # Example inputs
    loan_disbursal_date = "2025-05-22"
    start_date = "2025-07-01"
    principal_amount = 100000
    end_of_morotorium_date = "2027-06-01"
    morotorium_emi = 5000
    after_morotorium_emi = 10000
    annual_interest_rate = 0.1100

    schedule = repayment_calender(
        loan_disbursal_date=loan_disbursal_date,
        start_date=start_date,
        pa=principal_amount,
        end_of_morotorium_date=end_of_morotorium_date,
        morotorium_emi=morotorium_emi,
        after_morotorium_emi=after_morotorium_emi,
        annual_interest=annual_interest_rate
    )

    print(schedule)
    schedule.to_csv("Schedule.csv")
    print(schedule['emi'].sum())








