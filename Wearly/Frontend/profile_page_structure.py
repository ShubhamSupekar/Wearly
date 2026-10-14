import reflex as rx
from Wearly.Frontend.home_page_structure import sidebar_items


def profile_page_main_content() -> rx.Component:
    return rx.vstack(    
        rx.divider(),
        rx.hstack(
            sidebar_items("profile"),
            rx.vstack(
                rx.heading("Profile Page"),
                rx.text("Welcome to the profile page!"),
            ),
        ),   
        width="100%",
    )

