import reflex as rx
from utils.repayment_schedule import repayment_calender
from reflex_ag_grid import ag_grid
import pandas as pd
from typing import List, Dict

class LoanState(rx.State):
    loan_disbursal_date: str = "2025-05-22"
    start_date: str = "2025-07-01"
    principal_amount: int = 100_000
    end_of_morotorium_date: str = "2027-06-01"
    morotorium_emi: int = 5_000
    after_morotorium_emi: int = 10_000
    annual_interest_rate: float = 0.1100

    loan_repayment_df: pd.DataFrame = pd.DataFrame({})


    def compute_schedule(self):
        df = repayment_calender(
            loan_disbursal_date=self.loan_disbursal_date,
            start_date=self.start_date,
            pa=self.principal_amount,
            end_of_morotorium_date=self.end_of_morotorium_date,
            morotorium_emi=self.morotorium_emi,
            after_morotorium_emi=self.after_morotorium_emi,
            annual_interest=self.annual_interest_rate,
        )
        self.loan_repayment_df = df

#  Helper for a labelled input bound to LoanState.<field>
def bound_input(label: str, field: str, **kwargs):
    return rx.vstack(
        rx.text(label, size="2", weight="bold"),
        rx.input(
            value=getattr(LoanState, field),
            on_change=lambda v: getattr(LoanState, f"set_{field}")(v),
            **kwargs,
        ),
        align_items="start",
    )

#  Public component imported in index()
def input_details() -> rx.Component:
    return rx.vstack(
        bound_input("Loan disbursal date", "loan_disbursal_date", type="date"),
        bound_input("EMI start date", "start_date", type="date"),
        bound_input("Principal amount (₹)", "principal_amount", type="number"),
        bound_input("End of moratorium date", "end_of_morotorium_date", type="date"),
        bound_input("Moratorium EMI (₹)", "morotorium_emi", type="number"),
        bound_input("EMI after moratorium (₹)", "after_morotorium_emi", type="number"),
        bound_input(
            "Annual interest rate (decimal, e.g. 0.11)",
            "annual_interest_rate",
            type="number",
            step="0.0001",
        ),
        rx.button("Generate Schedule", on_click=LoanState.compute_schedule),
        rx.divider(),
        rx.box(
            rx.data_table(
                data=LoanState.loan_repayment_df,
                pagination=True,
                search=True,
                sort=True,
                overflow="auto",
                width="100%",
                max_height="800px",
                padding="4",
                style={
                    "fontSize": "1rem",
                    "td": {"padding": "12px"},
                    "th": {"padding": "12px", "backgroundColor": "#f5f5f5"},
                },
            ),
            width="100%",
            overflow_x="auto",
            padding="4",
            border_radius="md",
            border="1px solid #eaeaea",
            margin_y="4",
            background_color="white",
        ),
        spacing="4",
        width="100%",
        max_width="1600px",
        align_items="stretch",
    )
