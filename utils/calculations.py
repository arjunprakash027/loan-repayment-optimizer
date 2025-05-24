"""
All the loan related calculations happen here
"""

import numpy as np
from datetime import datetime

def calculate_interest_per_month(
        pa: float,
        interest_per_annum: float
) -> float:
    
    interest_per_month = (interest_per_annum / 12)

    return pa * interest_per_month


def calculate_pre_emi_interest(
    pa: float,
    loan_disbursal_date: datetime,
    emi_start_date: datetime,
    interest_per_annum: float
) -> float:
    
    per_day_interest_rough = round((interest_per_annum / 365), 5)
    days_difference = (emi_start_date - loan_disbursal_date).days

    return pa * per_day_interest_rough * (days_difference - 1)