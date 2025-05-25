import reflex as rx
from utils.repayment_schedule import repayment_calender
import pandas as pd
from typing import List, Dict
from ui.components.form_components import form_section, form_input, summary_card

class LoanState(rx.State):

    loan_repayment_df: pd.DataFrame = pd.DataFrame({})
    is_loading: bool = False
    has_data: bool = False

    @rx.var
    def total_emi_payments(self) -> str:
        if self.has_data and not self.loan_repayment_df.empty:
            return f"₹{self.loan_repayment_df['emi'].sum():,.0f}"
        return "₹0"
    
    @rx.var
    def total_interest(self) -> str:
        if self.has_data and not self.loan_repayment_df.empty:
            return f"₹{self.loan_repayment_df['interest_comp'].sum():,.0f}"
        return "₹0"
    
    @rx.var
    def loan_duration(self) -> str:
        if self.has_data and not self.loan_repayment_df.empty:
            return f"{len(self.loan_repayment_df)} months"
        return "0 months"

    def handle_submit(self, form_data: dict):
            
        """Process form submission and calculate repayment schedule"""
        self.is_loading = True
        yield
        
        try:
            df = repayment_calender(
                loan_disbursal_date=form_data["loan_disbursal_date"],
                start_date=form_data["start_date"],
                pa=int(form_data["principal_amount"]),
                end_of_morotorium_date=form_data["end_of_morotorium_date"],
                morotorium_emi=int(form_data["morotorium_emi"]),
                after_morotorium_emi=int(form_data["after_morotorium_emi"]),
                annual_interest=float(form_data["annual_interest_rate"]),
            )
            self.loan_repayment_df = df
            self.has_data = True
        except Exception as e:
            print(f"Error calculating repayment: {e}")
        finally:
            self.is_loading = False

