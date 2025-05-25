import reflex as rx
from typing import List

def form_section(title: str, icon: str, children: List[rx.Component]) -> rx.Component:
    """Create a styled form section with icon and title"""
    return rx.card(
        rx.hstack(
            rx.icon(icon, size=20, color="var(--blue-9)"),
            rx.heading(title, size="4", color="var(--blue-11)", weight="medium"),
            align="center",
            spacing="2",
            margin_bottom="4",
        ),
        rx.vstack(
            *children,
            spacing="4",
            width="100%",
        ),
        padding="6",
        background="var(--blue-2)",
        border="1px solid var(--blue-5)",
        border_radius="12px",
    )

def form_input(label: str, **props) -> rx.Component:
    """Create a styled form input with label"""
    return rx.vstack(
        rx.text(
            label,
            size="2",
            weight="medium",
            color="var(--gray-11)",
        ),
        rx.input(
            border="1px solid var(--gray-6)",
            border_radius="8px",
            padding="8px",
            font_size="14px",
            background="black",
            _focus={
                "border_color": "var(--blue-8)",
                "box_shadow": "0 0 0 3px var(--blue-4)",
                "outline": "none",
            },
            _hover={
                "border_color": "var(--gray-7)",
            },
            **props
        ),
        align="start",
        spacing="1",
        width="100%",
    )

def summary_card(title: str, value: str, icon: str, color: str = "blue") -> rx.Component:
    """Create a summary statistics card"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(icon, size=18, color=f"var(--{color}-9)"),
                rx.text(title, size="2", color="var(--gray-11)", weight="medium"),
                align="center",
                spacing="2",
            ),
            rx.text(
                value,
                size="5",
                weight="bold",
                color=f"var(--{color}-11)",
            ),
            align="start",
            spacing="2",
        ),
        padding="4",
        background=f"var(--{color}-2)",
        border=f"1px solid var(--{color}-5)",
        border_radius="8px",
        min_width="200px",
    )