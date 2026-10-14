import reflex as rx
from Wearly.Frontend import about_page_structure
from rxconfig import config
from Wearly.Backend.login import Login
from Wearly.Frontend.home_page_structure import home_page_main_content
from Wearly.Frontend.about_page_structure import about_page_main_Content
from Wearly.Frontend.login_page_strucutre import login_page_main_content
from Wearly.Frontend.profile_page_structure import profile_page_main_content
from Wearly.Frontend.discover_n_shop_page_structure import discover_n_shop_page_main_content


class State(rx.State):
    """The app state."""


def about_page() -> rx.Component:
    return about_page_main_Content()


@rx.page(route="/home",on_load=Login.check_login)
def home_page() -> rx.Component:
    return rx.cond(
        Login.is_logged_in,
        home_page_main_content(),
        rx.text("Please log in to continue."),
        )


@rx.page(route="/profile",on_load=Login.check_login)
def profile_page() -> rx.Component:
    return rx.cond(
            Login.is_logged_in,
            profile_page_main_content(),
            rx.text("Please log in to continue."),
            )


@rx.page(route="/shop",on_load=Login.check_login)
def shop_page() -> rx.Component:
    return rx.cond(
            Login.is_logged_in,
            discover_n_shop_page_main_content(),
            rx.text("Please log in to continue."),
            )


@rx.page(route="/login")
def login_page() -> rx.Component:
    return login_page_main_content()


app = rx.App()

app.add_page(about_page, route="/")