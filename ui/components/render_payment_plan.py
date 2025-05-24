import reflex as rx
from utils.repayment_schedule import repayment_calender
from reflex_ag_grid import ag_grid
import pandas as pd
from typing import List, Dict

class LoanState(rx.State):
    loan_disbursal_date: str | None = "2025-05-22"
    start_date: str | None = "2025-07-01"
    principal_amount: int | None = 100_000
    end_of_morotorium_date: str | None = "2027-06-01"
    morotorium_emi: int | None = 5_000
    after_morotorium_emi: int | None = 10_000
    annual_interest_rate: float | None = 0.1100

    loan_repayment_df: pd.DataFrame = pd.DataFrame({})


    def handle_submit(self, form_data: dict):
        """
        form_data is a dict of {input_name: value} where every value
        arrives **as a string**.  Convert here, then run the calculator.
        """
        df = repayment_calender(
            loan_disbursal_date = form_data["loan_disbursal_date"],
            start_date          = form_data["start_date"],
            pa                  = int(form_data["principal_amount"]),
            end_of_morotorium_date = form_data["end_of_morotorium_date"],
            morotorium_emi      = int(form_data["morotorium_emi"]),
            after_morotorium_emi= int(form_data["after_morotorium_emi"]),
            annual_interest     = float(form_data["annual_interest_rate"]),
        )
        self.loan_repayment_df = df

def form_input(component_name: str, **props):

    return rx.vstack(
        rx.text(component_name,size='2',weight="bold"),
        rx.input(**props),
        align='start',
    )

#  Public component imported in index()
def input_details() -> rx.Component:
    return rx.vstack(
        rx.form(
            # ── dates ─────────────────────────────────────────────
            form_input(
                "Loan disbursal date",
                name="loan_disbursal_date",
                type="date",
                default_value="2025-05-22",
            ),
            form_input(
                "EMI start date",
                name="start_date",
                type="date",
                default_value="2025-07-01",
            ),
            form_input(
                "End of moratorium",
                name="end_of_morotorium_date",
                type="date",
                default_value="2027-06-01",
            ),

            # ── numbers ───────────────────────────────────────────
            form_input(
                "Principal amount (₹)",
                name="principal_amount",
                type="number",
                default_value="100000",
                min_="0",
            ),
            form_input(
                "Moratorium EMI (₹)",
                name="morotorium_emi",
                type="number",
                default_value="5000",
            ),
            form_input(
                "EMI after moratorium (₹)",
                name="after_morotorium_emi",
                type="number",
                default_value="10000",
                min_="0",
            ),
            form_input(
                "Annual interest rate (e.g. 0.11)",
                name="annual_interest_rate",
                type="number",
                default_value="0.1100",
                min_="0",
                max_="1",
                step="0.0001",
                #pattern="[0-9]*.?[0-9]*"
            ),

            # ── action ────────────────────────────────────────────
            rx.button("Generate Schedule", type_="submit"),

            on_submit=LoanState.handle_submit,   # single state update
            spacing="4",
        ),
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