def input_details() -> rx.Component:
    """Main component for loan input form and results"""
    return rx.container(
        rx.vstack(
            # Header Section
            rx.center(
                rx.vstack(
                    rx.hstack(
                        rx.icon("calculator", size=32, color="var(--blue-9)"),
                        rx.heading(
                            "Loan Repayment Calculator",
                            size="8",
                            color="var(--gray-12)",
                            weight="bold",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    rx.text(
                        "Calculate your loan repayment schedule with moratorium periods",
                        size="4",
                        color="var(--gray-10)",
                        text_align="center",
                    ),
                    align="center",
                    spacing="2",
                ),
                margin_bottom="8",
            ),

            # Form Section
            rx.form(
                rx.vstack(
                    # Date Configuration Section
                    form_section(
                        "Loan Timeline",
                        "calendar",
                        [
                            rx.hstack(
                                form_input(
                                    "Loan Disbursal Date",
                                    name="loan_disbursal_date",
                                    type="date",
                                    default_value="2025-05-22",
                                ),
                                form_input(
                                    "EMI Start Date",
                                    name="start_date",
                                    type="date",
                                    default_value="2025-07-01",
                                ),
                                form_input(
                                    "End of Moratorium",
                                    name="end_of_morotorium_date",
                                    type="date",
                                    default_value="2027-06-01",
                                ),
                                spacing="4",
                                width="100%",
                                flex_wrap="wrap",
                            ),
                        ]
                    ),

                    # Financial Parameters Section
                    form_section(
                        "Financial Details",
                        "indian-rupee",
                        [
                            rx.hstack(
                                form_input(
                                    "Principal Amount (₹)",
                                    name="principal_amount",
                                    type="number",
                                    default_value="100000",
                                    min_="0",
                                    placeholder="e.g., 100000",
                                ),
                                form_input(
                                    "Annual Interest Rate",
                                    name="annual_interest_rate",
                                    type="number",
                                    default_value="0.1100",
                                    min_="0",
                                    max_="1",
                                    step="0.0001",
                                    placeholder="e.g., 0.11 for 11%",
                                ),
                                spacing="4",
                                width="100%",
                                flex_wrap="wrap",
                            ),
                            rx.hstack(
                                form_input(
                                    "Moratorium EMI (₹)",
                                    name="morotorium_emi",
                                    type="number",
                                    default_value="5000",
                                    min_="0",
                                    placeholder="e.g., 5000",
                                ),
                                form_input(
                                    "Post-Moratorium EMI (₹)",
                                    name="after_morotorium_emi",
                                    type="number",
                                    default_value="10000",
                                    min_="0",
                                    placeholder="e.g., 10000",
                                ),
                                spacing="4",
                                width="100%",
                                flex_wrap="wrap",
                            ),
                        ]
                    ),

                    # Submit Button
                    rx.center(
                        rx.button(
                            rx.cond(
                                LoanState.is_loading,
                                rx.hstack(
                                    rx.spinner(size="1", color="white"),
                                    rx.text("Calculating...", size="3"),
                                    align="center",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.icon("calculator", size=16),
                                    rx.text("Generate Schedule", size="3", weight="medium"),
                                    align="center",
                                    spacing="2",
                                ),
                            ),
                            type_="submit",
                            size="3",
                            variant="solid",
                            color_scheme="blue",
                            padding="16px 32px",
                            border_radius="8px",
                            cursor="pointer",
                            disabled=LoanState.is_loading,
                            _hover={
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 12px var(--blue-4)",
                            },
                            transition="all 0.2s ease",
                        ),
                        margin_y="6",
                    ),

                    spacing="6",
                    width="100%",
                ),
                on_submit=LoanState.handle_submit,
                width="100%",
            ),

            # Results Section
            rx.cond(
                LoanState.has_data,
                rx.vstack(
                    # Summary Cards
                    rx.center(
                        rx.hstack(
                            summary_card(
                                "Total EMI Payments",
                                LoanState.total_emi_payments,
                                "credit-card",
                                "blue"
                            ),
                            summary_card(
                                "Total Interest",
                                LoanState.total_interest,
                                "trending-up",
                                "orange"
                            ),
                            summary_card(
                                "Loan Duration",
                                LoanState.loan_duration,
                                "calendar-days",
                                "green"
                            ),
                            spacing="4",
                            flex_wrap="wrap",
                            justify="center",
                        ),
                        margin_y="6",
                    ),

                    # Data Table
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("table", size=20, color="var(--gray-9)"),
                                rx.heading(
                                    "Repayment Schedule",
                                    size="5",
                                    color="var(--gray-12)",
                                    weight="medium",
                                ),
                                align="center",
                                spacing="2",
                                margin_bottom="4",
                            ),
                            rx.data_table(
                                data=LoanState.loan_repayment_df,
                                pagination=True,
                                search=True,
                                sort=True,
                                overflow="auto",
                                width="100%",
                                max_height="600px",
                                style={
                                    "fontSize": "14px",
                                    "fontFamily": "system-ui, sans-serif",
                                    "td": {
                                        "padding": "12px 16px",
                                        "borderBottom": "1px solid var(--gray-5)",
                                    },
                                    "th": {
                                        "padding": "16px",
                                        "backgroundColor": "var(--gray-3)",
                                        "fontWeight": "600",
                                        "color": "var(--gray-11)",
                                        "borderBottom": "2px solid var(--gray-6)",
                                        "textAlign": "left",
                                    },
                                    "tbody tr:hover": {
                                        "backgroundColor": "var(--blue-2)",
                                    },
                                },
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="6",
                        background="white",
                        border="1px solid var(--gray-6)",
                        border_radius="12px",
                        box_shadow="0 2px 8px var(--gray-4)",
                    ),

                    spacing="6",
                    width="100%",
                ),
            ),

            spacing="8",
            width="100%",
            align="center",
        ),
        max_width="1200px",
        padding="6",
        margin="0 auto",
    )