import reflex as rx
from Wearly.Frontend.home_page_structure import sidebar_items


def discover_n_shop_page_main_content() -> rx.Component:
    return rx.vstack(    
        rx.divider(),
        rx.hstack(
            sidebar_items("shop"),
            rx.vstack(
                rx.heading("Shop Page"),
                rx.text("Welcome to the shop page!"),
            ),
        ),   
        width="100%",
    )

