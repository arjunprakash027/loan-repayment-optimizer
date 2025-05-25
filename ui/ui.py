"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from ui.components.render_payment_plan import input_details
class State(rx.State):
    """The app state."""
    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.box(
            rx.color_mode.button(position="fixed", right="4", top="4"),
            rx.vstack(
                input_details(),
                spacing="8",
                justify="center",
                align_items="center",
                min_height="100vh",
                width="100%",
                padding_y="8",
            ),
            rx.logo(),
            width="100%",
        ),
        width="100%",
    )


app = rx.App()
app.add_page(index)
